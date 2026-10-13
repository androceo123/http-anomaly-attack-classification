#!/usr/bin/env python3
"""Resume verified recovery from reachable Git history, without experimental execution.

Original datasets remain external. Models are treated as opaque bytes. This
administrative wrapper reuses the existing publication and verification guards.
"""
from __future__ import annotations
import base64
import collections
import gzip
import json
import sys
sys.dont_write_bytecode = True
import recuperar_lote as base

_original_recover = base.recover
_original_reconcile = base.reconcile
RAW_PAYLOAD_LIMIT = 64 * 1024 * 1024


def recover_history(rows, request):
    if not request.get('scan_reachable_history'):
        return _original_recover(rows, request)
    listing = base.git('rev-list', '--objects', '--all').decode('utf-8').splitlines()
    names = {}
    for line in listing:
        sha, _, name = line.partition(' ')
        if len(sha) == 40:
            names.setdefault(sha, name.strip('"'))
    if len(names) > 50000:
        raise ValueError('History scan exceeds administrative object bound')
    metadata = base.git('cat-file', '--batch-check=%(objectname) %(objecttype) %(objectsize)',
                        data=('\n'.join(names) + '\n').encode()).decode().splitlines()
    blobs = []
    for line in metadata:
        sha, kind, size = line.split()
        if kind == 'blob':
            blobs.append((sha, int(size)))
    archives = [{'sha': sha} for sha, size in blobs
                if names[sha].lower().endswith('.zip') and size <= base.MAX_FILE]
    archive_request = dict(request, historical_objects=archives, payload_objects=[])
    restored, blocked, archive_stats = _original_recover(rows, archive_request)
    if restored:
        base.git('add', '-f', '--', *[r['path'] for r in restored])
    present = base.identities(base.tracked())
    wanted = {(int(r['bytes']), r['sha256']) for r in rows
              if base.valid_relative(r['path']).parts[0] in base.ALLOWED_ROOTS
              and r.get('role') != 'dataset_original'
              and (int(r['bytes']), r['sha256']) not in present}
    sizes = {identity[0] for identity in wanted}
    matched = {}
    hashed_count = hashed_bytes = payload_bytes = 0
    for sha, size in sorted(blobs):
        if size not in sizes or size > base.MAX_FILE:
            continue
        data = base.git('cat-file', 'blob', sha)
        if len(data) != size or base.blob_sha(data) != sha:
            raise ValueError('Historical Git object verification failed')
        hashed_count += 1
        hashed_bytes += size
        ident = (size, base.digest(data))
        if ident not in wanted or ident in matched:
            continue
        if payload_bytes + size > RAW_PAYLOAD_LIMIT:
            blocked.append({'path': '[historical Git object]', 'reason': 'raw_payload_memory_bound', 'git_blob_sha': sha})
            continue
        matched[ident] = (sha, data)
        payload_bytes += size
    raw_stats = {'payload_objects': 0}
    raw_restored = []
    if matched:
        payload = {'schema_version': 1, 'files': [
            {'bytes': ident[0], 'sha256': ident[1], 'base64': base64.b64encode(data).decode('ascii')}
            for ident, (_, data) in sorted(matched.items())]}
        encoded = gzip.compress(json.dumps(payload, separators=(',', ':')).encode(), mtime=0)
        if len(encoded) > base.MAX_FILE:
            raise ValueError('Temporary payload exceeds the existing transport bound')
        payload_sha = base.git('hash-object', '-w', '--stdin', data=encoded).decode().strip()
        raw_request = {'payload_objects': [{'sha': payload_sha, 'sha256': base.digest(encoded)}]}
        raw_restored, raw_blocked, raw_stats = _original_recover(rows, raw_request)
        for row in raw_restored:
            ident = (int(row['bytes']), row['sha256'])
            row['source_kind'] = 'reachable_historical_git_blob'
            row['source_object'] = matched[ident][0]
        restored.extend(raw_restored)
        blocked.extend(raw_blocked)
    stats = dict(archive_stats,
                 reachable_history_blobs=len(blobs),
                 historical_archive_objects=[x['sha'] for x in archives],
                 historical_raw_candidates_hashed=hashed_count,
                 historical_raw_bytes_hashed=hashed_bytes,
                 historical_raw_matching_identities=len(matched),
                 historical_raw_files_restored=len(raw_restored),
                 source_scope='Reachable Git history only; private external sources were not processed by this job.')
    return restored, blocked, stats


def reconcile_history(catalog, state, batch_id, artifact_commit, restored, blocked, stats, source_commit):
    request = base.read_json(base.REC / 'lote_pendiente.json')
    if request.get('scan_reachable_history'):
        state['alcance_ultima_reanudacion'] = 'Historial Git alcanzable y archivos historicos internos; no implica lectura de fuentes privadas externas.'
        state['bloqueos_activos'] = [
            {'componente': 'procesamiento local de las fuentes',
             'detalle': 'En este intento las herramientas de procesamiento devolvieron ClientError tras materializar cinco fuentes; no se verificaron sus bytes internos.'},
            {'componente': 'descarga de la tercera entrega adicional',
             'detalle': 'El conector rechazo 536315323 bytes con HTTP 413: limite de descarga 268435456 bytes. No demuestra corrupcion del original.'},
            {'componente': 'transporte Git directo del entorno',
             'detalle': 'La lectura directa fallo por resolucion DNS. El conector y el flujo remoto de GitHub se usan para esta revision.'}
        ]
    report = _original_reconcile(catalog, state, batch_id, artifact_commit, restored, blocked, stats, source_commit)
    missing = [r for r in catalog['physical_files'] if r['availability'] != 'publicado']
    required = [r for r in missing if r.get('role') != 'dataset_original']
    unique = {(int(r['bytes']), r['sha256']) for r in missing}
    required_unique = {(int(r['bytes']), r['sha256']) for r in required}
    report['missing_classification'] = {
        'catalog_entries': len(missing),
        'unique_identities': len(unique),
        'unique_bytes': sum(size for size, _ in unique),
        'original_dataset_entries_kept_external': len(missing) - len(required),
        'required_entries_excluding_original_datasets': len(required),
        'required_unique_identities': len(required_unique),
        'required_unique_bytes': sum(size for size, _ in required_unique),
        'entries_by_role': dict(sorted(collections.Counter(str(r.get('role', '')) for r in missing).items())),
        'entries_by_run': dict(sorted(collections.Counter(str(r.get('run_id', '')) for r in missing).items())),
        'required_unique_over_100_MiB': sum(size > 100 * 1024 * 1024 for size, _ in required_unique),
        'note': 'An identity absent from reachable Git history is not declared lost; external sources remain necessary.'
    }
    report['local_source_processing_completed'] = False
    report_path = base.REC / f'verificacion_{batch_id}.json'
    base.write_json(report_path, report)
    base.git('add', '-f', '--', str(report_path))
    return report


if __name__ == '__main__':
    base.recover = recover_history
    base.reconcile = reconcile_history
    base.main()

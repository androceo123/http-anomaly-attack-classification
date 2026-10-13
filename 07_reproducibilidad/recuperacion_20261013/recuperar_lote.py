#!/usr/bin/env python3
"""Recuperacion administrativa por identidad; no ejecuta codigo experimental.

Solo restaura bytes que coinciden con el catalogo existente. Nunca carga modelos,
reentrena, sobrescribe un destino diferente ni publica un dataset original.
"""
from __future__ import annotations
import argparse
import base64
import collections
import csv
import datetime as dt
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import urllib.request
import zipfile

REPO = 'androceo123/http-anomaly-attack-classification'
REC = Path('07_reproducibilidad/recuperacion_20261013')
CAT = Path('07_reproducibilidad/catalogo_archivos.json')
MAN = Path('07_reproducibilidad/manifest_repositorio.json')
MAX_FILE = 99 * 1024 * 1024
MAX_BATCH = 512 * 1024 * 1024
MAX_EXPANDED = 1024 * 1024 * 1024
ALLOWED_ROOTS = {'01_documentacion', '02_auditoria', '03_datasets',
                 '04_experimentos', '05_codigo', '06_resultados_consolidados',
                 '90_artefactos_pesados'}
SECRET = re.compile(rb'(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|'
                    rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|'
                    rb'AKIA[0-9A-Z]{16}|sk-proj-[A-Za-z0-9_-]{30,}|'
                    rb'(?:drive|docs)\.google\.com/)')


def git(*args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(['git', *args], input=data, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=180).stdout


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def valid_relative(name: str) -> PurePosixPath:
    if not isinstance(name, str) or not name or '\\' in name or '\0' in name:
        raise ValueError('Invalid path')
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or not p.parts or ':' in p.parts[0]:
        raise ValueError('Unsafe path')
    return p


def target(name: str) -> Path:
    p = valid_relative(name)
    path = Path(*p.parts)
    if path.is_symlink() or not path.resolve().is_relative_to(Path.cwd().resolve()):
        raise ValueError('Path escapes repository')
    return path


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def tracked() -> list[str]:
    return [x.decode('utf-8') for x in git('ls-files', '-z').split(b'\0') if x]


def identities(paths: list[str]):
    result = collections.defaultdict(list)
    for name in paths:
        path = target(name)
        if not path.is_file():
            raise ValueError('Tracked file unavailable: ' + name)
        with path.open('rb') as stream:
            sha = hashlib.file_digest(stream, 'sha256').hexdigest()
        result[(path.stat().st_size, sha)].append(name)
    return result


def read_source_object(sha: str, expected_sha256: str | None = None) -> bytes:
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('Invalid source object')
    try:
        size = int(git('cat-file', '-s', sha))
        if size > MAX_FILE:
            raise ValueError('Source object exceeds transfer bound')
        data = git('cat-file', 'blob', sha)
    except subprocess.CalledProcessError:
        url = f'https://api.github.com/repos/{REPO}/git/blobs/{sha}'
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'artifact-recovery'}
        if os.environ.get('GH_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
            wire = response.read(MAX_FILE * 2 + 1)
        if len(wire) > MAX_FILE * 2:
            raise ValueError('Oversized source response')
        obj = json.loads(wire)
        if obj.get('encoding') != 'base64' or obj.get('sha') != sha:
            raise ValueError('Unexpected source object response')
        data = base64.b64decode(obj['content'])
    if len(data) > MAX_FILE or blob_sha(data) != sha:
        raise ValueError('Source object identity mismatch')
    if expected_sha256 and digest(data) != expected_sha256:
        raise ValueError('Source checksum mismatch')
    return data


def recover(rows, request):
    by_id = collections.defaultdict(list)
    for row in rows:
        p = valid_relative(row['path'])
        if p.parts[0] in ALLOWED_ROOTS and row.get('role') != 'dataset_original':
            by_id[(int(row['bytes']), row['sha256'])].append(row)
    present = identities(tracked())
    restored, blocked = [], []
    seen = set()
    stats = {'members_verified': 0, 'expanded_bytes': 0, 'payload_objects': 0}
    batch_bytes = 0

    def consider(data: bytes, source_sha: str, source_kind: str):
        nonlocal batch_bytes
        ident = (len(data), digest(data))
        if ident in seen:
            return
        seen.add(ident)
        candidates = by_id.get(ident, [])
        if not candidates or present.get(ident):
            return
        if SECRET.search(data):
            blocked.append({'path': candidates[0]['path'], 'reason': 'requires_privacy_review'})
            return
        if len(data) > MAX_FILE or batch_bytes + len(data) > MAX_BATCH:
            blocked.append({'path': candidates[0]['path'], 'reason': 'bounded_transfer_limit'})
            return
        chosen = None
        for row in sorted(candidates, key=lambda x: x['path']):
            path = target(row['path'])
            if not path.exists():
                chosen = row
                break
        if chosen is None:
            blocked.append({'path': candidates[0]['path'], 'reason': 'different_existing_destination'})
            return
        path = target(chosen['path'])
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as output:
            output.write(data)
        if digest(path.read_bytes()) != chosen['sha256']:
            raise ValueError('Written artifact checksum mismatch')
        restored.append({'path': chosen['path'], 'bytes': len(data), 'sha256': ident[1],
                         'git_blob_sha': blob_sha(data), 'run_id': chosen.get('run_id', ''),
                         'role': chosen.get('role', ''), 'source_kind': source_kind,
                         'source_object': source_sha})
        present[ident].append(chosen['path'])
        batch_bytes += len(data)

    def inspect_archive(data: bytes, source_sha: str, depth=0):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                try:
                    valid_relative(info.filename.replace('\\', '/'))
                except ValueError:
                    blocked.append({'path': '[source member]', 'reason': 'unsafe_member_path'})
                    continue
                if stat.S_ISLNK(info.external_attr >> 16) or info.flag_bits & 1:
                    blocked.append({'path': '[source member]', 'reason': 'symlink_or_encrypted_member'})
                    continue
                if info.file_size > MAX_FILE or stats['expanded_bytes'] + info.file_size > MAX_EXPANDED:
                    blocked.append({'path': '[source member]', 'reason': 'bounded_expansion_limit'})
                    continue
                content = archive.read(info)
                if len(content) != info.file_size:
                    raise ValueError('Source member size mismatch')
                stats['members_verified'] += 1
                stats['expanded_bytes'] += len(content)
                if info.filename.lower().endswith('.zip') and depth < 2 and zipfile.is_zipfile(io.BytesIO(content)):
                    inspect_archive(content, source_sha, depth + 1)
                else:
                    consider(content, source_sha, 'historical_git_object')

    for source in request.get('historical_objects', []):
        inspect_archive(read_source_object(source['sha'], source.get('sha256')), source['sha'])
    for source in request.get('payload_objects', []):
        raw = read_source_object(source['sha'], source['sha256'])
        with gzip.GzipFile(fileobj=io.BytesIO(raw)) as stream:
            decoded = stream.read(MAX_EXPANDED + 1)
        if len(decoded) > MAX_EXPANDED:
            raise ValueError('Payload expansion exceeds bound')
        payload = json.loads(decoded)
        if payload.get('schema_version') != 1 or len(payload['files']) > 10000:
            raise ValueError('Invalid payload schema')
        for item in payload['files']:
            data = base64.b64decode(item['base64'], validate=True)
            if len(data) != int(item['bytes']) or digest(data) != item['sha256']:
                raise ValueError('Payload artifact mismatch')
            consider(data, source['sha'], 'verified_content_object')
        stats['payload_objects'] += 1
    return restored, blocked, stats


def write_csv(path: Path, rows: list[dict], fields: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def verify_batch(path: Path, commit: str):
    with path.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        valid_relative(row['path'])
        data = git('show', f'{commit}:{row["path"]}')
        if len(data) != int(row['bytes']) or digest(data) != row['sha256'] or blob_sha(data) != row['git_blob_sha']:
            raise ValueError('Committed artifact verification failed: ' + row['path'])
    return rows


def reconcile(catalog, state, batch_id, artifact_commit, restored, blocked, stats, source_commit):
    paths = tracked()
    present = identities(paths)
    for row in catalog['physical_files']:
        matches = present.get((int(row['bytes']), row['sha256']), [])
        preferred = [row['path'], row.get('repository_path')]
        alias = next((p for p in preferred if p and p in matches), None)
        row['repository_path'] = alias or (sorted(matches)[0] if matches else None)
        row['availability'] = 'publicado' if matches else 'referenciado_no_publicado'
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    catalog['verification_date'] = now
    catalog['verification_source_commit'] = artifact_commit
    write_json(CAT, catalog)
    changed = [str(CAT)]
    for name in ['07_reproducibilidad/artefactos_externos.csv', '06_resultados_consolidados/catalogo_corridas.csv']:
        path = Path(name)
        with path.open(encoding='utf-8', newline='') as stream:
            reader = csv.DictReader(stream)
            fields, data = reader.fieldnames, list(reader)
        for row in data:
            if 'sha256' in row:
                matches = present.get((int(row['bytes']), row['sha256']), [])
                row['availability'] = 'publicado' if matches else 'referenciado_no_publicado'
                if matches and 'artifact_download_url' in row:
                    from urllib.parse import quote
                    alias = sorted(matches)[0]
                    row['artifact_download_url'] = f'https://raw.githubusercontent.com/{REPO}/{artifact_commit}/{quote(alias)}'
                    row['note'] = 'Bytes verificados por SHA-256 en la revision indicada; no es un enlace al dataset.'
            else:
                members = [x for x in catalog['physical_files'] if x.get('run_id') == row['run_id']]
                row['catalogued_artifacts'] = len(members)
                row['published_artifacts'] = sum(x['availability'] == 'publicado' for x in members)
                row['referenced_artifacts'] = len(members) - row['published_artifacts']
        write_csv(path, data, fields)
        changed.append(name)
    report_path = REC / f'verificacion_{batch_id}.json'
    pending_path = REC / f'pendientes_{batch_id}.csv'
    pending = [{k: x.get(k, '') for k in ('path', 'bytes', 'sha256', 'run_id', 'role')}
               for x in catalog['physical_files'] if x['availability'] != 'publicado']
    write_csv(pending_path, pending, ['path', 'bytes', 'sha256', 'run_id', 'role'])
    changed.append(str(pending_path))
    confirmed = state.setdefault('lotes_confirmados', [])
    if not any(x['lote'] == batch_id for x in confirmed):
        confirmed.append({'lote': batch_id, 'commit': artifact_commit,
                          'artefactos': len(restored), 'bytes': sum(int(x['bytes']) for x in restored),
                          'manifest': str(REC / f'lote_{batch_id}.csv'),
                          'verificacion': 'Tamano, SHA-256 e identidad Git recalculados sobre los objetos del commit.',
                          'reporte': str(report_path)})
    all_rows = {}
    for manifest in sorted(REC.glob('lote_*.csv')):
        for row in verify_batch(manifest, artifact_commit):
            all_rows[row['path']] = row
    state.update({'estado': 'recuperacion_parcial_publicada',
                  'ultimo_commit_artefactos_verificado': artifact_commit,
                  'archivos_publicados_en_esta_recuperacion': len(all_rows),
                  'bytes_publicados_en_esta_recuperacion': sum(int(x['bytes']) for x in all_rows.values()),
                  'catalogos_generales_reconciliados': True,
                  'catalogos_reconciliados': [str(CAT), '07_reproducibilidad/artefactos_externos.csv', '06_resultados_consolidados/catalogo_corridas.csv', str(MAN)],
                  'inventario_historico_preservado': True,
                  'publicacion_completa': not pending, 'proceso_en_segundo_plano': False,
                  'ultima_verificacion': str(report_path), 'pendientes_actuales': str(pending_path),
                  'fecha_verificacion': now,
                  'siguiente_paso': 'Contrastar pendientes contra las fuentes restantes. Un archivo ausente de estas fuentes no se declara perdido; no se alteran ni se ocultan identidades historicas.'})
    by_path = {r['path']: r for r in catalog['physical_files']}
    exp = [r for p, r in all_rows.items() if by_path.get(p, {}).get('run_id')]
    state['artefactos_experimentales_publicados_en_esta_recuperacion'] = len(exp)
    state['bytes_experimentales_publicados'] = sum(int(x['bytes']) for x in exp)
    write_json(REC / 'estado.json', state)
    changed.append(str(REC / 'estado.json'))
    git('add', '-f', '--', *changed)
    old_manifest = read_json(MAN)
    excluded = set(old_manifest.get('excluded_paths', [])) | {str(MAN), str(report_path)}
    excluded.update(str(x) for x in REC.glob('verificacion_*.json'))
    files = []
    for name in sorted(tracked()):
        if name in excluded:
            continue
        path = target(name)
        files.append({'path': name, 'bytes': path.stat().st_size, 'sha256': digest(path.read_bytes())})
    current_manifest = dict(old_manifest, revision_date=now[:10], base_commit=artifact_commit,
                            scope='Archivos publicados tras la recuperacion verificada; no implica que todos los artefactos historicos esten disponibles.',
                            excluded_paths=sorted(excluded), files=files)
    write_json(MAN, current_manifest)
    failures = []
    for row in files:
        path = target(row['path'])
        if path.stat().st_size != row['bytes'] or digest(path.read_bytes()) != row['sha256']:
            failures.append(row['path'])
    report = {'schema_version': 1, 'verified_at': now, 'source_commit': source_commit,
              'artifact_commit': artifact_commit, 'batch': batch_id,
              'new_files': len(restored), 'new_bytes': sum(int(x['bytes']) for x in restored),
              'total_recovered_files': len(all_rows),
              'checked': len(files), 'passed': len(files) - len(failures), 'failures': failures,
              'catalogued_entries': len(catalog['physical_files']),
              'available_catalogued_entries': len(catalog['physical_files']) - len(pending),
              'unavailable_catalogued_entries': len(pending),
              'catalog_count_is_not_unique_file_count': True,
              'source_inspection': stats, 'blocked_in_batch': blocked,
              'training_executed': False, 'models_deserialized': False,
              'original_datasets_published': False, 'complete_historical_recovery': not pending,
              'scope': 'Disponibilidad por identidad en esta revision. Las fuentes no inspeccionadas pueden contener mas faltantes.'}
    write_json(report_path, report)
    if failures:
        raise ValueError('Repository manifest verification failed')
    git('add', '-f', '--', str(MAN), str(report_path))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Publish a validated batch to the authorized repository')
    args = parser.parse_args()
    if not args.apply or os.environ.get('GITHUB_REPOSITORY') != REPO or os.environ.get('GITHUB_REF') != 'refs/heads/main':
        parser.error('Requires explicit --apply in the authorized main workflow')
    initial = git('rev-parse', 'HEAD').decode().strip()
    if initial != os.environ.get('GITHUB_SHA'):
        raise ValueError('Checkout does not match triggering commit')
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    if remote != initial:
        raise ValueError('main changed; create a fresh request rather than overwrite it')
    request = read_json(REC / 'lote_pendiente.json')
    batch_id = request['batch_id']
    if not re.fullmatch(r'\d{3,6}', batch_id):
        raise ValueError('Invalid batch identifier')
    if request.get('expected_parent') and git('rev-parse', 'HEAD^').decode().strip() != request['expected_parent']:
        raise ValueError('Request parent mismatch')
    catalog, state = read_json(CAT), read_json(REC / 'estado.json')
    manifest = REC / f'lote_{batch_id}.csv'
    git('config', 'user.name', 'github-actions[bot]')
    git('config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    if manifest.exists():
        restored = verify_batch(manifest, initial)
        artifact_commit = git('log', '-1', '--format=%H', '--', str(manifest)).decode().strip()
        blocked, stats = [], {'resume': True}
    else:
        restored, blocked, stats = recover(catalog['physical_files'], request)
        write_csv(manifest, restored, ['path', 'bytes', 'sha256', 'git_blob_sha', 'run_id', 'role', 'source_kind', 'source_object'])
        git('add', '-f', '--', str(manifest), *[x['path'] for x in restored])
        git('commit', '-m', f'Recover verified artifact batch {batch_id} ({len(restored)} files)')
        artifact_commit = git('rev-parse', 'HEAD').decode().strip()
        verify_batch(manifest, artifact_commit)
    report = reconcile(catalog, state, batch_id, artifact_commit, restored, blocked, stats, initial)
    git('commit', '-m', f'Checkpoint batch {batch_id}: reconcile catalog and verify published bytes')
    checkpoint_commit = git('rev-parse', 'HEAD').decode().strip()
    remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
    if remote != initial:
        raise ValueError('Concurrent change detected before publication')
    git('push', '--porcelain', 'origin', 'HEAD:refs/heads/main')
    if git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] != checkpoint_commit:
        raise ValueError('Published branch readback mismatch')
    print('ARTIFACT_COMMIT=' + artifact_commit)
    print('CHECKPOINT_COMMIT=' + checkpoint_commit)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

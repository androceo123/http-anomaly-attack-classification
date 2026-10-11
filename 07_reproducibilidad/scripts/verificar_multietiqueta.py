#!/usr/bin/env python3
"""Auditoría L1/L2 de los resultados experimentales HTTP.

Lee CSV/JSON originales, recalcula métricas desde predicciones ya guardadas y
reconstruye particiones con el procedimiento documentado y las semillas guardadas.
Las particiones reconstruidas son productos de esta auditoría, no archivos
históricos encontrados. La identidad se contrasta con índices test conservados.

Resuelve cada fuente y su SHA-256 mediante inventario_archivos.json. Los archivos
referenciados pueden estar dentro de --root o en --external-root.
L1 lee las etiquetas del CSV raw por bloques: no depende de NPY temporales.

Uso desde la raíz del repositorio:
  python 07_reproducibilidad/scripts/verificar_multietiqueta.py \
      --root . --output ./verificaciones_nuevas

Python >= 3.11 con las versiones de requisitos, numpy, pandas y scikit-learn. No requiere XGBoost, joblib,
pyarrow ni GPU. No carga modelos: solo verifica sus bytes, hash y tamaño.
--help funciona con la biblioteca estándar, sin leer datos ni crear salidas.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path, PurePosixPath
import re
import sys
from datetime import datetime, timezone

DEFAULT_INVENTORY = Path("02_auditoria/integridad_y_procedencia/inventario_archivos.json")


class AuditInputError(RuntimeError):
    """Falta una fuente o no coincide con el inventario."""


def load_runtime():
    # Imports diferidos para permitir --help sin dependencias científicas.
    global np, pd, sklearn, average_precision_score, roc_auc_score, train_test_split
    try:
        import numpy as np
        import pandas as pd
        import sklearn
        from sklearn.metrics import average_precision_score, roc_auc_score
        from sklearn.model_selection import train_test_split
    except ImportError as exc:
        raise AuditInputError(
            "Faltan dependencias: instalar numpy, pandas y scikit-learn "
            "en el intérprete que ejecuta este script."
        ) from exc


class InventoryResolver:
    """Resuelve rutas organizadas y alias de idéntico SHA sin usar rutas locales antiguas."""

    def __init__(self, root, inventory_path, external_roots=()):
        self.root = Path(root).resolve()
        self.inventory_path = Path(inventory_path).resolve()
        self.external_roots = [Path(p).resolve() for p in external_roots]
        if not self.inventory_path.is_file():
            raise AuditInputError(f"No se encuentra el inventario: {self.inventory_path}")
        inventory = read_json(self.inventory_path)
        self.entries = inventory.get("entries") if isinstance(inventory, dict) else None
        if not isinstance(self.entries, list):
            raise AuditInputError("El inventario debe contener una lista 'entries'.")
        self.by_sha = {}
        for entry in self.entries:
            self.by_sha.setdefault(entry.get("sha256"), []).append(entry)
        self.cache = {}
        self.used = {}

    def entry(self, *, name, source_code=None, run_id=None, dataset=None):
        matches = [r for r in self.entries
                   if PurePosixPath(str(r.get("original_path", ""))).name == name
                   and (source_code is None or r.get("source_code") == source_code)
                   and (run_id is None or r.get("run_id") == run_id)
                   and (dataset is None or r.get("dataset") == dataset)]
        if not matches:
            raise AuditInputError(
                f"El inventario no identifica {name!r} "
                f"(source_code={source_code}, run_id={run_id}, dataset={dataset})."
            )
        hashes = {r.get("sha256") for r in matches}
        if len(hashes) != 1:
            raise AuditInputError(f"Identidad ambigua para {name}: existen versiones con distintos SHA-256.")
        return matches[0]

    def candidate_paths(self, entry):
        # organized_path refleja también consolidación de duplicados. logical_path
        # permite ubicar artefactos conservados fuera del árbol del repositorio.
        for field in ("organized_path", "logical_path", "canonical_path"):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                continue
            rel = PurePosixPath(value)
            if rel.is_absolute() or ".." in rel.parts:
                raise AuditInputError(f"Ruta de inventario no relativa al proyecto: {value}")
            if "://" in value:
                continue
            suffix = Path(*rel.parts)
            yield self.root / suffix
            for external in self.external_roots:
                yield external / suffix

    def resolve(self, entry):
        key = (entry.get("source_code"), entry.get("original_path"))
        if key in self.used:
            return Path(self.used[key]["resolved_path"])
        expected = str(entry.get("sha256", "")).lower()
        if re.fullmatch(r"[0-9a-f]{64}", expected) is None:
            raise AuditInputError(f"SHA-256 ausente o inválido: {key}")
        # Si una copia fue consolidada, solo se aceptan alias de idénticos bytes.
        peers = [entry] + [x for x in self.by_sha.get(expected, []) if x is not entry]
        candidates = []
        for peer in peers:
            for candidate in self.candidate_paths(peer):
                if candidate not in candidates:
                    candidates.append(candidate)
        path = next((p for p in candidates if p.is_file()), None)
        if path is None:
            shown = "\n  ".join(str(p) for p in candidates[:8])
            raise AuditInputError(
                f"Falta {entry.get('source_code')}:{entry.get('original_path')}. "
                f"SHA-256 esperado: {expected}.\n  {shown}\n"
                "Proporcionar el artefacto identificado por su hash e indicar --external-root si está en otro almacenamiento."
            )
        path = path.resolve()
        size = path.stat().st_size
        if "bytes" in entry and size != int(entry["bytes"]):
            raise AuditInputError(f"Tamaño distinto al inventario: {path}; {size} != {entry['bytes']}")
        if path not in self.cache:
            self.cache[path] = sha256(path)
        actual = self.cache[path]
        if actual != expected:
            raise AuditInputError(f"SHA-256 distinto al inventario: {path}; {actual} != {expected}")
        self.used[key] = {
            "source_code": entry.get("source_code"), "original_path": entry.get("original_path"),
            "run_id": entry.get("run_id"), "organized_path": entry.get("organized_path"),
            "logical_path": entry.get("logical_path"), "resolved_path": str(path),
            "bytes_actual": size, "sha256_expected": expected, "sha256_actual": actual,
            "matches_inventory": True,
        }
        return path

    def find(self, **query):
        return self.resolve(self.entry(**query))

    def known_hash(self, path):
        return self.cache[Path(path).resolve()]


class RunArtifacts:
    """Acceso por nombre lógico; cada archivo puede vivir en una carpeta diferente."""

    def __init__(self, resolver, run):
        self.resolver, self.run = resolver, run

    def __truediv__(self, name):
        return self.resolver.find(name=name, source_code="S06", run_id=self.run)

    def known_hash(self, name):
        return self.resolver.known_hash(self / name)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_name(name):
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")


def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def div(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return np.divide(a, b, out=np.zeros_like(a, dtype=float), where=b != 0)


def choose_stratify(y, labels, fraction):
    """Reimplementación de la regla leída, sin importar el script experimental."""
    k = y.shape[1]
    codes = (y.astype(np.uint32) * (1 << np.arange(k, dtype=np.uint32))).sum(axis=1)
    lookup = []
    for code in range(1 << k):
        chosen = [labels[i] for i in range(k) if code & (1 << i)]
        lookup.append("NORMAL" if not chosen else "|".join(chosen) if len(chosen) <= 3
                      else "MULTI_" + str(len(chosen)) + "__" + "|".join(chosen[:3]))
    signature = np.array(lookup, dtype=object)[codes]

    def valid(keys):
        counts = pd.Series(keys).value_counts(dropna=False)
        nt = int(math.ceil(len(keys) * fraction))
        return not counts.empty and int(counts.min()) >= 2 and nt >= len(counts) and len(keys) - nt >= len(counts)

    if valid(signature):
        return signature, "labelset_signature"
    primary = np.array(labels, dtype=object)[np.argmax(y, axis=1)]
    primary[y.sum(axis=1) == 0] = "NORMAL"
    if valid(primary):
        return primary, "primary_label"
    binary = np.where(y.sum(axis=1) > 0, "ATTACK", "NORMAL")
    if valid(binary):
        return binary, "binary_attack_normal"
    return None, "none"


def divide(indices, y, labels, fraction, seed):
    strat, method = choose_stratify(y[indices], labels, fraction)
    a, b = train_test_split(np.arange(len(indices)), test_size=fraction,
                            random_state=seed, shuffle=True, stratify=strat)
    return indices[a], indices[b], method


def verify_predictions(run, folder, out_dir):
    cfg = read_json(folder / "run_config.json")
    expected = read_json(folder / "test_metrics_multilabel.json")
    labels = cfg["target_labels"]
    stems = [safe_name(x) for x in labels]
    cols = ["row_index", "sample_id"]
    if run == "L2":
        cols += ["request_fingerprint", "duplicate_group_size"]
    cols += [f"{prefix}_{x}" for x in stems for prefix in ["true", "pred", "score"]]
    frame = pd.read_csv(folder / "test_predictions.csv", usecols=cols,
                        dtype={"sample_id": str, "request_fingerprint": str},
                        keep_default_na=False, float_precision="round_trip")
    y = frame[[f"true_{x}" for x in stems]].to_numpy(dtype=np.int8)
    p = frame[[f"pred_{x}" for x in stems]].to_numpy(dtype=np.int8)
    scores = frame[[f"score_{x}" for x in stems]].to_numpy(dtype=float)
    if not (np.isin(y, [0, 1]).all() and np.isin(p, [0, 1]).all()):
        raise ValueError(f"{run}: etiquetas guardadas fuera de 0/1")
    tp = ((y == 1) & (p == 1)).sum(axis=0)
    fp = ((y == 0) & (p == 1)).sum(axis=0)
    fn = ((y == 1) & (p == 0)).sum(axis=0)
    tn = ((y == 0) & (p == 0)).sum(axis=0)
    precision = div(tp, tp + fp)
    recall = div(tp, tp + fn)
    f1 = div(2 * tp, 2 * tp + fp + fn)
    exact = np.all(y == p, axis=1)
    at = y.sum(axis=1) > 0
    ap = p.sum(axis=1) > 0
    metrics = {
        "rows": len(frame), "unit": "fila_evento" if run == "L1" else "grupo_por_huella",
        "exact_match_accuracy": float(exact.mean()),
        "exact_match_count": int(exact.sum()),
        "hamming_loss": float((y != p).mean()),
        "wrong_label_decisions": int((y != p).sum()),
        "f1_micro": float(div(2 * tp.sum(), 2 * tp.sum() + fp.sum() + fn.sum())),
        "f1_macro": float(f1.mean()),
        "f1_weighted": float(np.average(f1, weights=y.sum(axis=0))),
        "precision_micro": float(div(tp.sum(), tp.sum() + fp.sum())),
        "recall_micro": float(div(tp.sum(), tp.sum() + fn.sum())),
        "jaccard_micro": float(div(tp.sum(), tp.sum() + fp.sum() + fn.sum())),
        "pr_auc_macro": float(average_precision_score(y, scores, average="macro")),
        "roc_auc_macro": float(roc_auc_score(y, scores, average="macro")),
        "attack_only_exact_match_count": int(exact[at].sum()),
        "attack_only_support": int(at.sum()),
        "attack_only_exact_match": float(exact[at].mean()),
        "normal_support": int((~at).sum()),
        "normal_recall": float((~ap[~at]).mean()),
        "normal_99_goal_met": bool((~ap[~at]).mean() >= 0.99),
        "binary_confusion": {"tn": int((~at & ~ap).sum()), "fp": int((~at & ap).sum()),
                             "fn": int((at & ~ap).sum()), "tp": int((at & ap).sum())},
        "labels_meeting_f1_85": int((f1 >= 0.85).sum()),
        "duplicate_row_indices": int(frame.row_index.duplicated().sum()),
        "duplicate_sample_ids": int(frame.sample_id.duplicated().sum()),
    }
    checks = []
    for key, value in metrics.items():
        if key in expected and isinstance(value, (int, float)):
            delta = float(value) - float(expected[key])
            checks.append({"check": key, "recalculated": value, "saved": expected[key],
                           "delta": delta, "match": abs(delta) <= 1e-12})
    for key, value in metrics["binary_confusion"].items():
        checks.append({"check": f"binary_{key}", "recalculated": value,
                       "saved": expected["binary_normal_vs_attack"][key],
                       "match": value == expected["binary_normal_vs_attack"][key]})
    perlabel = pd.DataFrame({"label": labels, "tn": tn, "fp": fp, "fn": fn, "tp": tp,
                            "support": y.sum(axis=0), "precision": precision,
                            "recall": recall, "f1": f1})
    saved_per = pd.read_csv(folder / "per_label_metrics.csv").set_index("label").loc[labels]
    perlabel["saved_counts_match"] = np.all(saved_per[["tn", "fp", "fn", "tp"]].to_numpy()
                                             == perlabel[["tn", "fp", "fn", "tp"]].to_numpy(), axis=1)
    perlabel["saved_f1_match"] = np.isclose(saved_per.f1.to_numpy(), f1, atol=1e-12, rtol=0)
    perlabel.to_csv(out_dir / f"{run}_metricas_por_etiqueta_recalculadas.csv", index=False)
    whole_name = "metrics_multilabel_harvard_xgboost_none_fixed30.json" if run == "L1" else "metrics_multilabel_xgb_request90.json"
    whole = read_json(folder / whole_name)
    threshold = whole["thresholds"]
    if isinstance(threshold, dict):
        tau = np.array([threshold[label] for label in labels], dtype=float)
    else:
        tau = np.array(threshold, dtype=float)
    # El código original compara float32. La lectura round_trip conserva el decimal
    # guardado; el parser por defecto puede desplazar valores iguales al umbral.
    thresholds_match = int(np.not_equal(scores.astype(np.float32) >= tau.astype(np.float32), p).sum()) == 0
    latency = pd.read_csv(folder / "operational_latency_online_ms.csv").iloc[:, 0].to_numpy(dtype=float)
    oper = read_json(folder / "operational_metrics.json")
    operational = {"unit": metrics["unit"], "sample_size": len(latency), "sample_matches_saved_count": len(latency) == oper["measured_rows"],
                   "percentile_method": "numpy.percentile default linear", "recorded_online_seconds": oper["t_apply_pipeline_online_seconds"],
                   "sum_individual_seconds": float(latency.sum() / 1000),
                   "model_size_bytes_actual": (folder / ("model_multilabel_harvard_xgboost_none_fixed30.joblib" if run == "L1" else "model_multilabel_xgb_request90.joblib")).stat().st_size}
    for q in [50, 95, 99]:
        value = float(np.percentile(latency, q))
        key = f"latency_ms_pipeline_online_p{q}"
        operational[key] = {"recalculated": value, "saved": oper[key], "match": abs(value-oper[key]) <= 1e-10}
    for phase in ["pipeline_online", "pipeline_batch", "inference_batch"]:
        value = len(latency) / oper[f"t_apply_{phase}_seconds"]
        key = f"throughput_req_s_{phase}"
        operational[key] = {"recalculated": value, "saved": oper[key], "match": abs(value-oper[key]) <= 1e-8}
    checks.append({"check":"all_per_label_counts", "match": bool(perlabel.saved_counts_match.all())})
    checks.append({"check":"all_per_label_f1", "match": bool(perlabel.saved_f1_match.all())})
    checks.append({"check":"predictions_reproduced_by_saved_scores_and_thresholds", "match": thresholds_match})
    if run == "L2":
        metrics["duplicate_test_fingerprints"] = int(frame.request_fingerprint.duplicated().sum())
    return cfg, frame, y, {"metrics_recalculated": metrics, "checks": checks,
                           "prediction_reconstruction": {"csv_float_parser":"round_trip", "score_threshold_dtype":"float32", "operator":">="},
                           "operational": operational, "source_prediction_sha256": folder.known_hash("test_predictions.csv")}


def reconstruct(run, cfg, frame, test_y, y, sample_ids, fingerprints=None, *, out_dir):
    args = cfg["args"]
    labels = cfg["target_labels"]
    dev, test, test_method = divide(np.arange(len(y)), y, labels, args["test_size"], args["seed"])
    train, valid, valid_method = divide(dev, y, labels, args["valid_size"], args["seed"] + 1)
    methods = {"test": test_method, "validation": valid_method}
    if run == "L2":
        tune, calibration, cal_method = divide(valid, y, labels, args["calibration_share"], args["seed"] + 2)
        partitions = {"train": train, "tune": tune, "calibration": calibration, "test": test}
        methods["calibration"] = cal_method
    else:
        partitions = {"train": train, "valid": valid, "test": test}
    saved_test = frame.row_index.to_numpy(dtype=np.int64)
    checks = {"test_indices_same_order": bool(np.array_equal(test, saved_test)),
              "test_indices_same_set": bool(np.array_equal(np.sort(test), np.sort(saved_test))),
              "test_labels_match_processed": bool(np.array_equal(y[saved_test], test_y)),
              "test_sample_ids_match": bool(np.array_equal(np.asarray(sample_ids)[saved_test].astype(str), frame.sample_id.to_numpy(dtype=str))),
              "partitions_cover_all_rows": len(set(np.concatenate(list(partitions.values())).tolist())) == len(y)}
    counts = {}
    for name, ids in partitions.items():
        actual = y[ids].sum(axis=0).astype(int)
        expected = cfg["split_info"][name + "_positive_counts"]
        counts[name] = {"rows": len(ids), "expected_rows": cfg["split_info"][name + "_rows"],
                        "all_positive_counts_match": all(actual[i] == expected[lab] for i, lab in enumerate(labels)),
                        "positive_counts": {lab:int(actual[i]) for i,lab in enumerate(labels)},
                        "sorted_index_sha256": hashlib.sha256(np.sort(ids).astype("<i8").tobytes()).hexdigest()}
    pairs = []
    for a, b in itertools.combinations(partitions, 2):
        row = {"partition_a": a, "partition_b": b,
               "shared_indices": int(np.intersect1d(partitions[a], partitions[b]).size)}
        if fingerprints is not None:
            row["shared_fingerprints"] = len(set(fingerprints[partitions[a]]) & set(fingerprints[partitions[b]]))
        pairs.append(row)
    pd.DataFrame(pairs).to_csv(out_dir / f"{run}_intersecciones_recalculadas.csv", index=False)
    np.savez_compressed(out_dir / f"{run}_particiones_reconstruidas.npz", **partitions)
    if fingerprints is not None:
        checks["all_processed_fingerprints_unique"] = len(set(fingerprints)) == len(fingerprints)
        checks["test_fingerprints_match_processed"] = bool(np.array_equal(fingerprints[saved_test], frame.request_fingerprint.to_numpy(dtype=str)))
    return {"origin": "reconstructed_in_this_audit_not_historical_split_files", "methods": methods,
            "checks": checks, "counts": counts, "intersections": pairs,
            "qualification": "Agreement of test index order, sample IDs, labels and every saved split support is checked. Historical training memberships are reconstructed; no original full partition lists were found."}


def read_raw_label_matrix(resolver, labels):
    """Extrae solo las doce CAPEC en orden original, sin Parquet ni NPY auxiliares."""
    path = resolver.find(name="data_capec_multilabel.csv", source_code="S11")
    columns = list(pd.read_csv(path, nrows=0, keep_default_na=False).columns)
    by_code = {}
    for column in columns:
        match = re.match(r"(\d+)\s*-", column)
        if match:
            code = int(match.group(1))
            if code in by_code:
                raise AuditInputError(f"Código CAPEC duplicado en la cabecera raw: {code}")
            by_code[code] = column
    wanted = []
    for label in labels:
        match = re.search(r"CAPEC-(\d+)", label)
        if match is None or int(match.group(1)) not in by_code:
            raise AuditInputError(f"No se encuentra columna raw de {label!r}.")
        wanted.append(by_code[int(match.group(1))])
    chunks = []
    # usecols limita la carga a las etiquetas; no se guardan ni imprimen peticiones.
    for chunk in pd.read_csv(path, usecols=wanted, dtype="uint8", keep_default_na=False,
                             chunksize=100_000):
        values = chunk[wanted].to_numpy(dtype=np.int8)
        if not np.isin(values, [0, 1]).all():
            raise AuditInputError("Las etiquetas raw contienen valores distintos de 0/1.")
        chunks.append(values)
    if not chunks:
        raise AuditInputError("El CSV raw no tiene filas.")
    y = np.concatenate(chunks, axis=0)
    return y, {"source_code": "S11", "original_filename": "data_capec_multilabel.csv",
               "resolved_path": str(path), "sha256": resolver.known_hash(path),
               "rows": len(y), "selected_columns_in_order": wanted,
               "method": "pandas chunks of 100000 rows; selected target columns; original row order"}


def passed(evidence):
    """Agrupa las comprobaciones sin confundir métricas logradas con metas deseadas."""
    checks = [bool(c["match"]) for c in evidence["checks"]]
    oper = evidence["operational"]
    checks.append(bool(oper["sample_matches_saved_count"]))
    checks.extend(bool(v["match"]) for v in oper.values() if isinstance(v, dict) and "match" in v)
    parts = evidence["partitions"]
    checks.extend(bool(v) for v in parts["checks"].values())
    checks.extend(c["rows"] == c["expected_rows"] and bool(c["all_positive_counts_match"])
                  for c in parts["counts"].values())
    checks.extend(p["shared_indices"] == 0 and p.get("shared_fingerprints", 0) == 0
                  for p in parts["intersections"])
    if "deduplication_internal_reconciliation" in evidence:
        d = evidence["deduplication_internal_reconciliation"]
        checks.extend([d["recorded_counts_match"], d["duplicate_csv_fingerprints_and_sizes_match_processed"]])
    if "schema_hash_recomputed" in evidence:
        checks.append(evidence["schema_hash_recomputed"]["matches_run_config"])
    return all(checks)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=("Recalcula métricas L1/L2 desde predicciones guardadas y reconstruye "
                     "sus particiones. No carga modelos ni ejecuta entrenamiento."),
        epilog=("Requiere Python >= 3.11 con las versiones de requisitos, numpy, pandas y scikit-learn. "
                "Necesita los CSV de predicciones y modelos finales de las corridas; "
                "los modelos se leen solo como bytes para verificar integridad. "
                "El resultado identifica las particiones como reconstruidas."),
    )
    parser.add_argument("--root", required=True, type=Path,
                        help="Raíz del repositorio de código, documentación y evidencia experimental.")
    parser.add_argument("--output", required=True, type=Path,
                        help="Carpeta nueva o vacía para verificaciones derivadas; relativa al directorio actual.")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY,
                        help="Inventario JSON; ruta relativa a --root o absoluta (default: %(default)s).")
    parser.add_argument("--external-root", action="append", default=[], type=Path,
                        help=("Almacenamiento de artefactos experimentales adicional al repositorio. "
                              "Conserva las rutas relativas del inventario; repetible."))
    return parser.parse_args(argv)


def main(argv=None):
    cli = parse_args(argv)
    root, out_dir = cli.root.resolve(), cli.output.resolve()
    if not root.is_dir():
        raise AuditInputError(f"No existe --root: {root}")
    if out_dir.exists() and (not out_dir.is_dir() or any(out_dir.iterdir())):
        raise AuditInputError("--output debe ser una carpeta nueva o vacía para preservar verificaciones anteriores.")
    inventory_path = cli.inventory if cli.inventory.is_absolute() else root / cli.inventory
    resolver = InventoryResolver(root, inventory_path, cli.external_root)
    load_runtime()
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"created_at_utc": datetime.now(timezone.utc).isoformat(),
              "operation": "Read-only recomputation from saved predictions and deterministic split reconstruction. No model unpickling, no experiment script execution, no training.",
              "root": str(root), "output": str(out_dir),
              "inventory": str(resolver.inventory_path), "inventory_sha256": sha256(resolver.inventory_path),
              "external_roots": [str(p) for p in resolver.external_roots],
              "environment": {"python":sys.version, "numpy":np.__version__, "pandas":pd.__version__, "sklearn":sklearn.__version__}, "runs": {}}
    for run in ("L1", "L2"):
        folder = RunArtifacts(resolver, run)
        print(f"{run}: verificando predicciones y latencias", flush=True)
        cfg, frame, test_y, evidence = verify_predictions(run, folder, out_dir)
        evidence["source_selector"] = {"source_code": "S06", "run_id": run,
                                      "resolution": "organized_path/logical_path and exact-hash aliases in inventory"}
        evidence["run_config_sha256"] = folder.known_hash("run_config.json")
        if run == "L2":
            stems = [safe_name(x) for x in cfg["target_labels"]]
            cols = ["sample_id", "request_fingerprint", "duplicate_group_size"] + ["target__"+x for x in stems]
            print("L2: leyendo columnas de identidad y etiquetas de processed_request90", flush=True)
            processed = pd.read_csv(folder / "processed_request90_multilabel.csv", usecols=cols,
                                    dtype={"sample_id":str, "request_fingerprint":str}, keep_default_na=False)
            y = processed[["target__" + x for x in stems]].to_numpy(dtype=np.int8)
            fp = processed.request_fingerprint.to_numpy(dtype=str)
            evidence["partitions"] = reconstruct(run, cfg, frame, test_y, y, processed.sample_id.to_numpy(), fp,
                                                  out_dir=out_dir)
            dups = pd.read_csv(folder / "request_duplicate_groups.csv", keep_default_na=False)
            sizes = processed.duplicate_group_size.to_numpy(dtype=np.int64)
            observed = {"groups":len(processed), "valid_original_rows_by_group_size_sum":int(sizes.sum()),
                        "duplicate_groups":int((sizes > 1).sum()), "duplicate_rows_beyond_first":int((sizes-1).sum()),
                        "max_duplicate_group_size":int(sizes.max()), "normal_groups":int((y.sum(axis=1)==0).sum()),
                        "attack_groups":int((y.sum(axis=1)>0).sum()), "duplicate_audit_csv_rows":len(dups)}
            for c in ["label_disagreement", "normal_attack_conflict_after_or"]:
                observed[c + "_count"] = int(dups[c].astype(str).str.lower().eq("true").sum())
            recorded = read_json(folder / "request_deduplication_audit.json")
            observed["recorded_counts_match"] = (
                observed["groups"] == recorded["unique_request_fingerprints"] and
                observed["valid_original_rows_by_group_size_sum"] == recorded["rows_before_deduplication"] and
                observed["duplicate_groups"] == recorded["duplicate_groups"] and
                observed["duplicate_rows_beyond_first"] == recorded["duplicate_rows_beyond_first"] and
                observed["max_duplicate_group_size"] == recorded["max_duplicate_group_size"] and
                observed["label_disagreement_count"] == recorded["groups_with_any_label_disagreement"] and
                observed["normal_attack_conflict_after_or_count"] == recorded["groups_with_normal_attack_conflict_after_or"])
            subset = processed.loc[sizes > 1, ["request_fingerprint","duplicate_group_size"]].set_index("request_fingerprint")
            da = dups.set_index("request_fingerprint")
            observed["duplicate_csv_fingerprints_and_sizes_match_processed"] = (set(subset.index) == set(da.index) and bool(np.array_equal(subset.duplicate_group_size.to_numpy(), da.loc[subset.index].group_size.to_numpy())))
            evidence["deduplication_internal_reconciliation"] = observed
            trials = pd.read_csv(folder / "xgb_tuning_trials_by_label.csv")
            selected = trials[trials.selected.astype(str).str.lower().eq("true")]
            evidence["tuning_trials"] = {"count":len(trials), "by_label":trials.groupby("label").size().to_dict(),
                                          "status_counts":trials.status.value_counts().to_dict(),
                                          "selected_count":len(selected), "selected_by_label":selected.groupby("label").size().to_dict()}
            schema_hash = hashlib.sha256((cfg["feature_schema_version"]+"\n"+"\n".join(cfg["features"])).encode()).hexdigest()
            evidence["schema_hash_recomputed"] = {"sha256":schema_hash,"matches_run_config":schema_hash==cfg["feature_schema_sha256"]}
            del processed, y, fp
        else:
            print("L1: leyendo etiquetas del CSV raw por bloques", flush=True)
            y, raw_source = read_raw_label_matrix(resolver, cfg["target_labels"])
            evidence["partitions"] = reconstruct(run, cfg, frame, test_y, y, np.arange(len(y)), out_dir=out_dir)
            evidence["raw_label_source"] = raw_source
            del y
        evidence["verification_passed"] = passed(evidence)
        report["runs"][run] = evidence
        save_json(out_dir / f"{run}_verificacion.json", evidence)
        print(run, json.dumps({"metrics":evidence["metrics_recalculated"],"all_metric_checks_match":all(c["match"] for c in evidence["checks"]),"partitions_checks":evidence.get("partitions",{}).get("checks")}, ensure_ascii=False), flush=True)
        del cfg, frame, test_y
    report["sources_verified_against_inventory"] = list(resolver.used.values())
    report["verification_passed"] = all(e["verification_passed"] for e in report["runs"].values())
    save_json(out_dir / "fuentes_resueltas_y_verificadas.json", list(resolver.used.values()))
    save_json(out_dir / "resumen_verificacion_multietiqueta.json", report)
    print("Guardado", out_dir / "resumen_verificacion_multietiqueta.json", flush=True)
    return 0 if report["verification_passed"] else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AuditInputError, OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

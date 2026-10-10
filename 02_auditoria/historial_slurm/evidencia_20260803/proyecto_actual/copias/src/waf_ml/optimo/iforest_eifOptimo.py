#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import random
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_recall_fscore_support,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, StratifiedShuffleSplit, train_test_split
from sklearn.preprocessing import StandardScaler

try:
    import psutil
except Exception:  # pragma: no cover
    psutil = None

try:
    import cupy as cp
except Exception as e:  # pragma: no cover
    cp = None
    _CUPY_IMPORT_ERROR = repr(e)
else:
    _CUPY_IMPORT_ERROR = None


def now() -> float:
    return time.perf_counter()


def ensure_parent(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def json_dump(obj: Any, path: str | Path) -> None:
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=_json_default)


def _json_default(o: Any) -> Any:
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def get_gpu_info() -> Dict[str, Any]:
    info: Dict[str, Any] = {"cupy_import_error": _CUPY_IMPORT_ERROR}
    if cp is not None:
        try:
            n = int(cp.cuda.runtime.getDeviceCount())
            info["cupy_cuda_device_count"] = n
            if n > 0:
                props = cp.cuda.runtime.getDeviceProperties(0)
                name = props.get("name", b"")
                info["cupy_cuda_device_name"] = name.decode() if isinstance(name, bytes) else str(name)
        except Exception as e:
            info["cupy_cuda_error"] = repr(e)
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
            text=True,
            stderr=subprocess.STDOUT,
            timeout=10,
        ).strip()
        info["nvidia_smi"] = out
    except Exception as e:
        info["nvidia_smi_error"] = repr(e)
    return info


def require_gpu() -> None:
    if cp is None:
        raise RuntimeError(f"CuPy no importó; no se puede usar GPU. Error: {_CUPY_IMPORT_ERROR}")
    n = int(cp.cuda.runtime.getDeviceCount())
    if n <= 0:
        raise RuntimeError("CuPy no detecta ninguna GPU CUDA")
    # Fuerza una operación real en GPU.
    x = cp.asarray([1.0, 2.0, 3.0], dtype=cp.float32)
    _ = float(cp.sum(x).get())


def avg_path_length(n: int | float) -> float:
    n = float(n)
    if n <= 1:
        return 0.0
    if n == 2:
        return 1.0
    # c(n) = 2 H(n-1) - 2(n-1)/n; aproximación con Euler.
    return float(2.0 * (math.log(n - 1.0) + 0.5772156649) - 2.0 * (n - 1.0) / n)


@dataclass
class GpuIFNode:
    is_leaf: bool
    size: int
    depth: int
    feature: int = -1
    threshold: float = 0.0
    normal: Optional[np.ndarray] = None
    left: int = -1
    right: int = -1


class CuPyIsolationForest:
    """
    Isolation Forest/Extended Isolation Forest implementado con CuPy.

    backend='cupy_iforest' => cortes axis-aligned, estilo Isolation Forest clásico.
    backend='cupy_eif'     => cortes por hiperplanos aleatorios, estilo Extended Isolation Forest.

    No usa cuml.ensemble.IsolationForest, porque en varias builds de RAPIDS/cuML ese import no existe.
    """

    def __init__(
        self,
        *,
        backend: str = "cupy_iforest",
        n_estimators: int = 200,
        max_samples: int = 512,
        max_depth: int = 12,
        threshold_percentile: float = 95.0,
        random_state: int = 42,
        eps: float = 1e-12,
    ) -> None:
        self.backend = normalize_backend(backend)
        self.n_estimators = int(n_estimators)
        self.max_samples = int(max_samples)
        self.max_depth = int(max_depth)
        self.threshold_percentile = float(threshold_percentile)
        self.random_state = int(random_state)
        self.eps = float(eps)
        self.trees_: List[List[GpuIFNode]] = []
        self.n_features_in_: Optional[int] = None
        self.actual_max_samples_: Optional[int] = None
        self.threshold_: Optional[float] = None
        self.train_score_percentiles_: Dict[str, float] = {}

    def get_params(self) -> Dict[str, Any]:
        return {
            "backend": self.backend,
            "n_estimators": self.n_estimators,
            "max_samples": self.max_samples,
            "max_depth": self.max_depth,
            "threshold_percentile": self.threshold_percentile,
            "random_state": self.random_state,
        }

    def fit(self, X: np.ndarray) -> "CuPyIsolationForest":
        require_gpu()
        X_np = np.asarray(X, dtype=np.float32)
        if X_np.ndim != 2:
            raise ValueError("X debe ser matriz 2D")
        n, p = X_np.shape
        if n <= 0:
            raise ValueError("No hay filas normales para entrenar")
        self.n_features_in_ = int(p)
        self.actual_max_samples_ = int(min(max(2, self.max_samples), n))
        X_gpu = cp.asarray(X_np, dtype=cp.float32)
        self.trees_ = []
        rng = np.random.default_rng(self.random_state)

        for t in range(self.n_estimators):
            # Muestreo sin reemplazo controlado por CPU; el cálculo del árbol se hace con CuPy.
            idx_np = rng.choice(n, size=self.actual_max_samples_, replace=False)
            Xs = X_gpu[cp.asarray(idx_np, dtype=cp.int64)]
            tree: List[GpuIFNode] = []
            self._build_tree(Xs, depth=0, tree=tree, rng=rng)
            self.trees_.append(tree)

        train_scores = self.score_samples(X_np)
        self.threshold_ = float(np.percentile(train_scores, self.threshold_percentile))
        self.train_score_percentiles_ = {
            "p50": float(np.percentile(train_scores, 50)),
            "p90": float(np.percentile(train_scores, 90)),
            "p95": float(np.percentile(train_scores, 95)),
            "p97": float(np.percentile(train_scores, 97)),
            "p98": float(np.percentile(train_scores, 98)),
            "p99": float(np.percentile(train_scores, 99)),
            "p99_5": float(np.percentile(train_scores, 99.5)),
        }
        return self

    def _build_tree(self, X_node: Any, *, depth: int, tree: List[GpuIFNode], rng: np.random.Generator) -> int:
        n = int(X_node.shape[0])
        node_id = len(tree)
        tree.append(GpuIFNode(is_leaf=True, size=n, depth=depth))

        if depth >= self.max_depth or n <= 1:
            return node_id

        p = int(X_node.shape[1])

        if self.backend == "cupy_eif":
            normal_np = rng.normal(0.0, 1.0, size=p).astype(np.float32)
            norm = float(np.linalg.norm(normal_np))
            if not np.isfinite(norm) or norm <= self.eps:
                return node_id
            normal_np /= norm
            normal_gpu = cp.asarray(normal_np, dtype=cp.float32)
            proj = X_node @ normal_gpu
            mn = float(cp.min(proj).get())
            mx = float(cp.max(proj).get())
            if (not np.isfinite(mn)) or (not np.isfinite(mx)) or mx - mn <= self.eps:
                return node_id
            threshold = float(rng.uniform(mn, mx))
            mask = proj < threshold
            feature = -1
        else:
            # Reintentos para evitar features constantes.
            feature = -1
            mn = mx = threshold = 0.0
            mask = None
            for _ in range(min(10, p)):
                j = int(rng.integers(0, p))
                col = X_node[:, j]
                mn = float(cp.min(col).get())
                mx = float(cp.max(col).get())
                if np.isfinite(mn) and np.isfinite(mx) and mx - mn > self.eps:
                    feature = j
                    threshold = float(rng.uniform(mn, mx))
                    mask = col < threshold
                    break
            if mask is None or feature < 0:
                return node_id
            normal_np = None

        left_count = int(cp.sum(mask).get())
        right_count = n - left_count
        if left_count <= 0 or right_count <= 0:
            return node_id

        left_X = X_node[mask]
        right_X = X_node[~mask]

        left_id = self._build_tree(left_X, depth=depth + 1, tree=tree, rng=rng)
        right_id = self._build_tree(right_X, depth=depth + 1, tree=tree, rng=rng)

        tree[node_id] = GpuIFNode(
            is_leaf=False,
            size=n,
            depth=depth,
            feature=feature,
            threshold=threshold,
            normal=normal_np,
            left=left_id,
            right=right_id,
        )
        return node_id

    def score_samples(self, X: np.ndarray, *, batch_size: int = 20000) -> np.ndarray:
        require_gpu()
        if not self.trees_:
            raise RuntimeError("Modelo no entrenado")
        X_np = np.asarray(X, dtype=np.float32)
        n = X_np.shape[0]
        out_parts: List[np.ndarray] = []
        c_ms = avg_path_length(int(self.actual_max_samples_ or self.max_samples))
        if c_ms <= 0:
            c_ms = 1.0
        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            X_gpu = cp.asarray(X_np[start:end], dtype=cp.float32)
            total = cp.zeros((end - start,), dtype=cp.float32)
            all_idx = cp.arange(end - start, dtype=cp.int64)
            for tree in self.trees_:
                depths = cp.zeros((end - start,), dtype=cp.float32)
                self._apply_tree(tree, 0, X_gpu, all_idx, depths)
                total += depths
            avg_depth = total / float(len(self.trees_))
            # Score de anomalía: mayor = más anómalo.
            scores = cp.power(cp.asarray(2.0, dtype=cp.float32), -avg_depth / float(c_ms))
            out_parts.append(cp.asnumpy(scores).astype(np.float64, copy=False))
        return np.concatenate(out_parts, axis=0) if out_parts else np.array([], dtype=np.float64)

    def _apply_tree(self, tree: List[GpuIFNode], node_id: int, X: Any, idx: Any, depths: Any) -> None:
        if int(idx.size) == 0:
            return
        node = tree[node_id]
        if node.is_leaf or node.left < 0 or node.right < 0:
            depths[idx] = float(node.depth + avg_path_length(node.size))
            return
        Xi = X[idx]
        if self.backend == "cupy_eif":
            normal_gpu = cp.asarray(node.normal, dtype=cp.float32)
            proj = Xi @ normal_gpu
            mask = proj < float(node.threshold)
        else:
            col = Xi[:, int(node.feature)]
            mask = col < float(node.threshold)
        idx_left = idx[mask]
        idx_right = idx[~mask]
        self._apply_tree(tree, node.left, X, idx_left, depths)
        self._apply_tree(tree, node.right, X, idx_right, depths)

    def predict(self, X: np.ndarray) -> np.ndarray:
        scores = self.score_samples(X)
        thr = float(self.threshold_ if self.threshold_ is not None else np.percentile(scores, self.threshold_percentile))
        return (scores >= thr).astype(np.int64)


class ScaledGpuAnomalyModel:
    def __init__(self, scaler: StandardScaler, forest: CuPyIsolationForest, feature_names: Sequence[str]):
        self.scaler = scaler
        self.forest = forest
        self.feature_names = list(feature_names)

    def score_samples(self, X_raw: np.ndarray) -> np.ndarray:
        Xs = self.scaler.transform(np.asarray(X_raw, dtype=np.float32)).astype(np.float32)
        return self.forest.score_samples(Xs)

    def predict(self, X_raw: np.ndarray) -> np.ndarray:
        scores = self.score_samples(X_raw)
        thr = float(self.forest.threshold_)
        return (scores >= thr).astype(np.int64)

    def get_params(self) -> Dict[str, Any]:
        return self.forest.get_params()


def normalize_backend(backend: str) -> str:
    b = str(backend or "cupy_iforest").strip().lower()
    aliases = {
        "cuml_iforest": "cupy_iforest",  # compatibilidad con el .sh viejo
        "iforest": "cupy_iforest",
        "isolation_forest": "cupy_iforest",
        "cupy_iforest": "cupy_iforest",
        "torch_eif": "cupy_eif",        # compatibilidad con el .sh viejo
        "eif": "cupy_eif",
        "extended_iforest": "cupy_eif",
        "cupy_eif": "cupy_eif",
    }
    if b not in aliases:
        raise ValueError(f"backend inválido: {backend}. Usa cupy_iforest o cupy_eif")
    return aliases[b]


def safe_auc(func, y_true: np.ndarray, y_score: np.ndarray) -> float:
    try:
        if len(np.unique(y_true)) < 2:
            return float("nan")
        return float(func(y_true, y_score))
    except Exception:
        return float("nan")


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray) -> Dict[str, Any]:
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    y_score = np.asarray(y_score).astype(float)
    labels = [0, 1]
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    tn, fp, fn, tp = [int(x) for x in cm.ravel()]

    precision_arr, recall_arr, f1_arr, support_arr = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0
    )

    out: Dict[str, Any] = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)) if len(np.unique(y_true)) > 1 else 0.0,
        "roc_auc": safe_auc(roc_auc_score, y_true, y_score),
        "pr_auc": safe_auc(average_precision_score, y_true, y_score),
        "precision_macro": float(precision_score(y_true, y_pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "precision_weighted": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "normal": {
            "precision": float(precision_arr[0]),
            "recall": float(recall_arr[0]),
            "f1": float(f1_arr[0]),
            "support": int(support_arr[0]),
        },
        "anomaly": {
            "precision": float(precision_arr[1]),
            "recall": float(recall_arr[1]),
            "f1": float(f1_arr[1]),
            "support": int(support_arr[1]),
        },
        "confusion_matrix": {
            "labels": ["NORMAL_0", "ANOMALY_1"],
            "matrix": cm.tolist(),
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "tp": tp,
        },
        "rates": {
            "tpr_recall_anomaly": float(tp / (tp + fn)) if (tp + fn) else 0.0,
            "fpr": float(fp / (fp + tn)) if (fp + tn) else 0.0,
            "tnr_specificity": float(tn / (tn + fp)) if (tn + fp) else 0.0,
            "fnr": float(fn / (fn + tp)) if (fn + tp) else 0.0,
        },
        "classification_report": classification_report(
            y_true,
            y_pred,
            labels=labels,
            target_names=["NORMAL", "ANOMALY"],
            output_dict=True,
            zero_division=0,
        ),
        "score_summary": {
            "min": float(np.min(y_score)) if y_score.size else float("nan"),
            "p01": float(np.percentile(y_score, 1)) if y_score.size else float("nan"),
            "p05": float(np.percentile(y_score, 5)) if y_score.size else float("nan"),
            "p50": float(np.percentile(y_score, 50)) if y_score.size else float("nan"),
            "p95": float(np.percentile(y_score, 95)) if y_score.size else float("nan"),
            "p99": float(np.percentile(y_score, 99)) if y_score.size else float("nan"),
            "max": float(np.max(y_score)) if y_score.size else float("nan"),
        },
    }
    return out


def metric_for_tuning(metrics: Dict[str, Any], tune_metric: str) -> float:
    m = (tune_metric or "auto").lower()
    if m in {"f1", "f1_anomaly", "anomaly_f1"}:
        return float(metrics["anomaly"]["f1"])
    if m in {"pr_auc", "ap", "average_precision"}:
        val = float(metrics["pr_auc"])
        return val if np.isfinite(val) else 0.0
    if m in {"roc_auc", "auc"}:
        val = float(metrics["roc_auc"])
        return val if np.isfinite(val) else 0.0
    if m in {"mcc"}:
        return float(metrics["mcc"])
    # auto: prioriza detección binaria con algo de ranking.
    f1 = float(metrics["anomaly"]["f1"])
    pr = float(metrics["pr_auc"])
    if not np.isfinite(pr):
        pr = 0.0
    return 0.75 * f1 + 0.25 * pr


def sample_indices_stratified(y: np.ndarray, max_rows: int, seed: int) -> np.ndarray:
    n = len(y)
    if max_rows <= 0 or max_rows >= n:
        return np.arange(n)
    sss = StratifiedShuffleSplit(n_splits=1, train_size=max_rows, random_state=seed)
    idx, _ = next(sss.split(np.zeros((n, 1)), y))
    return np.asarray(idx)


def candidate_grid(args: argparse.Namespace) -> List[Dict[str, Any]]:
    def parse_ints(s: str) -> List[int]:
        return [int(x.strip()) for x in str(s).split(",") if x.strip()]

    def parse_floats(s: str) -> List[float]:
        return [float(x.strip()) for x in str(s).split(",") if x.strip()]

    vals = []
    for n_estimators in parse_ints(args.tune_n_estimators_grid):
        for max_samples in parse_ints(args.tune_max_samples_grid):
            for max_depth in parse_ints(args.tune_max_depth_grid):
                for threshold_percentile in parse_floats(args.tune_threshold_percentile_grid):
                    vals.append({
                        "n_estimators": n_estimators,
                        "max_samples": max_samples,
                        "max_depth": max_depth,
                        "threshold_percentile": threshold_percentile,
                    })
    rng = random.Random(args.seed)
    rng.shuffle(vals)
    if args.tune_n_iter > 0:
        vals = vals[: min(args.tune_n_iter, len(vals))]
    return vals


def fit_scaled_model(
    X_train_normals_raw: np.ndarray,
    *,
    backend: str,
    params: Dict[str, Any],
    seed: int,
    feature_names: Sequence[str],
) -> ScaledGpuAnomalyModel:
    scaler = StandardScaler()
    X_train_normals_scaled = scaler.fit_transform(X_train_normals_raw).astype(np.float32)
    forest = CuPyIsolationForest(backend=backend, random_state=seed, **params)
    forest.fit(X_train_normals_scaled)
    return ScaledGpuAnomalyModel(scaler, forest, feature_names)


def run_tuning(
    X_train: np.ndarray,
    y_train: np.ndarray,
    *,
    backend: str,
    args: argparse.Namespace,
    feature_names: Sequence[str],
) -> Tuple[Dict[str, Any], pd.DataFrame]:
    idx = sample_indices_stratified(y_train, args.tune_max_train, args.seed)
    X_tune = X_train[idx]
    y_tune = y_train[idx]
    cv = max(2, int(args.cv))
    candidates = candidate_grid(args)
    print(f"[TUNE] backend={backend} candidates={len(candidates)} cv={cv} rows={len(y_tune)} metric={args.tune_metric}", flush=True)
    rows: List[Dict[str, Any]] = []

    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=args.seed)
    for ci, params in enumerate(candidates, start=1):
        fold_scores: List[float] = []
        fold_f1: List[float] = []
        fold_pr: List[float] = []
        fold_roc: List[float] = []
        fold_tpr: List[float] = []
        fold_fpr: List[float] = []
        errors: List[str] = []
        t0 = now()
        for fold, (tr_idx, va_idx) in enumerate(skf.split(X_tune, y_tune), start=1):
            try:
                X_tr, y_tr = X_tune[tr_idx], y_tune[tr_idx]
                X_va, y_va = X_tune[va_idx], y_tune[va_idx]
                normal_mask = y_tr == 0
                if int(normal_mask.sum()) < 2:
                    raise RuntimeError("fold sin normales suficientes")
                model = fit_scaled_model(
                    X_tr[normal_mask],
                    backend=backend,
                    params=params,
                    seed=args.seed + ci * 1000 + fold,
                    feature_names=feature_names,
                )
                y_score = model.score_samples(X_va)
                y_pred = (y_score >= float(model.forest.threshold_)).astype(int)
                met = compute_metrics(y_va, y_pred, y_score)
                fold_scores.append(metric_for_tuning(met, args.tune_metric))
                fold_f1.append(float(met["anomaly"]["f1"]))
                fold_pr.append(float(met["pr_auc"]) if np.isfinite(met["pr_auc"]) else 0.0)
                fold_roc.append(float(met["roc_auc"]) if np.isfinite(met["roc_auc"]) else 0.0)
                fold_tpr.append(float(met["rates"]["tpr_recall_anomaly"]))
                fold_fpr.append(float(met["rates"]["fpr"]))
            except Exception as e:
                errors.append(f"fold={fold}: {repr(e)}")
        sec = now() - t0
        if fold_scores:
            score_mean = float(np.mean(fold_scores))
            score_std = float(np.std(fold_scores))
        else:
            score_mean = -1.0
            score_std = 0.0
        row = {
            "candidate": ci,
            "backend": backend,
            "metric": args.tune_metric,
            "score_mean": score_mean,
            "score_std": score_std,
            "f1_anomaly_mean": float(np.mean(fold_f1)) if fold_f1 else 0.0,
            "pr_auc_mean": float(np.mean(fold_pr)) if fold_pr else 0.0,
            "roc_auc_mean": float(np.mean(fold_roc)) if fold_roc else 0.0,
            "tpr_mean": float(np.mean(fold_tpr)) if fold_tpr else 0.0,
            "fpr_mean": float(np.mean(fold_fpr)) if fold_fpr else 0.0,
            "seconds": float(sec),
            "errors": " | ".join(errors),
            **params,
        }
        rows.append(row)
        print(
            f"[TUNE] {ci:04d}/{len(candidates)} score={score_mean:.5f} "
            f"f1={row['f1_anomaly_mean']:.5f} pr_auc={row['pr_auc_mean']:.5f} params={params}",
            flush=True,
        )
    df = pd.DataFrame(rows).sort_values(["score_mean", "f1_anomaly_mean", "pr_auc_mean"], ascending=False)
    if df.empty:
        raise RuntimeError("No hubo candidatos de tuning")
    best_row = df.iloc[0].to_dict()
    best_params = {
        "n_estimators": int(best_row["n_estimators"]),
        "max_samples": int(best_row["max_samples"]),
        "max_depth": int(best_row["max_depth"]),
        "threshold_percentile": float(best_row["threshold_percentile"]),
    }
    return best_params, df


def permutation_importance(
    model: ScaledGpuAnomalyModel,
    X: np.ndarray,
    y: np.ndarray,
    feature_names: Sequence[str],
    *,
    max_rows: int,
    seed: int,
    metric: str,
) -> pd.DataFrame:
    idx = sample_indices_stratified(y, max_rows, seed) if max_rows and max_rows < len(y) else np.arange(len(y))
    X0 = np.asarray(X[idx], dtype=np.float32)
    y0 = np.asarray(y[idx], dtype=int)
    base_score = model.score_samples(X0)
    base_pred = (base_score >= float(model.forest.threshold_)).astype(int)
    base_met = compute_metrics(y0, base_pred, base_score)
    base_metric = metric_for_tuning(base_met, metric)
    base_f1 = float(base_met["anomaly"]["f1"])
    base_pr = float(base_met["pr_auc"]) if np.isfinite(base_met["pr_auc"]) else 0.0
    rng = np.random.default_rng(seed)
    rows = []
    print(f"[FI] permutation rows={len(y0)} features={len(feature_names)} baseline_{metric}={base_metric:.5f}", flush=True)
    for j, name in enumerate(feature_names):
        Xp = X0.copy()
        Xp[:, j] = rng.permutation(Xp[:, j])
        sc = model.score_samples(Xp)
        pred = (sc >= float(model.forest.threshold_)).astype(int)
        met = compute_metrics(y0, pred, sc)
        mval = metric_for_tuning(met, metric)
        f1 = float(met["anomaly"]["f1"])
        pr = float(met["pr_auc"]) if np.isfinite(met["pr_auc"]) else 0.0
        rows.append({
            "rank": 0,
            "feature": name,
            "importance": float(base_metric - mval),
            "baseline_metric": float(base_metric),
            "permuted_metric": float(mval),
            "f1_anomaly_drop": float(base_f1 - f1),
            "pr_auc_drop": float(base_pr - pr),
            "metric": metric,
        })
    out = pd.DataFrame(rows).sort_values("importance", ascending=False).reset_index(drop=True)
    out["rank"] = np.arange(1, len(out) + 1)
    return out


def benchmark_model(model: ScaledGpuAnomalyModel, X: np.ndarray, *, max_rows: int, batch_size: int) -> Dict[str, Any]:
    if max_rows and max_rows > 0:
        Xb = X[: min(max_rows, len(X))]
    else:
        Xb = X
    Xb = np.asarray(Xb, dtype=np.float32)
    # Warmup GPU
    _ = model.score_samples(Xb[: min(len(Xb), max(1, batch_size))])
    if cp is not None:
        cp.cuda.Stream.null.synchronize()
    batch_times = []
    total_rows = 0
    t0 = now()
    for start in range(0, len(Xb), batch_size):
        end = min(start + batch_size, len(Xb))
        bt0 = now()
        _ = model.score_samples(Xb[start:end])
        if cp is not None:
            cp.cuda.Stream.null.synchronize()
        dt = now() - bt0
        batch_times.append((dt, end - start))
        total_rows += end - start
    total = now() - t0
    per_row_ms = []
    for dt, rows in batch_times:
        if rows:
            per_row_ms.extend([1000.0 * dt / rows] * rows)
    arr = np.asarray(per_row_ms, dtype=float) if per_row_ms else np.asarray([], dtype=float)
    return {
        "rows": int(total_rows),
        "batch_size": int(batch_size),
        "total_seconds": float(total),
        "throughput_rows_per_second": float(total_rows / total) if total > 0 else float("inf"),
        "latency_ms_per_row_estimated": {
            "p50": float(np.percentile(arr, 50)) if arr.size else float("nan"),
            "p95": float(np.percentile(arr, 95)) if arr.size else float("nan"),
            "p99": float(np.percentile(arr, 99)) if arr.size else float("nan"),
            "mean": float(np.mean(arr)) if arr.size else float("nan"),
        },
    }


def load_features(data_path: str, feature_cols_arg: str, label_col: str) -> Tuple[pd.DataFrame, List[str]]:
    df = pd.read_parquet(data_path) if data_path.endswith(".parquet") else pd.read_csv(data_path)
    if feature_cols_arg.strip():
        feature_cols = [c.strip() for c in feature_cols_arg.split(",") if c.strip()]
    else:
        try:
            from waf_ml.features.http_features import TOP25_HTTP_FEATURES
            feature_cols = list(TOP25_HTTP_FEATURES)
        except Exception:
            blocked = {label_col, "label_binary", "label_multiclass", "label_multilabel", "label_type_raw"}
            feature_cols = [c for c in df.columns if c not in blocked and pd.api.types.is_numeric_dtype(df[c])]
    missing = [c for c in feature_cols + [label_col] if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas en {data_path}: {missing}")
    return df, feature_cols


def main() -> int:
    p = argparse.ArgumentParser(description="GPU Isolation Forest / Extended Isolation Forest para WAF HTTP features")
    p.add_argument("--mode", default="train", choices=["train"])
    p.add_argument("--backend", default="cupy_iforest", help="cupy_iforest o cupy_eif. Alias: cuml_iforest, torch_eif")
    p.add_argument("--data", required=True)
    p.add_argument("--label-col", default="label_binary")
    p.add_argument("--feature-cols", default="")
    p.add_argument("--test-size", type=float, default=0.2)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--cv", type=int, default=3)
    p.add_argument("--tune", default="random", choices=["none", "random"])
    p.add_argument("--tune-metric", default="auto")
    p.add_argument("--tune-n-iter", type=int, default=48)
    p.add_argument("--tune-max-train", type=int, default=30000)
    p.add_argument("--tune-n-estimators-grid", default="100,200,400")
    p.add_argument("--tune-max-samples-grid", default="128,256,512,1024")
    p.add_argument("--tune-max-depth-grid", default="8,12,16")
    p.add_argument("--tune-threshold-percentile-grid", default="80,85,90,92,95,97,98,99,99.5")
    p.add_argument("--n-estimators", type=int, default=200)
    p.add_argument("--max-samples", type=int, default=512)
    p.add_argument("--max-depth", type=int, default=12)
    p.add_argument("--threshold-percentile", type=float, default=95.0)
    p.add_argument("--require-gpu", action="store_true")
    p.add_argument("--out", required=True)
    p.add_argument("--metrics-out", required=True)
    p.add_argument("--pred-out", required=True)
    p.add_argument("--tune-results-out", required=True)
    p.add_argument("--fi-kind", default="permutation", choices=["none", "permutation", "shap"])
    p.add_argument("--fi-out", required=True)
    p.add_argument("--fi-topk", type=int, default=25)
    p.add_argument("--fi-max-rows", type=int, default=1000)
    p.add_argument("--benchmark-mode", default="auto", choices=["none", "auto"])
    p.add_argument("--benchmark-max-rows", type=int, default=0)
    p.add_argument("--benchmark-batch-size", type=int, default=4096)
    p.add_argument("--benchmark-out", required=True)
    args = p.parse_args()

    backend = normalize_backend(args.backend)
    print(f"[START] backend={backend} data={args.data}", flush=True)
    gpu_info = get_gpu_info()
    print("[GPU] " + json.dumps(gpu_info, ensure_ascii=False), flush=True)
    if args.require_gpu:
        require_gpu()

    t_all0 = now()
    mem_start = psutil.Process(os.getpid()).memory_info().rss if psutil else None

    df, feature_cols = load_features(args.data, args.feature_cols, args.label_col)
    X = df[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)
    y = df[args.label_col].astype(int).to_numpy()
    print(f"[DATA] rows={len(df)} cols={len(feature_cols)} normal={(y==0).sum()} anomaly={(y==1).sum()}", flush=True)
    print("[DATA] features=" + ",".join(feature_cols), flush=True)

    idx_all = np.arange(len(y))
    train_idx, test_idx = train_test_split(
        idx_all, test_size=args.test_size, random_state=args.seed, stratify=y
    )
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]
    print(f"[SPLIT] train={len(train_idx)} test={len(test_idx)} train_normals={(y_train==0).sum()}", flush=True)

    t_tune0 = now()
    if args.tune == "none":
        best_params = {
            "n_estimators": args.n_estimators,
            "max_samples": args.max_samples,
            "max_depth": args.max_depth,
            "threshold_percentile": args.threshold_percentile,
        }
        tune_df = pd.DataFrame([{ "candidate": 1, "backend": backend, "score_mean": np.nan, **best_params }])
    else:
        best_params, tune_df = run_tuning(X_train, y_train, backend=backend, args=args, feature_names=feature_cols)
    t_tune = now() - t_tune0
    ensure_parent(args.tune_results_out)
    tune_df.to_csv(args.tune_results_out, index=False)
    print(f"[TUNE] done seconds={t_tune:.2f} best={best_params}", flush=True)

    t_fit0 = now()
    X_train_normals = X_train[y_train == 0]
    model = fit_scaled_model(
        X_train_normals,
        backend=backend,
        params=best_params,
        seed=args.seed,
        feature_names=feature_cols,
    )
    t_fit = now() - t_fit0
    print(f"[FIT] seconds={t_fit:.2f} threshold={model.forest.threshold_:.8f}", flush=True)

    t_pred0 = now()
    y_score = model.score_samples(X_test)
    y_pred = (y_score >= float(model.forest.threshold_)).astype(int)
    t_pred = now() - t_pred0
    metrics = compute_metrics(y_test, y_pred, y_score)
    print(
        f"[TEST] acc={metrics['accuracy']:.5f} f1_anom={metrics['anomaly']['f1']:.5f} "
        f"tpr={metrics['rates']['tpr_recall_anomaly']:.5f} fpr={metrics['rates']['fpr']:.5f} "
        f"pr_auc={metrics['pr_auc']:.5f} roc_auc={metrics['roc_auc']:.5f}",
        flush=True,
    )

    pred_df = pd.DataFrame({
        "row_index": test_idx,
        "y_true": y_test,
        "y_pred": y_pred,
        "anomaly_score": y_score,
        "threshold": float(model.forest.threshold_),
    })
    ensure_parent(args.pred_out)
    pred_df.to_csv(args.pred_out, index=False)

    # Feature importance
    fi_seconds = 0.0
    if args.fi_kind == "none":
        fi_df = pd.DataFrame(columns=["rank", "feature", "importance"])
    else:
        if args.fi_kind == "shap":
            print("[FI] fi-kind=shap solicitado; para IF/EIF se usa permutation importance estable y comparable.", flush=True)
        fi0 = now()
        fi_df = permutation_importance(
            model,
            X_test,
            y_test,
            feature_cols,
            max_rows=args.fi_max_rows,
            seed=args.seed + 777,
            metric=args.tune_metric,
        )
        if args.fi_topk and args.fi_topk > 0:
            fi_df = fi_df.head(args.fi_topk)
        fi_seconds = now() - fi0
    ensure_parent(args.fi_out)
    fi_df.to_csv(args.fi_out, index=False)
    print(f"[FI] seconds={fi_seconds:.2f} out={args.fi_out}", flush=True)

    # Benchmark
    if args.benchmark_mode == "none":
        bench = {}
    else:
        b0 = now()
        bench = benchmark_model(
            model,
            X_test,
            max_rows=args.benchmark_max_rows,
            batch_size=args.benchmark_batch_size,
        )
        bench["seconds_including_overhead"] = float(now() - b0)
    json_dump(bench, args.benchmark_out)
    print(f"[BENCH] {bench}", flush=True)

    ensure_parent(args.out)
    joblib.dump(model, args.out)
    model_size_bytes = int(Path(args.out).stat().st_size) if Path(args.out).exists() else 0

    mem_end = psutil.Process(os.getpid()).memory_info().rss if psutil else None
    total_seconds = now() - t_all0
    metrics_out = {
        **metrics,
        "dataset": {
            "data_path": args.data,
            "rows_total": int(len(df)),
            "rows_train": int(len(train_idx)),
            "rows_test": int(len(test_idx)),
            "train_normals": int((y_train == 0).sum()),
            "features": list(feature_cols),
        },
        "model": {
            "family": "IsolationForest" if backend == "cupy_iforest" else "ExtendedIsolationForest",
            "backend": backend,
            "params": model.get_params(),
            "threshold": float(model.forest.threshold_),
            "train_score_percentiles": model.forest.train_score_percentiles_,
            "model_size_bytes": model_size_bytes,
        },
        "timing_seconds": {
            "tune": float(t_tune),
            "fit_final": float(t_fit),
            "predict_test": float(t_pred),
            "feature_importance": float(fi_seconds),
            "total": float(total_seconds),
        },
        "resources": {
            "gpu": gpu_info,
            "rss_start_bytes": int(mem_start) if mem_start is not None else None,
            "rss_end_bytes": int(mem_end) if mem_end is not None else None,
            "rss_delta_bytes": int(mem_end - mem_start) if mem_start is not None and mem_end is not None else None,
        },
        "outputs": {
            "model": args.out,
            "metrics": args.metrics_out,
            "pred": args.pred_out,
            "search": args.tune_results_out,
            "feature_importance": args.fi_out,
            "benchmark": args.benchmark_out,
        },
    }
    json_dump(metrics_out, args.metrics_out)
    print(f"[SAVE] model={args.out} metrics={args.metrics_out} pred={args.pred_out}", flush=True)
    print("[DONE]", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print("[FATAL]", repr(e), file=sys.stderr, flush=True)
        traceback.print_exc()
        raise

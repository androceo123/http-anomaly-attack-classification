from __future__ import annotations

import argparse
import glob
import json
import os
import re

import pandas as pd
from tqdm import tqdm

from waf_ml.data.csic_loader import load_csic_txt, make_labels
from waf_ml.features.http_features import extract_http_features


def _to_bytes(v) -> bytes:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return b""
    s = str(v)
    if s in {"", "nan", "None"}:
        return b""
    return s.encode("utf-8", errors="ignore")


def _json_to_headers(s: str) -> dict:
    if not s:
        return {}
    try:
        return json.loads(s)
    except Exception:
        return {}


def _collect_inputs(items: list[str]) -> list[str]:
    """
    Accepts:
      - files
      - globs (e.g. data/raw/csic/*.txt)
      - directories (loads **/*.txt)
    """
    paths: list[str] = []
    for it in items:
        it = (it or "").strip()
        if not it:
            continue

        if os.path.isdir(it):
            paths.extend(sorted(glob.glob(os.path.join(it, "**", "*.txt"), recursive=True)))
        else:
            paths.extend(sorted(glob.glob(it)))

    # de-dup, keep order
    seen = set()
    out = []
    for p in paths:
        if p not in seen:
            out.append(p)
            seen.add(p)
    return out


def _infer_label_from_filename(path: str) -> str:
    """
    CSIC 2010 típicamente trae:
      - normalTrafficTraining.txt / normalTrafficTest.txt
      - anomalousTrafficTest.txt
    """
    name = os.path.basename(path).lower()

    # anomalous first (avoid weird overlaps)
    if ("anomal" in name) or ("attack" in name) or ("anomaly" in name):
        return "anomalous"
    if "normal" in name:
        return "normal"

    # fallback: allow patterns like allNormals / allAnomalies
    if re.search(r"\bnormals?\b", name):
        return "normal"
    if re.search(r"\banomal(?:y|ous|ies)\b", name):
        return "anomalous"

    raise ValueError(
        f"No pude inferir label desde el nombre: {path}\n"
        "Renombrá el archivo para incluir 'normal' o 'anomalous', o usá --label para forzar."
    )


def _infer_split_from_filename(path: str) -> str:
    name = os.path.basename(path).lower()
    if "train" in name or "training" in name:
        return "train"
    if "test" in name:
        return "test"
    return ""


def main() -> None:
    ap = argparse.ArgumentParser()

    # Legacy single-file mode (no rompe lo que ya tenías / lo que está en el libro)
    ap.add_argument("--input", default=None, help="(legacy) Path a un único CSIC .txt")

    # New multi-file mode
    ap.add_argument(
        "--inputs",
        nargs="+",
        default=None,
        help="Uno o más .txt / globs / directorios (si es dir, carga **/*.txt)",
    )

    ap.add_argument("--output", required=True, help="Path al output parquet/csv (features)")

    # Label policy
    ap.add_argument(
        "--label",
        default=None,
        choices=["normal", "anomalous"],
        help="(legacy) requerido con --input. (override) si se usa con --inputs, fuerza ese label para TODOS los archivos.",
    )
    ap.add_argument(
        "--label-prefix",
        default="CSIC-ANOMALOUS",
        help="Valor para la clase anómala en label_multiclass/multilabel",
    )

    ap.add_argument("--sample-n", type=int, default=0, help="Si >0, procesa solo N requests POR ARCHIVO (debug)")
    ap.add_argument("--out-format", default="parquet", choices=["parquet", "csv"])
    ap.add_argument("--keep-absolute-uri", action="store_true", help="NO recortar http://host:port del request line")
    ap.add_argument("--use-headers", dest="use_headers", action="store_true", default=True, help="Pasar headers parseados al extractor de features (default: ON, requerido para Content-Length/Content-Type mismatch).")
    ap.add_argument("--no-use-headers", dest="use_headers", action="store_false", help="No pasar headers al extractor de features.")

    args = ap.parse_args()

    if (args.input is None and args.inputs is None) or (args.input and args.inputs):
        raise SystemExit("Usá exactamente UNO: --input (single) o --inputs (multi).")

    dfs = []

    if args.input:
        # Legacy mode: same as before, but we also set label_type_raw + split + dataset_name
        if not args.label:
            raise SystemExit("--label es requerido cuando usás --input")

        df = load_csic_txt(args.input, keep_absolute_uri=args.keep_absolute_uri, sample_n=args.sample_n)
        if df.empty:
            raise SystemExit(f"No requests parseadas desde: {args.input}")

        df["source_file"] = args.input
        df["dataset_name"] = "CSIC-2010"
        df["split"] = _infer_split_from_filename(args.input)
        df["label_type_raw"] = args.label
        dfs.append(df)

    else:
        inputs = _collect_inputs(args.inputs or [])
        if not inputs:
            raise SystemExit("No se encontraron inputs. Revisá --inputs (paths/globs/dirs).")

        for p in tqdm(inputs, desc="Loading CSIC txt"):
            df = load_csic_txt(p, keep_absolute_uri=args.keep_absolute_uri, sample_n=args.sample_n)
            if df is None or df.empty:
                continue

            df["source_file"] = p
            df["dataset_name"] = "CSIC-2010"
            df["split"] = _infer_split_from_filename(p)

            if args.label:
                df["label_type_raw"] = args.label
            else:
                df["label_type_raw"] = _infer_label_from_filename(p)

            dfs.append(df)

        if not dfs:
            raise SystemExit("No se parseó ningún request desde los inputs.")

    df_all = pd.concat(dfs, ignore_index=True)

    # Crea: label_binary, label_multiclass, label_multilabel (K=2 para CSIC)
    df_all = make_labels(df_all, label_prefix=args.label_prefix, label_type_col="label_type_raw")

    # Null-safe
    df_all["request_http_method"] = df_all["request_http_method"].fillna("")
    df_all["request_http_request"] = df_all["request_http_request"].fillna("")
    df_all["request_body"] = df_all["request_body"].fillna("")
    df_all["request_headers_json"] = df_all["request_headers_json"].fillna("")

    tqdm.pandas(desc="Extracting features (CSIC)")
    feats = df_all.progress_apply(
        lambda r: extract_http_features(
            method=str(r["request_http_method"]),
            uri=str(r["request_http_request"]),
            headers=_json_to_headers(str(r["request_headers_json"])) if args.use_headers else None,
            body=_to_bytes(r["request_body"]),
        ),
        axis=1,
    )

    feat_df = pd.DataFrame(list(feats))

    top25_features = [
        "body_encoded_ratio", "uri_encoded_ratio", "path_depth", "uri_non_alnum_ratio",
        "max_param_value_len", "body_len", "uri_len", "query_len", "n_query_params",
        "req_content_length", "uri_entropy", "body_entropy", "invalid_percent_encoding_count",
        "double_encoding_count", "path_traversal_token_count", "sql_token_count",
        "xss_token_count", "cmd_injection_token_count", "file_inclusion_token_count",
        "quote_comment_operator_count", "repeated_param_name_count", "empty_param_value_ratio",
        "avg_param_value_len", "content_length_body_mismatch", "content_type_body_mismatch",
    ]
    missing = [c for c in top25_features if c not in feat_df.columns]
    if missing:
        raise SystemExit(f"Faltan features top-25 en el extractor: {missing}")

    out = pd.concat([df_all, feat_df], axis=1)

    if args.out_format == "parquet" or args.output.lower().endswith(".parquet"):
        out.to_parquet(args.output, index=False)
    else:
        out.to_csv(args.output, index=False)

    print(f"Wrote: {args.output}  rows={len(out)}  cols={len(out.columns)}")
    print("Top-25 features CSIC generadas:", ", ".join(top25_features))


if __name__ == "__main__":
    main()
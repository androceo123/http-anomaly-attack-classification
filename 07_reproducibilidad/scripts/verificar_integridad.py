"""Verifica el manifiesto del repositorio y, opcionalmente, artefactos referenciados.

No carga modelos ni ejecuta entrenamientos. Requiere Python 3.11 o posterior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

DEFAULT_MANIFEST = Path("07_reproducibilidad/manifest_repositorio.json")
HISTORICAL_CATALOG = Path("07_reproducibilidad/catalogo_archivos.json")


def safe_path(root, relative):
    relative = PurePosixPath(relative)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Ruta no válida en manifiesto: {relative}")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Ruta fuera de la raíz indicada: {relative}")
    return path


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check(row, roots, *, allow_repository_alias=False):
    names = [row["path"]]
    if allow_repository_alias and row.get("repository_path"):
        names.insert(0, row["repository_path"])
    candidates = [safe_path(root, name) for root in roots for name in names]
    failures = []
    for target in candidates:
        if not target.is_file():
            continue
        if target.stat().st_size != int(row["bytes"]):
            failures.append("size_mismatch")
        elif digest(target) != row["sha256"]:
            failures.append("sha256_mismatch")
        else:
            return {"path": row["path"], "status": "ok"}
    return {"path": row["path"], "status": failures[0] if failures else "missing"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Raíz del repositorio")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST,
                        help="Manifiesto relativo a --root, o ruta absoluta")
    parser.add_argument("--include-external", action="store_true",
                        help="Requerir también todos los archivos del catálogo histórico")
    parser.add_argument("--external-root", type=Path, action="append", default=[],
                        help="Almacenamiento adicional; conserva rutas relativas; repetible")
    parser.add_argument("--output", type=Path,
                        help="Informe JSON nuevo; no sobrescribe un archivo existente")
    args = parser.parse_args()
    if args.external_root and not args.include_external:
        parser.error("--external-root requiere --include-external")
    root = args.root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        rows = manifest["files"]
        if not isinstance(rows, list):
            raise ValueError("El manifiesto debe contener una lista files")
        results = [check(row, [root]) for row in rows]
        external_results = []
        if args.include_external:
            catalog = json.loads((root / HISTORICAL_CATALOG).read_text(encoding="utf-8"))
            roots = [root] + [p.resolve() for p in args.external_root]
            external_results = [
                check(row, roots, allow_repository_alias=True)
                for row in catalog["physical_files"]
            ]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    failures = [row for row in results if row["status"] != "ok"]
    external_failures = [row for row in external_results if row["status"] != "ok"]
    report = {
        "scope": "Archivos de la revisión publicada; manifiesto e informe excluidos para evitar referencias circulares.",
        "checked": len(results),
        "passed": len(results) - len(failures),
        "failures": failures,
        "historical_catalog_checked": len(external_results),
        "historical_catalog_failures": external_failures,
        "training_executed": False,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failures or external_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

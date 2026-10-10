#!/usr/bin/env python3
"""
Exporta una base de datos SQLite (.db) a CSV.

Uso rapido:
    python export_db_to_csv.py "DS_Augmented_v2.db"

Eso crea una carpeta llamada DS_Augmented_v2_csv con un .csv por cada tabla.

Otros usos:
    python export_db_to_csv.py "DS_Augmented_v2.db" --list-tables
    python export_db_to_csv.py "DS_Augmented_v2.db" --table mi_tabla --output mi_tabla.csv
    python export_db_to_csv.py "DS_Augmented_v2.db" --include-views
"""

from __future__ import annotations

import argparse
import csv
import re
import sqlite3
import sys
from pathlib import Path
from typing import Iterable, Iterator, Sequence


FETCH_SIZE = 10_000


def quote_identifier(name: str) -> str:
    """Cita nombres de tablas/vistas para SQLite de forma segura."""
    return '"' + name.replace('"', '""') + '"'


def safe_filename(name: str) -> str:
    """Convierte el nombre de una tabla en un nombre de archivo valido."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._-")
    return cleaned or "tabla"


def normalize_value(value):
    """Convierte valores no aptos para CSV a texto simple."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        # Los BLOB se guardan como hexadecimal para no romper el CSV.
        return "0x" + value.hex()
    return value


def get_objects(conn: sqlite3.Connection, include_views: bool = False) -> list[tuple[str, str]]:
    """Devuelve [(tipo, nombre)] para tablas y, opcionalmente, vistas."""
    types = ("table", "view") if include_views else ("table",)
    placeholders = ",".join("?" for _ in types)
    sql = f"""
        SELECT type, name
        FROM sqlite_master
        WHERE type IN ({placeholders})
          AND name NOT LIKE 'sqlite_%'
        ORDER BY type, name
    """
    return [(row[0], row[1]) for row in conn.execute(sql, types)]


def row_batches(cursor: sqlite3.Cursor, fetch_size: int = FETCH_SIZE) -> Iterator[Sequence[sqlite3.Row]]:
    while True:
        rows = cursor.fetchmany(fetch_size)
        if not rows:
            break
        yield rows


def export_object_to_csv(
    conn: sqlite3.Connection,
    object_name: str,
    csv_path: Path,
    delimiter: str = ",",
    encoding: str = "utf-8-sig",
) -> int:
    """Exporta una tabla/vista a CSV y devuelve la cantidad de filas escritas."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    query = f"SELECT * FROM {quote_identifier(object_name)}"
    cursor = conn.execute(query)
    headers = [description[0] for description in cursor.description or []]

    total_rows = 0
    with csv_path.open("w", newline="", encoding=encoding) as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(headers)

        for batch in row_batches(cursor):
            writer.writerows([normalize_value(value) for value in row] for row in batch)
            total_rows += len(batch)

    return total_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convierte/exporta una base SQLite .db a CSV."
    )
    parser.add_argument(
        "database",
        type=Path,
        help="Ruta del archivo .db, por ejemplo: DS_Augmented_v2.db",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help=(
            "Carpeta de salida. Si usas --table, tambien puede ser un archivo .csv. "
            "Por defecto crea <nombre_db>_csv."
        ),
    )
    parser.add_argument(
        "--table",
        help="Exporta solo una tabla/vista especifica.",
    )
    parser.add_argument(
        "--include-views",
        action="store_true",
        help="Incluye vistas ademas de tablas.",
    )
    parser.add_argument(
        "--list-tables",
        action="store_true",
        help="Muestra las tablas/vistas disponibles y no exporta nada.",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Delimitador del CSV. Por defecto: coma. Para punto y coma usa ';'.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8-sig",
        help="Encoding del CSV. Por defecto: utf-8-sig, compatible con Excel.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.database.exists():
        print(f"ERROR: No existe el archivo: {args.database}", file=sys.stderr)
        return 1

    if not args.database.is_file():
        print(f"ERROR: La ruta no es un archivo: {args.database}", file=sys.stderr)
        return 1

    try:
        conn = sqlite3.connect(str(args.database))
    except sqlite3.Error as exc:
        print(f"ERROR: No pude abrir la base de datos: {exc}", file=sys.stderr)
        return 1

    try:
        objects = get_objects(conn, include_views=args.include_views)

        if args.list_tables:
            if not objects:
                print("No se encontraron tablas/vistas.")
                return 0
            print("Objetos encontrados:")
            for obj_type, name in objects:
                print(f"- {name} ({obj_type})")
            return 0

        if args.table:
            object_names = {name for _, name in objects}
            if args.table not in object_names:
                print(f"ERROR: No existe la tabla/vista: {args.table}", file=sys.stderr)
                print("Usa --list-tables para ver las disponibles.", file=sys.stderr)
                return 1
            objects_to_export = [("table/view", args.table)]
        else:
            objects_to_export = objects

        if not objects_to_export:
            print("No se encontraron tablas para exportar.")
            return 0

        default_output_dir = args.database.with_suffix("").name + "_csv"
        output = args.output or Path(default_output_dir)

        # Si se exporta una sola tabla, --output puede ser archivo .csv.
        single_object = len(objects_to_export) == 1
        output_is_csv_file = single_object and output.suffix.lower() == ".csv"

        if not output_is_csv_file:
            output.mkdir(parents=True, exist_ok=True)

        for _, object_name in objects_to_export:
            if output_is_csv_file:
                csv_path = output
            else:
                csv_path = output / f"{safe_filename(object_name)}.csv"

            print(f"Exportando {object_name} -> {csv_path}")
            rows = export_object_to_csv(
                conn,
                object_name,
                csv_path,
                delimiter=args.delimiter,
                encoding=args.encoding,
            )
            print(f"  OK: {rows:,} filas")

        print("Exportacion completada.")
        return 0

    except sqlite3.DatabaseError as exc:
        print(
            "ERROR: El archivo no parece ser una base SQLite valida, "
            f"o esta dañado/bloqueado: {exc}",
            file=sys.stderr,
        )
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Banco versionado para a skill financas-pessoais."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

DEFAULT_DB = Path(__file__).resolve().parent.parent / "assets" / "financas.db"

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    effective_date TEXT NOT NULL,
    source TEXT NOT NULL,
    note TEXT,
    operation TEXT NOT NULL,
    changed_pointer TEXT,
    document_json TEXT NOT NULL,
    sha256 TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS current_state (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    snapshot_id INTEGER NOT NULL REFERENCES snapshots(id)
);
CREATE INDEX IF NOT EXISTS idx_snapshots_created_at ON snapshots(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_snapshots_effective_date ON snapshots(effective_date DESC);
"""


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(document: Any) -> str:
    return json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(document_json: str) -> str:
    return hashlib.sha256(document_json.encode("utf-8")).hexdigest()


def emit(payload: Any, *, pretty: bool = True) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2 if pretty else None, sort_keys=True))


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    conn.commit()
    os.chmod(path, 0o600)
    return conn


def current_row(conn: sqlite3.Connection) -> sqlite3.Row:
    row = conn.execute(
        """SELECT s.* FROM snapshots s
           JOIN current_state c ON c.snapshot_id = s.id
           WHERE c.singleton = 1"""
    ).fetchone()
    if row is None:
        raise RuntimeError("nenhum snapshot atual no banco")
    return row


def decode_pointer(pointer: str) -> list[str]:
    if pointer == "":
        return []
    if not pointer.startswith("/"):
        raise ValueError("JSON Pointer deve ser vazio ou começar com /")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def resolve(document: Any, pointer: str) -> Any:
    node = document
    for token in decode_pointer(pointer):
        if isinstance(node, list):
            node = node[int(token)]
        elif isinstance(node, dict):
            node = node[token]
        else:
            raise KeyError(f"não é possível atravessar {token!r}")
    return node


def parent_and_token(document: Any, pointer: str) -> tuple[Any, str]:
    tokens = decode_pointer(pointer)
    if not tokens:
        raise ValueError("a raiz não pode ser alterada por set/remove; use import")
    parent = document
    for token in tokens[:-1]:
        if isinstance(parent, list):
            parent = parent[int(token)]
        elif isinstance(parent, dict):
            parent = parent[token]
        else:
            raise KeyError(f"não é possível atravessar {token!r}")
    return parent, tokens[-1]


def validate_document(document: Any) -> None:
    if not isinstance(document, dict):
        raise ValueError("o documento financeiro deve ser um objeto JSON")
    meta = document.get("meta")
    if not isinstance(meta, dict):
        raise ValueError("campo meta ausente ou inválido")
    for field in ("competencia", "atualizado_em", "moeda"):
        if not meta.get(field):
            raise ValueError(f"meta.{field} ausente")


def store_snapshot(
    conn: sqlite3.Connection,
    document: dict[str, Any],
    *,
    effective_date: str,
    source: str,
    note: str | None,
    operation: str,
    changed_pointer: str | None,
) -> tuple[int, str, bool]:
    validate_document(document)
    serialized = canonical_json(document)
    sha = digest(serialized)
    existing = conn.execute("SELECT id FROM snapshots WHERE sha256 = ?", (sha,)).fetchone()
    if existing:
        snapshot_id = int(existing["id"])
        conn.execute(
            "INSERT INTO current_state(singleton, snapshot_id) VALUES(1, ?) "
            "ON CONFLICT(singleton) DO UPDATE SET snapshot_id=excluded.snapshot_id",
            (snapshot_id,),
        )
        conn.commit()
        return snapshot_id, sha, False
    cursor = conn.execute(
        """INSERT INTO snapshots(
               created_at, effective_date, source, note, operation,
               changed_pointer, document_json, sha256
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (now_utc(), effective_date, source, note, operation, changed_pointer, serialized, sha),
    )
    snapshot_id = int(cursor.lastrowid)
    conn.execute(
        "INSERT INTO current_state(singleton, snapshot_id) VALUES(1, ?) "
        "ON CONFLICT(singleton) DO UPDATE SET snapshot_id=excluded.snapshot_id",
        (snapshot_id,),
    )
    conn.commit()
    return snapshot_id, sha, True


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    validate_document(document)
    return document


def cmd_import(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    document = load_json(Path(args.file))
    snapshot_id, sha, created = store_snapshot(
        conn,
        document,
        effective_date=args.effective_date or document["meta"]["atualizado_em"],
        source=args.source,
        note=args.note,
        operation="import",
        changed_pointer=None,
    )
    emit({"ok": True, "snapshot_id": snapshot_id, "sha256": sha, "created": created})


def cmd_get(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = current_row(conn)
    document = json.loads(row["document_json"])
    value = resolve(document, args.pointer)
    emit({
        "ok": True,
        "snapshot_id": row["id"],
        "sha256": row["sha256"],
        "pointer": args.pointer,
        "value": value,
    })


def update_meta(document: dict[str, Any], effective_date: str) -> None:
    document.setdefault("meta", {})["atualizado_em"] = effective_date


def cmd_set(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = current_row(conn)
    document = copy.deepcopy(json.loads(row["document_json"]))
    value = json.loads(args.value)
    parent, token = parent_and_token(document, args.pointer)
    if isinstance(parent, list):
        index = int(token)
        if index == len(parent):
            parent.append(value)
        else:
            parent[index] = value
    elif isinstance(parent, dict):
        parent[token] = value
    else:
        raise ValueError("destino não é objeto nem array")
    update_meta(document, args.effective_date)
    snapshot_id, sha, created = store_snapshot(
        conn,
        document,
        effective_date=args.effective_date,
        source=args.source,
        note=args.note,
        operation="set",
        changed_pointer=args.pointer,
    )
    emit({"ok": True, "snapshot_id": snapshot_id, "sha256": sha, "created": created, "pointer": args.pointer})


def cmd_remove(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = current_row(conn)
    document = copy.deepcopy(json.loads(row["document_json"]))
    parent, token = parent_and_token(document, args.pointer)
    if isinstance(parent, list):
        del parent[int(token)]
    elif isinstance(parent, dict):
        del parent[token]
    else:
        raise ValueError("destino não é objeto nem array")
    update_meta(document, args.effective_date)
    snapshot_id, sha, created = store_snapshot(
        conn,
        document,
        effective_date=args.effective_date,
        source=args.source,
        note=args.note,
        operation="remove",
        changed_pointer=args.pointer,
    )
    emit({"ok": True, "snapshot_id": snapshot_id, "sha256": sha, "created": created, "pointer": args.pointer})


def cmd_history(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    rows = conn.execute(
        """SELECT s.id, s.created_at, s.effective_date, s.source, s.note,
                  s.operation, s.changed_pointer, s.sha256,
                  CASE WHEN c.snapshot_id = s.id THEN 1 ELSE 0 END AS is_current
           FROM snapshots s LEFT JOIN current_state c ON c.singleton = 1
           ORDER BY s.id DESC LIMIT ?""",
        (args.limit,),
    ).fetchall()
    emit({"ok": True, "snapshots": [dict(row) for row in rows]})


def cmd_export(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = current_row(conn)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    document = json.loads(row["document_json"])
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(output, 0o600)
    emit({"ok": True, "snapshot_id": row["id"], "sha256": row["sha256"], "output": str(output.resolve())})


def cmd_summary(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    row = current_row(conn)
    document = json.loads(row["document_json"])
    meta = document.get("meta", {})
    emit({
        "ok": True,
        "snapshot_id": row["id"],
        "sha256": row["sha256"],
        "competencia": meta.get("competencia"),
        "atualizado_em": meta.get("atualizado_em"),
        "moeda": meta.get("moeda"),
        "effective_date": row["effective_date"],
        "sections": sorted(key for key in document if key != "meta"),
        "pending_actions": len(document.get("acoes", {}).get("pendentes", [])),
        "open_gaps": len(document.get("lacunas_abertas", [])),
    })


def cmd_verify(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
    current_count = conn.execute("SELECT COUNT(*) FROM current_state WHERE singleton = 1").fetchone()[0]
    row = current_row(conn)
    document = json.loads(row["document_json"])
    validate_document(document)
    actual_sha = digest(canonical_json(document))
    stored_sha = row["sha256"]
    file_mode = oct(os.stat(args.db).st_mode & 0o777)
    ok = integrity == "ok" and current_count == 1 and actual_sha == stored_sha and file_mode == "0o600"
    emit({
        "ok": ok,
        "integrity": integrity,
        "current_state_rows": current_count,
        "snapshot_id": row["id"],
        "stored_sha256": stored_sha,
        "actual_sha256": actual_sha,
        "hash_matches": actual_sha == stored_sha,
        "db_mode": file_mode,
        "competencia": document["meta"]["competencia"],
        "atualizado_em": document["meta"]["atualizado_em"],
    })
    if not ok:
        raise RuntimeError("verificação do banco falhou")


def add_write_metadata(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--source", required=True)
    parser.add_argument("--effective-date", required=True)
    parser.add_argument("--note")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)

    p_import = sub.add_parser("import")
    p_import.add_argument("file")
    p_import.add_argument("--source", required=True)
    p_import.add_argument("--effective-date")
    p_import.add_argument("--note")
    p_import.set_defaults(func=cmd_import)

    p_get = sub.add_parser("get")
    p_get.add_argument("pointer")
    p_get.set_defaults(func=cmd_get)

    p_set = sub.add_parser("set")
    p_set.add_argument("pointer")
    p_set.add_argument("value")
    add_write_metadata(p_set)
    p_set.set_defaults(func=cmd_set)

    p_remove = sub.add_parser("remove")
    p_remove.add_argument("pointer")
    add_write_metadata(p_remove)
    p_remove.set_defaults(func=cmd_remove)

    p_history = sub.add_parser("history")
    p_history.add_argument("--limit", type=int, default=20)
    p_history.set_defaults(func=cmd_history)

    p_export = sub.add_parser("export")
    p_export.add_argument("--output", required=True)
    p_export.set_defaults(func=cmd_export)

    p_summary = sub.add_parser("summary")
    p_summary.set_defaults(func=cmd_summary)

    p_verify = sub.add_parser("verify")
    p_verify.set_defaults(func=cmd_verify)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.db = Path(args.db).expanduser().resolve()
    try:
        with connect(args.db) as conn:
            args.func(conn, args)
        return 0
    except (OSError, sqlite3.Error, ValueError, KeyError, IndexError, RuntimeError, json.JSONDecodeError) as exc:
        emit({"ok": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "assets" / "financas.db"
CLI = ROOT / "scripts" / "finance_db.py"
OUT = Path.home() / "relatorios-financeiros"

FATURA_KEYS = (
    "fatura_atual",
    "fatura_aberta",
    "fatura_setembro",
    "fatura_agosto",
    "fatura_julho",
)
TOTAL_KEYS = (
    "total_atual",
    "total",
    "valor_atual",
    "valor_total",
    "total_exibido",
    "total_exibido_banco",
    "total_exibido_nubank",
    "total_exibido_bradesco",
)


def get(pointer: str) -> Any:
    r = subprocess.run(
        [sys.executable, str(CLI), "--db", str(DB), "get", pointer],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(r.stdout)["value"]


def verify() -> dict[str, Any]:
    r = subprocess.run(
        [sys.executable, str(CLI), "--db", str(DB), "verify"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(r.stdout)


def money(v: Any) -> str:
    if v is None or v == "":
        return "não informado"
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return html.escape(str(v))


def card_label(card: dict[str, Any]) -> str:
    for key in ("nome", "nome_cartao", "descricao", "banco", "id"):
        if card.get(key):
            return str(card[key])
    return "cartão sem nome"


def invoice_from_card(card: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    for key in FATURA_KEYS:
        value = card.get(key)
        if isinstance(value, dict):
            return key, value
    for key, value in card.items():
        if key.startswith("fatura_") and isinstance(value, dict):
            return key, value
    return "", None


def total_from_invoice(invoice: dict[str, Any] | None) -> Any:
    if not isinstance(invoice, dict):
        return None
    for key in TOTAL_KEYS:
        value = invoice.get(key)
        if value is not None:
            return value
    lancamentos = invoice.get("lancamentos") or invoice.get("itens") or invoice.get("compras")
    if isinstance(lancamentos, list):
        total = 0.0
        found = False
        for item in lancamentos:
            if isinstance(item, dict) and item.get("valor") is not None:
                total += float(item["valor"])
                found = True
        if found:
            return round(total, 2)
    return None


def invoice_meta(invoice: dict[str, Any] | None) -> str:
    if not isinstance(invoice, dict):
        return ""
    pieces = []
    if invoice.get("competencia"):
        pieces.append(f"competência {invoice['competencia']}")
    if invoice.get("fecha_dia") or invoice.get("fechamento"):
        pieces.append(f"fecha {invoice.get('fecha_dia') or invoice.get('fechamento')}")
    if invoice.get("vence_dia") or invoice.get("vencimento"):
        pieces.append(f"vence {invoice.get('vence_dia') or invoice.get('vencimento')}")
    return " · ".join(html.escape(str(p)) for p in pieces)


def main() -> None:
    proof = verify()
    doc = get("")
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"relatorio-financeiro-{date.today().isoformat()}.html"

    cartoes = doc.get("cartoes", [])
    contas = doc.get("contas", {})
    lacunas = doc.get("lacunas_abertas", [])

    body = ["<h1>Relatório financeiro semanal</h1>"]
    body.append(f"<p><b>Competência:</b> {html.escape(str(doc.get('meta', {}).get('competencia')))}</p>")
    body.append(f"<p><b>Snapshot:</b> {proof['snapshot_id']}<br><b>Hash:</b> {proof['actual_sha256']}</p>")
    body.append("<h2>Contas</h2><pre>" + html.escape(json.dumps(contas, ensure_ascii=False, indent=2)) + "</pre>")

    body.append("<h2>Cartões</h2><ul>")
    for card in cartoes:
        if not isinstance(card, dict):
            body.append(f"<li>{html.escape(str(card))}</li>")
            continue
        invoice_key, invoice = invoice_from_card(card)
        total = total_from_invoice(invoice)
        label = html.escape(card_label(card))
        meta = invoice_meta(invoice)
        suffix = f" <small>({html.escape(invoice_key)}{': ' + meta if meta else ''})</small>" if invoice_key else " <small>(sem fatura atual encontrada)</small>"
        body.append(f"<li>{label}: {money(total)}{suffix}</li>")
    body.append("</ul>")

    body.append("<h2>Lacunas abertas</h2><pre>" + html.escape(json.dumps(lacunas, ensure_ascii=False, indent=2)) + "</pre>")
    path.write_text(
        "<!doctype html><meta charset='utf-8'><style>body{font-family:system-ui;max-width:960px;margin:40px auto;line-height:1.45}pre{background:#f6f6f6;padding:16px;border-radius:8px;overflow:auto}small{color:#555}</style>"
        + "\n".join(body),
        encoding="utf-8",
    )
    print(json.dumps({"ok": True, "output": str(path), "snapshot_id": proof["snapshot_id"], "sha256": proof["actual_sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

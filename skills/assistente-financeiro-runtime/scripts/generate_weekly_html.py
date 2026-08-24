#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "assets" / "financas.db"
CLI = ROOT / "scripts" / "finance_db.py"
OUT = Path.home() / "relatorios-financeiros"
TZ = ZoneInfo("America/Sao_Paulo")

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
    "total_pagar",
    "total_parcial",
    "total_exibido",
    "total_exibido_banco",
    "total_exibido_nubank",
    "total_exibido_bradesco",
)
ITEM_KEYS = (
    "lancamentos",
    "itens",
    "compras",
    "despesas",
    "parcelamentos",
    "creditos",
)

STYLE = """
:root{--bg:#09111f;--card:#101c30;--line:#263856;--txt:#edf4ff;--muted:#9eb0ca;--cyan:#44d7c6;--amber:#ffc66d;--red:#ff8e99;--green:#8ff0ad}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 10% 0,#173454,transparent 35%),var(--bg);color:var(--txt);font:15px/1.45 Inter,system-ui,sans-serif}main{max-width:1280px;margin:auto;padding:28px 18px 52px}h1{font-size:clamp(26px,4vw,43px);margin:0 0 4px}h2{font-size:20px;margin:0 0 14px}h3{font-size:16px;margin:16px 0 10px}p,.sub{color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:14px;margin:22px 0}.card,details{background:rgba(16,28,48,.94);border:1px solid var(--line);border-radius:14px;padding:18px}.value{font-size:29px;font-weight:750;margin:4px 0}.accent{color:var(--cyan)}.warn{color:var(--amber)}.danger{color:var(--red)}.ok{color:var(--green)}section{margin-top:25px}.scroll{overflow:auto;border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%;min-width:620px}th,td{padding:10px 11px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}th{background:#14243d;color:#c6d7ef;font-size:12px;text-transform:uppercase;letter-spacing:.04em}.tag{display:inline-block;padding:3px 8px;border-radius:999px;background:#1a3552;color:#8de9dd;font-size:12px}.notice{border-left:3px solid var(--amber);padding-left:12px;color:#f3d8a1}.empty{color:var(--muted);font-style:italic}.small{font-size:12px;color:var(--muted)}footer{margin-top:32px;border-top:1px solid var(--line);padding-top:16px}@media(max-width:600px){main{padding:19px 12px}.card,details{padding:14px}.value{font-size:25px}}
""".strip()


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


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def money(value: Any) -> str:
    if value is None or value == "":
        return "não informado"
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return esc(value)


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    return []


def first_present(data: dict[str, Any], keys: tuple[str, ...] | list[str]) -> Any:
    for key in keys:
        if isinstance(data, dict) and data.get(key) not in (None, ""):
            return data.get(key)
    return None


def card_label(card: dict[str, Any]) -> str:
    return str(first_present(card, ("nome", "nome_cartao", "descricao", "banco", "id")) or "cartão sem nome")


def scope_label(item: dict[str, Any]) -> str:
    value = first_present(item, ("escopo", "conta_pagadora", "tipo_conta"))
    return str(value).upper() if value else ""


def invoice_from_card(card: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    for key in FATURA_KEYS:
        value = card.get(key)
        if isinstance(value, dict):
            return key, value
        if isinstance(value, (int, float, str)) and value not in ("", None):
            return key, {"total_atual": value, "status": "valor informado sem detalhamento de fatura"}
    candidates = [(key, value) for key, value in card.items() if key.startswith("fatura_") and isinstance(value, dict)]
    if candidates:
        return sorted(candidates)[-1]
    detailed = card.get("faturas_detalhadas")
    if isinstance(detailed, list) and detailed:
        invoice = detailed[-1]
        if isinstance(invoice, dict):
            return "faturas_detalhadas", invoice
    return "", None


def items_from_invoice(invoice: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(invoice, dict):
        return []
    rows: list[dict[str, Any]] = []
    for key in ITEM_KEYS:
        for item in as_list(invoice.get(key)):
            if isinstance(item, dict):
                row = dict(item)
                row.setdefault("grupo", key)
                rows.append(row)
    return rows


def total_from_rows(rows: list[dict[str, Any]]) -> float | None:
    total = 0.0
    found = False
    for item in rows:
        value = item.get("valor")
        if value is not None:
            try:
                total += float(value)
                found = True
            except Exception:
                pass
    return round(total, 2) if found else None


def total_from_invoice(invoice: dict[str, Any] | None) -> Any:
    if not isinstance(invoice, dict):
        return None
    for key in TOTAL_KEYS:
        value = invoice.get(key)
        if value is not None:
            return value
    rows = items_from_invoice(invoice)
    return total_from_rows(rows)


def invoice_status(invoice: dict[str, Any] | None) -> str:
    if not isinstance(invoice, dict):
        return "sem fatura atual encontrada"
    return str(first_present(invoice, ("status_reconciliacao", "status", "confianca", "fonte", "evidencia")) or "fatura sem status informado")


def invoice_due(card: dict[str, Any], invoice: dict[str, Any] | None) -> str:
    if isinstance(invoice, dict):
        value = first_present(invoice, ("vencimento", "vence_dia", "data_vencimento"))
        if value:
            return str(value)
    value = first_present(card, ("vence_dia", "vencimento", "data_vencimento"))
    return str(value) if value else "não informado"


def invoice_close(card: dict[str, Any], invoice: dict[str, Any] | None) -> str:
    if isinstance(invoice, dict):
        value = first_present(invoice, ("fechamento", "fecha_dia", "data_fechamento"))
        if value:
            return str(value)
    value = first_present(card, ("fecha_dia", "fechamento", "data_fechamento"))
    return str(value) if value else "não informado"


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return "<p class='empty'>Sem dados registrados nesta seção.</p>"
    thead = "".join(f"<th>{esc(h)}</th>" for h in headers)
    trs = []
    for row in rows:
        trs.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    return "<div class='scroll'><table><thead><tr>" + thead + "</tr></thead><tbody>" + "".join(trs) + "</tbody></table></div>"


def render_card_kpis(cards: list[dict[str, Any]]) -> str:
    if not cards:
        return "<p class='empty'>Nenhum cartão registrado.</p>"
    out = ["<div class='grid'>"]
    for card in cards:
        key, invoice = invoice_from_card(card)
        total = total_from_invoice(invoice)
        status = invoice_status(invoice)
        due = invoice_due(card, invoice)
        css = "accent" if total not in (None, "") else "warn"
        subtitle = card_label(card)
        if scope_label(card):
            subtitle += f", {scope_label(card)}"
        out.append(
            "<article class='card'>"
            f"<div class='sub'>{esc(subtitle)}</div>"
            f"<div class='value {css}'>{money(total)}</div>"
            f"<div>Vence: {esc(due)}. Fonte: {esc(key or 'não informada')}</div>"
            f"<p class='small'>{esc(status)}</p>"
            "</article>"
        )
    out.append("</div>")
    return "".join(out)


def row_value(item: dict[str, Any], keys: tuple[str, ...]) -> str:
    value = first_present(item, keys)
    return esc(value)


def render_invoice_section(card: dict[str, Any]) -> str:
    key, invoice = invoice_from_card(card)
    title = card_label(card)
    total = total_from_invoice(invoice)
    rows = []
    for item in items_from_invoice(invoice):
        rows.append([
            row_value(item, ("data", "em", "date")),
            row_value(item, ("descricao", "lançamento", "lancamento", "nome")),
            row_value(item, ("categoria", "tipo", "grupo", "status")),
            money(item.get("valor")),
            row_value(item, ("evidencia", "status", "fonte", "observacao")),
        ])
    notice = invoice_status(invoice)
    meta = f"Total: {money(total)}. Fecha: {esc(invoice_close(card, invoice))}. Vence: {esc(invoice_due(card, invoice))}. Campo: {esc(key or 'não encontrado')}."
    return (
        f"<section><h2>{esc(title)}, fatura detalhada</h2>"
        f"<p class='notice'>{esc(notice)}</p>"
        f"<p class='sub'>{meta}</p>"
        + render_table(["Data", "Lançamento", "Categoria", "Valor", "Evidência"], rows)
        + "</section>"
    )


def recurring_items(doc: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("custo_fixo_mensal", "despesas_recorrentes", "recorrencias", "assinaturas"):
        value = doc.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
        if isinstance(value, dict):
            return [x for x in value.values() if isinstance(x, dict)]
    return []


def render_recurring(doc: dict[str, Any]) -> str:
    rows = []
    for item in recurring_items(doc):
        rows.append([
            row_value(item, ("descricao", "item", "nome")),
            row_value(item, ("escopo", "conta", "conta_pagadora", "cartao")),
            money(first_present(item, ("valor_mensal", "valor", "total"))),
            row_value(item, ("status", "observacao", "evidencia", "vencimento")),
        ])
    return "<section id='gastos-fixos'><h2>Gastos fixos mensais</h2>" + render_table(["Item", "Conta", "Valor mensal", "Status ou observação"], rows) + "</section>"


def render_accounts(doc: dict[str, Any]) -> str:
    contas_value = doc.get("contas")
    contas: dict[str, Any] = contas_value if isinstance(contas_value, dict) else {}
    rows = []
    for scope in ("pf", "pj"):
        for account in as_list(contas.get(scope)):
            if isinstance(account, dict):
                rows.append([
                    esc(scope.upper()),
                    row_value(account, ("banco", "nome", "nome_conta")),
                    row_value(account, ("tipo_conta", "tipo")),
                    money(first_present(account, ("saldo_atual", "saldo", "valor"))),
                    row_value(account, ("data_saldo", "atualizado_em", "evidencia")),
                ])
    return "<section><h2>Contas</h2>" + render_table(["Escopo", "Banco", "Tipo", "Saldo", "Data ou evidência"], rows) + "</section>"


def pending_actions(doc: dict[str, Any]) -> list[str]:
    actions = []
    acoes_value = doc.get("acoes")
    acoes: dict[str, Any] = acoes_value if isinstance(acoes_value, dict) else {}
    for item in as_list(acoes.get("pendentes")):
        if isinstance(item, dict):
            text = first_present(item, ("acao", "descricao", "titulo", "question"))
            if text:
                actions.append(str(text))
        elif item:
            actions.append(str(item))
    for gap in as_list(doc.get("lacunas_abertas")):
        if isinstance(gap, dict):
            text = first_present(gap, ("question", "descricao", "id"))
            if text:
                actions.append(str(text))
        elif gap:
            actions.append(str(gap))
    return actions[:3]


def render_next_actions(doc: dict[str, Any]) -> str:
    actions = pending_actions(doc)
    if not actions:
        return "<section><h2>Próximas ações físicas</h2><p class='empty'>Nenhuma ação pendente registrada.</p></section>"
    lis = "".join(f"<li>{esc(action)}</li>" for action in actions)
    return f"<section><h2>Próximas ações físicas</h2><ol>{lis}</ol></section>"


def render_lacunas(doc: dict[str, Any]) -> str:
    gaps = as_list(doc.get("lacunas_abertas"))
    rows = []
    for gap in gaps:
        if isinstance(gap, dict):
            rows.append([
                row_value(gap, ("id", "state", "fase")),
                row_value(gap, ("question", "descricao", "motivo")),
                row_value(gap, ("status", "blocks_exit_gate")),
            ])
        else:
            rows.append(["", esc(gap), ""])
    return "<section><h2>Lacunas abertas</h2>" + render_table(["ID ou fase", "Lacuna", "Status"], rows) + "</section>"


def main() -> None:
    proof = verify()
    doc = get("")
    now = datetime.now(TZ)
    meta = doc.get("meta", {}) if isinstance(doc, dict) else {}
    competencia = meta.get("competencia", "não informada")
    atualizado_em = meta.get("atualizado_em", "não informado")
    cards = [c for c in as_list(doc.get("cartoes")) if isinstance(c, dict)]

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"relatorio-financeiro-{now.date().isoformat()}.html"

    parts = [
        "<!doctype html>",
        "<html lang='pt-BR'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>",
        f"<title>Painel financeiro, {esc(competencia)}</title><style>{STYLE}</style></head><body><main>",
        "<header>",
        f"<p class='sub'>Competência {esc(competencia)}, estado canônico atualizado em {esc(atualizado_em)}</p>",
        "<h1>Painel financeiro</h1>",
        "<p>Projeção operacional, não substitui extrato. Valores e nível de evidência preservados da fonte canônica do aluno.</p>",
        f"<p class='small'>Snapshot {esc(proof.get('snapshot_id'))}, hash {esc(proof.get('actual_sha256'))}</p>",
        "</header>",
        render_card_kpis(cards),
        render_accounts(doc),
    ]
    parts.extend(render_invoice_section(card) for card in cards)
    parts.extend([
        render_recurring(doc),
        render_lacunas(doc),
        render_next_actions(doc),
        f"<footer><p class='sub'>Fonte: snapshot financeiro {esc(competencia)}, atualização {esc(atualizado_em)}. Painel calculado em {now.strftime('%d/%m/%Y, %H:%M')} America/Sao_Paulo.</p></footer>",
        "</main></body></html>",
    ])
    path.write_text("".join(parts), encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(path), "snapshot_id": proof["snapshot_id"], "sha256": proof["actual_sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

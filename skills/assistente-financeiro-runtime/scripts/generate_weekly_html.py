#!/usr/bin/env python3
from __future__ import annotations
import html, json, subprocess, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'assets' / 'financas.db'
CLI = ROOT / 'scripts' / 'finance_db.py'
OUT = Path.home() / 'relatorios-financeiros'

def get(pointer):
    r = subprocess.run([sys.executable, str(CLI), '--db', str(DB), 'get', pointer], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)['value']

def verify():
    r = subprocess.run([sys.executable, str(CLI), '--db', str(DB), 'verify'], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)

def money(v):
    try:
        return f"R$ {float(v):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except Exception:
        return html.escape(str(v))

def main():
    proof = verify()
    doc = get('')
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"relatorio-financeiro-{date.today().isoformat()}.html"
    cartoes = doc.get('cartoes', [])
    contas = doc.get('contas', {})
    lacunas = doc.get('lacunas_abertas', [])
    body = ["<h1>Relatório financeiro semanal</h1>"]
    body.append(f"<p><b>Competência:</b> {html.escape(str(doc.get('meta', {}).get('competencia')))}</p>")
    body.append(f"<p><b>Snapshot:</b> {proof['snapshot_id']}<br><b>Hash:</b> {proof['actual_sha256']}</p>")
    body.append("<h2>Contas</h2><pre>" + html.escape(json.dumps(contas, ensure_ascii=False, indent=2)) + "</pre>")
    body.append("<h2>Cartões</h2><ul>")
    for c in cartoes:
        total = c.get('fatura_setembro', {}).get('total_atual') or c.get('fatura_setembro', {}).get('total') or c.get('fatura_agosto')
        body.append(f"<li>{html.escape(str(c.get('nome', c.get('id'))))}: {money(total)}</li>")
    body.append("</ul>")
    body.append("<h2>Lacunas abertas</h2><pre>" + html.escape(json.dumps(lacunas, ensure_ascii=False, indent=2)) + "</pre>")
    path.write_text("<!doctype html><meta charset='utf-8'><style>body{font-family:system-ui;max-width:960px;margin:40px auto;line-height:1.45}pre{background:#f6f6f6;padding:16px;border-radius:8px;overflow:auto}</style>" + "\n".join(body), encoding='utf-8')
    print(json.dumps({'ok': True, 'output': str(path), 'snapshot_id': proof['snapshot_id'], 'sha256': proof['actual_sha256']}, ensure_ascii=False))

if __name__ == '__main__':
    main()

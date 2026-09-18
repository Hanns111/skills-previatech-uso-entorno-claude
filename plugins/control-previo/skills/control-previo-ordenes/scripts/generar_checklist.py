#!/usr/bin/env python3
"""
generar_checklist.py — Genera el INFORME_CONTROL_PREVIO_<EXPEDIENTE>.xlsx

Uso:
    python3 generar_checklist.py <carpeta_expediente> <datos_json>

<datos_json> es la ruta a un JSON con la estructura:
{
  "expediente": "DIFODS2026-INT-0188724",
  "ue": "026",
  "tipo_contratacion": "CM",
  "orden": "OS 1703-2026",
  "carta_contrato": "-",
  "proveedor": "QUEZADA BARRIOS LIDIA ROSA DEL MILAGRO",
  "ruc": "10XXXXXXXXX",
  "monto_total": 7500.00,
  "n_armadas": 3,
  "armada_actual": 1,
  "monto_armada": 2500.00,
  "fecha_inicio": "02/03/2026",
  "fecha_fin": "31/03/2026",
  "fecha_entregable": "30/03/2026",
  "fecha_conformidad": "31/03/2026",
  "veredicto": "No hay observaciones",
  "observaciones": [],
  "checklist": [
    {"item": "TDR firmado", "estado": "PRESENTE", "archivo": "TDR.pdf",
     "pagina": "1-5", "aplica_armada": "1ra", "comentario": ""},
    ...
  ],
  "coherencia": [
    {"campo": "Proveedor", "valor_doc1": "QUEZADA...", "doc1": "TDR",
     "valor_doc2": "QUEZADA...", "doc2": "Proveído", "resultado": "OK"},
    ...
  ],
  "tributario": {
    "comprobante": "RHE E001-41",
    "fecha": "30/03/2026",
    "importe": 2500.00,
    "retencion_8": 0.00,
    "constancia_1609": "AUTORIZADO 13/02/2026 op.26694681",
    "constancia_archivo": "e3f18b07-...pdf",
    "constancia_pagina": 23,
    "resultado": "CONFORME"
  }
}

Salida: <carpeta_expediente>/INFORME_CONTROL_PREVIO_<expediente>.xlsx
"""
import json, sys, os, re, argparse, urllib.parse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

LINK_FONT = Font(color="0563C1", underline="single")

def first_page(p):
    if p is None: return None
    s = str(p).strip()
    m = re.search(r"\d+", s)
    return int(m.group()) if m else None

def build_link(host_base, archivo, pagina):
    """Construye un hyperlink file:///<ruta>/<archivo>#page=N
    URL-encodeando espacios y caracteres especiales para que Adobe/Foxit
    abran el PDF EXACTAMENTE en la página indicada."""
    if not host_base or not archivo: return None
    n = first_page(pagina)
    base = host_base.replace("\\", "/")
    if not base.endswith("/"): base += "/"
    # URL-encode preservando "/" y ":"
    base_q = urllib.parse.quote(base, safe="/:")
    arch_q = urllib.parse.quote(archivo, safe="/:")
    if base.startswith("/"):
        url = "file://" + base_q + arch_q
    else:
        url = "file:///" + base_q + arch_q
    if n: url += f"#page={n}"
    return url

# ----------------------------------------------------------------------------
# Orden canónico del checklist exigido por el usuario (Hans, v9.4)
# Cada entrada: (clave_regex, prioridad, exigible_en_default)
# Cuanto MENOR la prioridad, más arriba aparece el ítem.
# ----------------------------------------------------------------------------
ORDEN_CANONICO = [
    (r"prove[ií]do.*deveng",                    10),
    (r"informe.*conformidad|conformidad.*\barea\b|conformidad\b", 20),
    (r"informe.*t[eé]cnico",                    25),
    (r"constancia.*recepci[oó]n",               30),
    (r"certificaci[oó]n.*presup|cci",           40),
    (r"compromiso.*pago|certificaci[oó]n.*compromiso", 50),
    (r"suspensi[oó]n.*4ta|suspensi[oó]n.*cuarta|form\.?\s*1609|constancia.*1609", 60),
    (r"recibo.*honor|rhe\b",                    70),
    (r"factura|comprobante.*pago",              71),
    (r"orden.*servicio|orden.*compra|\bos\b|\boc\b", 80),
    (r"carta.*contrato",                        85),
    (r"entregable|informe.*activid",            90),
    (r"tdr|t[eé]rminos.*referencia",            100),
    (r"propuesta.*econ[oó]mica",                110),
    (r"anexo",                                  120),
    (r"penalidad",                              130),
]

def prioridad(item_name):
    n = (item_name or "").lower()
    for pat, pri in ORDEN_CANONICO:
        if re.search(pat, n):
            return pri
    return 999

VERDE = PatternFill("solid", fgColor="C6EFCE")
ROJO  = PatternFill("solid", fgColor="FFC7CE")
AMAR  = PatternFill("solid", fgColor="FFEB9C")
HEAD  = PatternFill("solid", fgColor="305496")
HEADF = Font(bold=True, color="FFFFFF")
BORDER = Border(*[Side(style="thin", color="999999")]*4)

def color_estado(estado):
    e = (estado or "").upper()
    if e in ("PRESENTE","OK","CONFORME","CONSISTENTE","SI","SÍ"): return VERDE
    if e in ("AUSENTE","NO","INCONSISTENTE","OBSERVABLE","FALTA"): return ROJO
    if e in ("INCOMPLETO","PARCIAL","N.A.","NA","REVISAR"): return AMAR
    return None

def write_header(ws, headers, row=1):
    for j, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.fill = HEAD; c.font = HEADF
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER

def autosize(ws, max_w=60):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        length = max((len(str(c.value)) for c in col if c.value is not None), default=10)
        ws.column_dimensions[col_letter].width = min(max(length+2, 12), max_w)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta", help="VM path de la carpeta del expediente (donde se guarda el xlsx)")
    ap.add_argument("datos", help="Ruta al JSON con los datos del expediente")
    ap.add_argument("--host-base", default=None, help="Ruta HOST (Windows) de la carpeta del expediente para construir hyperlinks file:///")
    args = ap.parse_args()
    carpeta = args.carpeta
    host_base = args.host_base
    with open(args.datos, encoding="utf-8") as f:
        d = json.load(f)

    wb = Workbook()

    # Hoja 1: Datos del expediente
    ws = wb.active; ws.title = "Datos Expediente"
    pares = [
        ("Expediente", d.get("expediente","")),
        ("Unidad Ejecutora", d.get("ue","")),
        ("Tipo de contratación", d.get("tipo_contratacion","")),
        ("Orden de Servicio/Compra", d.get("orden","")),
        ("Carta Contrato", d.get("carta_contrato","")),
        ("Proveedor", d.get("proveedor","")),
        ("RUC", d.get("ruc","")),
        ("Monto total contractual (S/)", d.get("monto_total","")),
        ("Número de armadas", d.get("n_armadas","")),
        ("Armada en revisión", f"{d.get('armada_actual','')} de {d.get('n_armadas','')}"),
        ("Monto de la armada (S/)", d.get("monto_armada","")),
        ("Fecha inicio armada", d.get("fecha_inicio","")),
        ("Fecha fin armada", d.get("fecha_fin","")),
        ("Fecha de entregable", d.get("fecha_entregable","")),
        ("Fecha de conformidad", d.get("fecha_conformidad","")),
        ("VEREDICTO", d.get("veredicto","")),
    ]
    for i,(k,v) in enumerate(pares, 1):
        a = ws.cell(row=i, column=1, value=k); a.font = Font(bold=True); a.fill = HEAD; a.font = HEADF
        b = ws.cell(row=i, column=2, value=v); b.alignment = Alignment(wrap_text=True)
        if k == "VEREDICTO":
            b.fill = VERDE if "No hay" in str(v) else ROJO
            b.font = Font(bold=True)
    autosize(ws)

    # Hoja 2: Checklist documental — filtrado por la armada actual
    ws = wb.create_sheet("Checklist Documental")
    headers = ["#","Documento requerido","Estado","Archivo (clic para abrir)","Página","Exigible en","Firma","Comentario"]
    write_header(ws, headers)

    armada_actual = int(d.get("armada_actual", 1) or 1)
    items = d.get("checklist", [])

    def _exig(it):
        # v9.7 — acepta ambos nombres de campo: exigible_en | aplica_armada
        return (it.get("exigible_en","") or it.get("aplica_armada","") or "").lower()

    def es_base(it):
        v = _exig(it)
        return v in ("1ra","base","primera","primer pago","solo 1ra")

    def es_por_armada(it):
        v = _exig(it)
        return v in ("cada armada","todas","por armada","actual","siempre","cada_armada")

    if armada_actual == 1:
        base = [it for it in items if es_base(it)]
        porarmada = [it for it in items if es_por_armada(it)]
    else:
        base = []  # en armadas posteriores NO se muestran los base
        porarmada = [it for it in items if es_por_armada(it)]
    otros = [it for it in items if it not in base and it not in porarmada]

    # v9.4 — Orden canónico exigido por el usuario
    porarmada.sort(key=lambda it: prioridad(it.get("item","")))
    base.sort(key=lambda it: prioridad(it.get("item","")))
    otros.sort(key=lambda it: prioridad(it.get("item","")))

    row = 2
    def write_section(title, rows):
        nonlocal row
        sc = ws.cell(row=row, column=1, value=title)
        sc.font = Font(bold=True, color="FFFFFF")
        sc.fill = PatternFill("solid", fgColor="8497B0")
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=8)
        sc.alignment = Alignment(horizontal="left", vertical="center")
        row += 1
        for n, item in enumerate(rows, 1):
            es = (item.get("estado","") or "").upper()
            row_red = es in ("AUSENTE","OBSERVABLE","FALTA","NO","INCONSISTENTE")
            ws.cell(row=row, column=1, value=n)
            ws.cell(row=row, column=2, value=item.get("item",""))
            c = ws.cell(row=row, column=3, value=item.get("estado",""))
            fcol = color_estado(item.get("estado",""))
            if fcol: c.fill = fcol
            archivo = item.get("archivo","") or "—"
            ac = ws.cell(row=row, column=4, value=archivo)
            link = build_link(host_base, item.get("archivo",""), item.get("pagina",""))
            if link:
                ac.hyperlink = link
                ac.font = LINK_FONT
            ws.cell(row=row, column=5, value=str(item.get("pagina","")))
            ws.cell(row=row, column=6, value=item.get("exigible_en","") or item.get("aplica_armada",""))
            firma = ws.cell(row=row, column=7, value=item.get("firma",""))
            ff = color_estado(item.get("firma",""))
            if ff: firma.fill = ff
            ws.cell(row=row, column=8, value=item.get("comentario",""))
            for j in range(1,9):
                cc = ws.cell(row=row, column=j)
                cc.border = BORDER
                cc.alignment = Alignment(wrap_text=True, vertical="top")
                if row_red and j != 4:  # no pisar el hyperlink azul
                    cc.fill = ROJO
            row += 1
        row += 1  # blank line

    if armada_actual == 1:
        # En 1ra armada: el orden canónico se aplica sobre TODOS los ítems
        # (porarmada + base) en una sola sección, según pidió el usuario:
        # 1.Proveído 2.Conformidad 3.Constancia recepción 4.Certificación
        # 5.Compromiso 6.Suspensión/RHE/Factura 7.OS/OC … resto abajo.
        unificado = sorted(porarmada + base, key=lambda it: prioridad(it.get("item","")))
        write_section(f"PRIMER PAGO (1RA ARMADA) — orden canónico de revisión", unificado)
        if otros:
            write_section("OTROS DOCUMENTOS", otros)
    else:
        write_section(f"DOCUMENTOS EXIGIBLES PARA LA ARMADA {armada_actual} (pago siguiente — revisión simplificada, orden canónico)", porarmada)
    autosize(ws)

    # Hoja 2-bis: Accesos rápidos a documentos clave
    ws = wb.create_sheet("Accesos rápidos")
    write_header(ws, ["Documento clave","Archivo (clic para abrir)","Página"])
    claves = d.get("accesos_rapidos", [])
    for i, k in enumerate(claves, 1):
        ws.cell(row=i+1, column=1, value=k.get("doc",""))
        archivo = k.get("archivo","") or "—"
        ac = ws.cell(row=i+1, column=2, value=archivo)
        link = build_link(host_base, k.get("archivo",""), k.get("pagina",""))
        if link:
            ac.hyperlink = link
            ac.font = LINK_FONT
        ws.cell(row=i+1, column=3, value=str(k.get("pagina","")))
        for j in range(1,4):
            ws.cell(row=i+1, column=j).border = BORDER
    autosize(ws)

    # Hoja 3: Coherencia documental
    ws = wb.create_sheet("Coherencia")
    headers = ["Campo","Valor Doc 1","Doc 1","Valor Doc 2","Doc 2","Resultado"]
    write_header(ws, headers)
    for i, row in enumerate(d.get("coherencia", []), 1):
        ws.cell(row=i+1, column=1, value=row.get("campo",""))
        ws.cell(row=i+1, column=2, value=row.get("valor_doc1",""))
        ws.cell(row=i+1, column=3, value=row.get("doc1",""))
        ws.cell(row=i+1, column=4, value=row.get("valor_doc2",""))
        ws.cell(row=i+1, column=5, value=row.get("doc2",""))
        c = ws.cell(row=i+1, column=6, value=row.get("resultado",""))
        f = color_estado(row.get("resultado",""))
        if f: c.fill = f
        for j in range(1,7):
            ws.cell(row=i+1, column=j).border = BORDER
            ws.cell(row=i+1, column=j).alignment = Alignment(wrap_text=True, vertical="top")
    autosize(ws)

    # Hoja 4: Verificación tributaria
    ws = wb.create_sheet("Tributario")
    t = d.get("tributario", {})
    pares = [
        ("Comprobante", t.get("comprobante","")),
        ("Fecha de emisión", t.get("fecha","")),
        ("Importe (S/)", t.get("importe","")),
        ("Condición de pago (al contado / al crédito)", t.get("condicion_pago","")),
        ("¿Aplica retención 8% IR?", t.get("aplica_retencion","")),
        ("Retención 8% IR (S/)", t.get("retencion_8","")),
        ("Constancia Suspensión 1609 (Form. 1609)", t.get("constancia_1609","")),
        ("Archivo Constancia", t.get("constancia_archivo","")),
        ("Página Constancia", t.get("constancia_pagina","")),
        ("¿Aplica detracción?", t.get("aplica_detraccion","")),
        ("Tasa de detracción (%)", t.get("tasa_detraccion","")),
        ("Monto detracción (S/)", t.get("monto_detraccion","")),
        ("Constancia de depósito de detracción", t.get("constancia_detraccion","")),
        ("Resultado tributario", t.get("resultado","")),
    ]
    for i,(k,v) in enumerate(pares, 1):
        a = ws.cell(row=i, column=1, value=k); a.fill = HEAD; a.font = HEADF
        b = ws.cell(row=i, column=2, value=v)
        if k == "Resultado tributario":
            f = color_estado(v)
            if f: b.fill = f
    autosize(ws)

    # Hoja 5: Observaciones
    ws = wb.create_sheet("Observaciones")
    write_header(ws, ["#","Observación","Fundamento","Gravedad"])
    obs = d.get("observaciones", [])
    if not obs:
        c = ws.cell(row=2, column=1, value="—")
        ws.cell(row=2, column=2, value="No hay observaciones").fill = VERDE
    else:
        for i, o in enumerate(obs, 1):
            ws.cell(row=i+1, column=1, value=i)
            ws.cell(row=i+1, column=2, value=o.get("descripcion","")).fill = ROJO
            ws.cell(row=i+1, column=3, value=o.get("fundamento",""))
            ws.cell(row=i+1, column=4, value=o.get("gravedad",""))
    autosize(ws)

    out = os.path.join(carpeta, f"INFORME_CONTROL_PREVIO_{d.get('expediente','EXP')}.xlsx")
    wb.save(out)
    print(out)

if __name__ == "__main__":
    main()

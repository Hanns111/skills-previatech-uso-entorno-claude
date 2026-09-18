---
name: informe-control-previo-minedu
description: "Genera el informe Excel de control previo del MINEDU en formato de dos hojas, Dictamen y Expediente, para encargos a personal, caja chica, convenios, servicios básicos, tasas, sentencias judiciales y demás expedientes de pago. NO aplica a Órdenes de Servicio ni Órdenes de Compra, que usan el Protocolo v1.1 de siete hojas de informe-control-previo-os-oc, ni a viáticos, que tienen su propio formato oficial de tres hojas."
---

# Informe de Control Previo MINEDU — formato de dos hojas

## Enrutador MINEDU — qué skill manda en cada expediente

La norma y el criterio los pone la **skill de dominio**. El formato del Excel lo pone la **skill de salida**. Ninguna reemplaza a otra ni borra las normas de otra: se suman.

| Tipo de expediente | Dominio: norma y criterio | Salida: formato del informe |
|---|---|---|
| Orden de Servicio y Orden de Compra | `control-previo-ordenes` | `informe-control-previo-os-oc` — siete hojas, Protocolo v1.1 |
| Rendición de viáticos | `control-previo-viaticos-v3` | la propia skill — tres hojas, formato oficial v7.0 |
| Encargos a personal | `control-previo-encargos` | `informe-control-previo-minedu` — dos hojas |
| Caja chica | `control-previo-caja-chica` | `informe-control-previo-minedu` — dos hojas |
| Convenios, servicios básicos, tasas, sentencias judiciales | criterio de la especialidad | `informe-control-previo-minedu` — dos hojas |

Transversales, se aplican encima de cualquiera de las anteriores: `deteccion-firmas-expedientes` y `coherencia-documental-expedientes`.

Regla de desempate: si dos skills de salida pudieran activarse, manda la de la fila del tipo de expediente. Viáticos nunca usa una salida ajena.


Skill **transversal de salida**. No decide observaciones ni interpreta normas: eso lo hace la skill de dominio. Esta skill solo define **cómo se presenta el informe** y **qué validaciones externas deben quedar registradas**.

## Alcance

Se invoca desde:

- `control-previo-encargos`
- `control-previo-caja-chica`
- Otros expedientes de pago: convenios, servicios básicos, tasas, sentencias judiciales

**EXCLUSIÓN EXPRESA — ÓRDENES DE SERVICIO Y DE COMPRA.** Desde el 18/09/2026 las OS y OC NO usan este formato de dos hojas. Su formato acordado con el especialista es el **Protocolo v1.1 de siete hojas** de la skill `informe-control-previo-os-oc`, alimentado por la norma y el criterio de `control-previo-ordenes`. Si el expediente es de OS u OC, esta skill no se usa.

**EXCLUSIÓN EXPRESA — VIÁTICOS.** Los expedientes de rendición de viáticos NO usan este formato. Tienen su propio formato oficial v7.0, de tres hojas — INFORME, CHECKLIST y COMPROBANTES —, en la skill `control-previo-viaticos-v3`; ese formato dejó sin efecto el v5.5 de cuatro hojas, el v6.0 de seis hojas y el espejo HTML. Si el expediente es de viáticos, esta skill no se usa: se deriva a esa skill y se respeta su formato sin modificarlo.

## Orden de trabajo — no invertirlo

1. La skill de dominio lee su directiva, analiza el expediente y **decide** veredicto, observaciones y notas.
2. Recién entonces se arma el JSON de esta skill.
3. Se ejecuta el generador.

Nunca al revés. El formato no puede anteceder al análisis.

## Principios del formato

- **Lo primero que se ve es el veredicto.** Si hay que bajar para saber si está observado, el informe falló.
- **Lenguaje de control previo, no de sistemas.** Jamás mencionar OCR, extracción, scripts ni procesos técnicos. La trazabilidad se expresa como documento, número y página.
- **Cero filas de "no corresponde" para documentos que no existen en la carpeta.** Si no está y no se exige, no ocupa una fila.
- **Ninguna celda vacía.** O dato, o la palabra que corresponda.
- **Todo texto de observación en tercera persona y listo para pegar** al informe oficial, sin editar.
- **Tres colores:** rojo observado, ámbar por verificar, verde conforme. Gris para no corresponde.

## Contrato JSON

```json
{
  "expediente": "DIFODS2026-INT-0567802",
  "tipo_tramite": "Orden de Servicio - Contratación Menor",
  "norma_aplicada": "Pautas MM 0034-2020-MINEDU/SG-OGA; Ley 32069; Ley 27444",
  "unidad_remitente": "OGA - Oficina de Logística",
  "acreedor": "APELLIDOS NOMBRES o RAZON SOCIAL",
  "doc_identidad": "RUC 10XXXXXXXXX",
  "objeto_gasto": "Servicio de asistencia técnica",
  "periodo": "01/03/2026 al 31/03/2026 - armada 1 de 3",
  "importe_bruto": 2500.00,
  "deducciones": 56.45,
  "importe_neto": 2443.55,
  "revisor": "APELLIDOS NOMBRES DEL REVISOR",
  "fecha_revision": "18/09/2026",
  "veredicto": "SÍ HAY OBSERVACIONES",

  "observaciones": [
    {"texto": "Redacción en tercera persona lista para pegar.",
     "documento": "Cuadro de penalidad N° 2",
     "base_normativa": "Pautas, numeral 11",
     "gravedad": "A subsanable",
     "subsanacion": "Remitir el cuadro suscrito por el responsable."}
  ],

  "notas": [
    {"hecho": "Obra copia sin firma del informe técnico.",
     "motivo": "Prevalece el ejemplar suscrito. No se observa; descartar del legajo."}
  ],

  "validaciones": [
    {"validacion": "Ficha RUC del acreedor", "resultado": "ACTIVO / HABIDO",
     "estado": "VERIFICADO", "fecha_hora": "18/09/2026 09:14", "fuente": "SUNAT - Consulta RUC"}
  ],

  "verificaciones": [
    {"concepto": "Suma del comprobante", "debe_ser": "2,500.00",
     "expediente": "2,500.00", "resultado": "CONFORME"}
  ],

  "documentos": [
    {"documento": "Proveído de Devengado", "numero_fecha": "N° 12847 del 15/03/2026",
     "emisor": "Oficina de Logística", "firma": "Digital FAU, 15/03/2026 10:22",
     "exigible": "Sí - Anexo 1 fila 1", "estado": "CONFORME",
     "archivo": "PROVEIDO-12847.pdf", "pagina": 1,
     "aporte": "Autoriza el devengado por S/ 2,443.55."}
  ]
}
```

Campos obligatorios: todos los de cabecera, `veredicto`, `documentos`, `validaciones`, `verificaciones`. `observaciones` y `notas` pueden ir vacíos.

## HOJA 1 — DICTAMEN

**Línea 1.** El veredicto solo, celda combinada, fondo verde o rojo, letra grande. Una de dos frases: `NO HAY OBSERVACIONES` o `SÍ HAY OBSERVACIONES — n`.

**Bloque 1. Identificación.** Los campos de cabecera, en el orden del JSON.

**Bloque 2. Observaciones.** Columnas: N°, Observación, Documento que la origina, Base normativa, Gravedad, Cómo se subsana. Si no hay, una sola fila verde que diga `Sin observaciones`.

**Bloque 3. Notas y constancias.** Columnas: N°, Hecho advertido, Por qué no se observa. Es el respaldo del revisor: deja escrito lo que vio y decidió no observar.

**Bloque 4. Validaciones externas.** Columnas: Validación, Resultado, Estado, Fecha y hora de consulta, Fuente.

**Bloque 5. Verificación de montos y plazos.** Columnas: Concepto, Lo que debe ser, Lo que dice el expediente, Resultado.

## HOJA 2 — EXPEDIENTE

Una fila por documento **que realmente obra en la carpeta**. Columnas: N°, Documento, Número y fecha, Emisor y cargo, Firma y fecha de suscripción, Exigible con su numeral, Estado, Ubicación con hipervínculo a la página exacta, Qué aporta al pago.

La columna de **fecha de suscripción** es obligatoria y nunca se deja vacía: es la que revela conformidades apoyadas en informes firmados después.

Estados admitidos: `CONFORME`, `OBSERVADO`, `DUPLICADO`, `AJENO AL EXPEDIENTE`.

## Validaciones externas — catálogo y regla de honestidad

Se consulta lo que corresponda al tipo de expediente:

| Validación | Fuente |
|---|---|
| Ficha RUC: estado y condición | SUNAT, Consulta RUC |
| Validez del comprobante de pago | SUNAT, Consulta Validez CPE |
| Constancia de suspensión de 4ta categoría | SUNAT, Form. 1609 |
| Constancia de depósito de detracción | SUNAT, SPOT |
| Vigencia y sanciones del proveedor | OSCE, RNP |
| Impedimentos para contratar | OSCE |
| Grado académico exigido por el TDR | SUNEDU, Registro de Grados y Títulos |
| Colegiatura y habilidad | Colegio profesional que corresponda |
| CCI coincide con la entidad bancaria declarada | Documentos del expediente |

**Regla dura, no negociable:** el campo `estado` solo admite `VERIFICADO`, `NO VERIFICABLE` o `NO CORRESPONDE`.

- `VERIFICADO` únicamente si la consulta se ejecutó y devolvió resultado. Se registra la hora.
- `NO VERIFICABLE` si el portal pidió captcha, no respondió o exigió credenciales. Se registra igual la hora del intento.
- `NO CORRESPONDE` si la validación no aplica a ese tipo de expediente.

Jamás se declara verificado lo que no se consultó. Un hueco visible vale más que una conformidad falsa.

## Generación

Escribir el script en el directorio de trabajo y ejecutarlo:

```bash
python3 generar_informe_cp.py <carpeta_destino> <datos.json> --host-base "<ruta Windows del expediente>"
```

Salida: `<carpeta>/INFORME_CONTROL_PREVIO_<expediente>.xlsx`, guardado **dentro de la carpeta del expediente**. Si el archivo está abierto en Excel, avisar al usuario y reintentar; nunca renombrar para esquivar el bloqueo.

```python
#!/usr/bin/env python3
# generar_informe_cp.py — formato único de informe de control previo MINEDU
import json, os, re, argparse, urllib.parse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

VERDE=PatternFill("solid",fgColor="C6EFCE"); ROJO=PatternFill("solid",fgColor="FFC7CE")
AMAR=PatternFill("solid",fgColor="FFEB9C"); GRIS=PatternFill("solid",fgColor="E7E6E6")
HEAD=PatternFill("solid",fgColor="305496"); SUB=PatternFill("solid",fgColor="8497B0")
HEADF=Font(bold=True,color="FFFFFF")
BORDE=Border(*[Side(style="thin",color="999999")]*4)
LINK=Font(color="0563C1",underline="single")

OK={"CONFORME","VERIFICADO","PRESENTE","OK","SI","SÍ"}
MAL={"OBSERVADO","AUSENTE","NO CONFORME","DIFERENCIA","SIN SUSTENTO","INCONSISTENTE"}
MEDIO={"POR VERIFICAR","NO VERIFICABLE","REVISAR","INCOMPLETO","PARCIAL"}
NEUTRO={"NO CORRESPONDE","N.A.","DUPLICADO","AJENO AL EXPEDIENTE"}

def color(v):
    e=(v or "").strip().upper()
    if e in OK: return VERDE
    if e in MAL: return ROJO
    if e in MEDIO: return AMAR
    if e in NEUTRO: return GRIS
    return None

def link(base,arch,pag):
    if not base or not arch: return None
    b=str(base).replace(chr(92),"/")
    if not b.endswith("/"): b+="/"
    pre="file://" if b.startswith("/") else "file:///"
    u=pre+urllib.parse.quote(b,safe="/:")+urllib.parse.quote(str(arch),safe="/:")
    m=re.search(r"\\d+",str(pag or ""))
    return u+("#page="+m.group() if m else "")

def autosize(ws,maxw=70):
    for col in ws.columns:
        L=get_column_letter(col[0].column)
        n=max((len(str(c.value)) for c in col if c.value is not None),default=10)
        ws.column_dimensions[L].width=min(max(n+2,12),maxw)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("carpeta"); ap.add_argument("datos")
    ap.add_argument("--host-base",default=None)
    a=ap.parse_args()
    d=json.load(open(a.datos,encoding="utf-8"))
    wb=Workbook(); ws=wb.active; ws.title="DICTAMEN"
    estado={"r":1}

    obs=d.get("observaciones",[])
    txt=(d.get("veredicto") or "").upper()
    if obs and "NO HAY" not in txt: txt="SÍ HAY OBSERVACIONES — %d"%len(obs)
    r=estado["r"]
    ws.merge_cells(start_row=r,start_column=1,end_row=r+1,end_column=6)
    c=ws.cell(row=r,column=1,value=txt)
    if "NO HAY" in txt:
        c.fill=VERDE; c.font=Font(bold=True,size=22,color="006100")
    else:
        c.fill=ROJO; c.font=Font(bold=True,size=22,color="9C0006")
    c.alignment=Alignment(horizontal="center",vertical="center")
    ws.row_dimensions[r].height=30; ws.row_dimensions[r+1].height=30
    estado["r"]=r+3

    def titulo(t):
        r=estado["r"]
        ws.merge_cells(start_row=r,start_column=1,end_row=r,end_column=6)
        s=ws.cell(row=r,column=1,value=t); s.fill=SUB; s.font=HEADF
        s.alignment=Alignment(horizontal="left",vertical="center")
        estado["r"]=r+1

    def tabla(cols,filas,estado_col=None):
        r=estado["r"]
        for j,h in enumerate(cols,1):
            x=ws.cell(row=r,column=j,value=h); x.fill=HEAD; x.font=HEADF
            x.alignment=Alignment(horizontal="center",wrap_text=True); x.border=BORDE
        r+=1
        for fila in filas:
            for j,v in enumerate(fila,1):
                x=ws.cell(row=r,column=j,value=v); x.border=BORDE
                x.alignment=Alignment(wrap_text=True,vertical="top")
                if estado_col and j==estado_col:
                    f=color(v)
                    if f: x.fill=f
            r+=1
        estado["r"]=r+1

    titulo("1. IDENTIFICACIÓN DEL EXPEDIENTE")
    campos=[("expediente","Expediente"),("tipo_tramite","Tipo de trámite"),
            ("norma_aplicada","Norma aplicada"),("unidad_remitente","Unidad que remite"),
            ("acreedor","Acreedor"),("doc_identidad","RUC o DNI"),
            ("objeto_gasto","Objeto del gasto"),("periodo","Periodo o plazo"),
            ("importe_bruto","Importe bruto S/"),("deducciones","Deducciones S/"),
            ("importe_neto","Importe neto a pagar S/"),("revisor","Revisor"),
            ("fecha_revision","Fecha de revisión")]
    r=estado["r"]
    for k,lab in campos:
        x=ws.cell(row=r,column=1,value=lab); x.fill=HEAD; x.font=HEADF; x.border=BORDE
        y=ws.cell(row=r,column=2,value=d.get(k,"—")); y.border=BORDE
        y.alignment=Alignment(wrap_text=True); r+=1
    estado["r"]=r+1

    titulo("2. OBSERVACIONES")
    if obs:
        tabla(["N°","Observación","Documento que la origina","Base normativa","Gravedad","Cómo se subsana"],
              [[i,o.get("texto",""),o.get("documento","—"),o.get("base_normativa","—"),
                o.get("gravedad","—"),o.get("subsanacion","—")] for i,o in enumerate(obs,1)])
    else:
        r=estado["r"]
        x=ws.cell(row=r,column=1,value="Sin observaciones")
        x.fill=VERDE; x.font=Font(bold=True); x.border=BORDE
        estado["r"]=r+2

    titulo("3. NOTAS Y CONSTANCIAS")
    notas=d.get("notas",[])
    tabla(["N°","Hecho advertido","Por qué no se observa"],
          [[i,n.get("hecho",""),n.get("motivo","")] for i,n in enumerate(notas,1)]
          or [["—","Sin notas","—"]])

    titulo("4. VALIDACIONES EXTERNAS")
    tabla(["Validación","Resultado","Estado","Fecha y hora de consulta","Fuente"],
          [[v.get("validacion",""),v.get("resultado","—"),v.get("estado","NO VERIFICABLE"),
            v.get("fecha_hora","—"),v.get("fuente","—")] for v in d.get("validaciones",[])],
          estado_col=3)

    titulo("5. VERIFICACIÓN DE MONTOS Y PLAZOS")
    tabla(["Concepto","Lo que debe ser","Lo que dice el expediente","Resultado"],
          [[v.get("concepto",""),v.get("debe_ser","—"),v.get("expediente","—"),v.get("resultado","—")]
           for v in d.get("verificaciones",[])], estado_col=4)

    autosize(ws); ws.column_dimensions["B"].width=62

    w2=wb.create_sheet("EXPEDIENTE")
    cols=["N°","Documento","Número y fecha","Emisor y cargo","Firma y fecha de suscripción",
          "Exigible","Estado","Ubicación","Qué aporta al pago"]
    for j,h in enumerate(cols,1):
        x=w2.cell(row=1,column=j,value=h); x.fill=HEAD; x.font=HEADF
        x.alignment=Alignment(horizontal="center",wrap_text=True); x.border=BORDE
    for i,doc in enumerate(d.get("documentos",[]),1):
        f=i+1
        vals=[i,doc.get("documento",""),doc.get("numero_fecha","—"),doc.get("emisor","—"),
              doc.get("firma","—"),doc.get("exigible","—"),doc.get("estado","—"),
              doc.get("archivo","—"),doc.get("aporte","—")]
        for j,v in enumerate(vals,1):
            x=w2.cell(row=f,column=j,value=v); x.border=BORDE
            x.alignment=Alignment(wrap_text=True,vertical="top")
            if j==7:
                c2=color(v)
                if c2: x.fill=c2
        u=link(a.host_base,doc.get("archivo",""),doc.get("pagina",""))
        if u:
            cel=w2.cell(row=f,column=8); cel.hyperlink=u; cel.font=LINK
    autosize(w2); w2.column_dimensions["I"].width=55

    out=os.path.join(a.carpeta,"INFORME_CONTROL_PREVIO_%s.xlsx"%d.get("expediente","EXP"))
    wb.save(out); print(out)

if __name__=="__main__":
    main()
```

## Verificación antes de entregar

1. Abrir el archivo generado y confirmar que el veredicto se ve en la primera pantalla.
2. Comprobar que cada hipervínculo de la hoja EXPEDIENTE abre el documento en la página indicada.
3. Confirmar que no quedó ninguna celda vacía ni ningún `estado` de validación en blanco.
4. Confirmar que ninguna fila de la hoja EXPEDIENTE corresponde a un documento que no está en la carpeta.
5. Si el expediente era de viáticos, esta skill no debía usarse: rehacer con `control-previo-viaticos-v3`.
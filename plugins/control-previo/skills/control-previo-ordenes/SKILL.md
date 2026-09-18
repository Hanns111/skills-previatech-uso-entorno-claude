---
name: control-previo-ordenes
description: "Skill para control previo administrativo y financiero de expedientes de pago de Órdenes de Servicio (OS) y Órdenes de Compra (OC) del MINEDU. Aplica las \"Pautas para la Remisión de Expedientes para el Trámite de Devengado y Pago\", la Ley 32069 (Ley General de Contrataciones Públicas) y la Ley 27444 (Procedimiento Administrativo General). Usar cuando el usuario mencione orden de servicio, orden de compra, OS, OC, carta contrato, expediente de pago, control previo de OS/OC, recibo por honorarios, RHE, factura, devengado, proveído, conformidad, entregable, armada, suspensión de cuarta categoría, detracción, contratación menor a 8 UIT, locación de servicios, o adjunte PDFs con TDR, propuesta económica, conformidad, RHE, proveído de devengado o expedientes UPP/INT del MINEDU. Produce el veredicto estructurado (Sí/No hay observaciones), las observaciones con su base normativa y la matriz de coherencia. El formato del informe Excel NO lo define esta skill: lo define informe-control-previo-os-oc, Protocolo v1.1 de siete hojas. Esta skill aporta la norma y el criterio; aquella aporta la presentación."
---

# Control Previo — Órdenes de Servicio y Órdenes de Compra MINEDU

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


> **Versión 10.0 — generada el 10-09-2026 (hora de Lima)**
>
> Ver carpeta `versiones/` para el detalle de cambios de cada versión.

## Marco normativo aplicable

- **Pautas operativas**: "PAUTAS PARA LA REMISIÓN DE EXPEDIENTES DE PAGO – REVISIÓN CONTROL PREVIO" (MINEDU, vigentes).
- **Ley 32069** — Ley General de Contrataciones Públicas y su Reglamento.
- **Ley 27444** — Ley del Procedimiento Administrativo General (jerárquicamente superior a directivas internas).
- **TUO Ley del Impuesto a la Renta**, Art. 33 inciso a) — base de no retención de cuarta categoría.
- **Régimen de detracciones SUNAT** (cuando el servicio esté afecto).
- **Pautas para los Contratos Menores en el MINEDU – UE 024, 026 y 116**.

> **PRINCIPIO RECTOR (Ley 27444)**: Si el expediente está completo conforme a las pautas, no se puede detener el pago por errores formales o información accesoria que no corresponda al expediente. La Ley 27444 prevalece sobre directivas internas. Prefiere NO observar antes que observar incorrectamente.
>
> **v10.0 — Documentos ajenos inocuos**: un documento que no tiene nada que ver con el trámite (circulares, oficios múltiples, directivas, resoluciones generales, etc.) NO anula ni interrumpe el pago de un expediente completo. Solo se observa un documento ajeno cuando tergiversa la información del expediente o corresponde a otra persona/contrato (ver "Clasificación de documentos ajenos").

---

## Auto-montaje de carpetas (REGLA OBLIGATORIA)

Si el usuario menciona o pega una ruta de carpeta de expediente (Windows o Unix) y esa carpeta NO está montada, **montarla inmediatamente** pasando la ruta tal cual (`mcp__cowork__request_cowork_directory`, o `mcp__remote-devices__device_request_folder_access` cuando la sesión trabaja contra el equipo del usuario).

- **PROHIBIDO** preguntar al usuario "¿quieres que la monte?" o "no la veo, móntala desde Cowork".
- **PROHIBIDO** sugerir un expediente alternativo que sí esté montado.
- Si la ruta tiene número similar a otra ya montada, igual montarla — son expedientes distintos.
- Aplicar el mismo auto-montaje cuando el usuario adjunte una imagen del Explorador de Windows mostrando la ruta.

## Flujo de trabajo general (REGLAS ANTI-ALUCINACIÓN)

Cuando el usuario proporcione un expediente de OS/OC, ejecutar este flujo en orden estricto:

### Paso 0 — Inventario y extracción de TODOS los PDFs
```bash
# Para cada PDF del expediente:
pdfinfo "$f"                       # contar páginas
pdftotext -layout "$f" "$f.txt"    # extracción de texto base
pdfimages -list "$f"               # ¿qué páginas tienen imágenes?
```

### Paso 1 — OCR OBLIGATORIO Y EXHAUSTIVO sobre TODAS las páginas image-only del EXPEDIENTE COMPLETO

**REGLA DE ORO**: Antes de emitir CUALQUIER juicio, se debe construir un **corpus textual completo del expediente** que incluya el texto OCR de TODAS las páginas image-only de TODOS los PDFs. Sin excepciones, sin muestreo, sin "cercanía al RHE", sin filtrar por nombre de archivo.

Pipeline obligatorio para cada PDF del expediente:

```bash
mkdir -p /tmp/cp_ocr
for f in *.pdf; do
  base=$(basename "$f" .pdf)
  pdftotext -layout "$f" "/tmp/cp_ocr/${base}.txt"
  npages=$(pdfinfo "$f" | awk '/Pages/ {print $2}')
  for n in $(seq 1 $npages); do
    # ¿la página n tiene texto extraíble?
    chars=$(pdftotext -layout -f $n -l $n "$f" - | tr -d '[:space:]' | wc -c)
    if [ "$chars" -lt 20 ]; then
      pdftoppm -f $n -l $n -r 250 "$f" "/tmp/cp_ocr/${base}_p${n}" -png
      tesseract "/tmp/cp_ocr/${base}_p${n}-${n}.png" - -l spa 2>/dev/null \
        >> "/tmp/cp_ocr/${base}.ocr.txt"
    fi
  done
done
# Corpus consolidado del expediente:
cat /tmp/cp_ocr/*.txt /tmp/cp_ocr/*.ocr.txt > /tmp/cp_ocr/_CORPUS.txt
```

**Comprobación previa del OCR (v9.9)**: si `tesseract --list-langs` no incluye `spa`, instalarlo antes de OCRear (por ejemplo descargando `spa.traineddata` de `tessdata_fast` a `/usr/share/tesseract-ocr/*/tessdata/`). Un OCR que devuelve páginas vacías NO es prueba de que la página esté en blanco: verificar siempre que el motor cargó el idioma antes de concluir que un documento no existe.

**Disparadores OBLIGATORIOS de OCR** (cualquiera de estos):
- Una página tiene < 20 caracteres extraíbles por `pdftotext`.
- `pdfimages -list` reporta imágenes en una página sin texto.
- Un PDF tiene tamaño > 1 MB y texto extraído < 50 líneas por MB.
- El nombre del PDF sugiere comprobante (RHE, factura, recibo, boleto, constancia, suspensión).
- El expediente referencia un documento (RHE, factura, constancia SUNAT, conformidad) que no aparece en el corpus actual.

**Búsquedas OBLIGATORIAS sobre el corpus consolidado** (NO sobre un solo PDF, NO solo cerca del RHE):

```bash
# Constancia de Suspensión 4ta Categoría — buscar por TODOS los términos:
grep -in -E "1609|Suspensi[oó]n|AUTORIZADO|Form\.?\s*1609|4ta.*[Cc]ategor" /tmp/cp_ocr/_CORPUS.txt
# Por RUC del proveedor (reemplazar):
grep -n "RUC_DEL_PROVEEDOR" /tmp/cp_ocr/_CORPUS.txt
# RHE / Factura:
grep -in -E "RECIBO POR HONORARIOS|FACTURA ELECTR|E001-|EE01-" /tmp/cp_ocr/_CORPUS.txt
```

**REGLA ANTI-FALSO-NEGATIVO (no negociable)**: PROHIBIDO declarar un documento "ausente" (Constancia de Suspensión, RHE, factura, conformidad, etc.) sin haber:
1. Construido el corpus OCR completo del expediente conforme al pipeline anterior.
2. Ejecutado las búsquedas obligatorias por **al menos tres términos distintos** (p.ej. "1609", "Suspensión", RUC del proveedor) sobre el corpus consolidado.
3. Confirmado que ninguna página del expediente — esté donde esté, en cualquier PDF, en cualquier orden — contiene el documento.

Las constancias y comprobantes pueden estar en CUALQUIER PDF del expediente, en CUALQUIER página, no necesariamente junto al RHE ni en páginas contiguas. Las imágenes escaneadas son la causa #1 de falsos positivos.

### Paso 2 — Reglas operativas

1. **Leer TODOS los archivos del expediente, página por página**, antes de emitir cualquier juicio. Nunca muestrear.
2. **Nunca completar** información de un documento con datos de otro.
3. **Nunca calcular** por cuenta propia salvo verificación matemática indicada (saldo por devengar, plazos, sumas de armadas).
4. Si un dato no es visible → escribir **NULL** o "no visible en expediente"; nunca inferir.
5. **Evaluar el expediente como un TODO**: si un documento existe en cualquier parte del expediente (incluido OCR de imágenes), es válido. No observar ausencia por no verlo en una página o por estar en formato imagen.
6. Antes de emitir cualquier observación, verificar contra la lista "Reglas de NO observar" (ver más abajo).
7. Antes de declarar "ausente" un comprobante de pago o una constancia SUNAT, **certificar** que se aplicó OCR sobre todas las páginas image-only del expediente y que se buscó por RUC + "1609" + "Suspensión" sobre el corpus consolidado completo.
8. Las constancias, RHE y comprobantes pueden estar en CUALQUIER PDF y CUALQUIER página del expediente. Nunca asumir que un documento debe estar "junto" o "cerca" de otro.
9. **Antes de observar una supuesta discrepancia de montos, entender qué representa CADA campo del formato** (nivel contrato vs nivel armada). Ver "Lectura de campos por nivel" más abajo. Un campo que responde a otra pregunta no es una contradicción.

---

## Lectura de campos por nivel: CONTRATO vs ARMADA (REGLA OBLIGATORIA — v9.9)

En los expedientes MINEDU conviven formatos que razonan a **nivel de contrato** y formatos que razonan a **nivel de armada**. Confundirlos produce falsas observaciones.

| Documento | Nivel | Campos típicos |
|---|---|---|
| Orden de Servicio / Compra (SIGA) | Contrato, con detalle de cuotas | Monto total del contrato; cuotas 001, 002… con su plazo e importe |
| Informe/Cuadro de Aplicación de Penalidad (SGC) | **Contrato** para el residual, **armada** para la base de cálculo | "1. Monto del contrato", "3. Saldo a pagar", "7. Monto a pagar" son CONTRACTUALES; la penalidad diaria se calcula con el monto de la ARMADA |
| Proveído de Devengado (SGC) | **Armada** | SUB TOTAL del comprobante y de cada penalidad; TOTAL S/. = lo que se paga en ESTA armada |
| Conformidad | Armada | Monto de armada a pagar, N° de armada, fechas de la armada |

**Consecuencia práctica**: en el cuadro de penalidad, `7. Monto a pagar` = `monto del contrato − esa penalidad`. NO es el pago de la armada y **NO tiene por qué coincidir con el TOTAL del Proveído**. Cuando hay dos o más penalidades en la misma armada, cada cuadro muestra el residual contractual considerando **solo la suya**; la acumulación aparece únicamente en el Proveído. **Eso es el comportamiento normal del formato SGC y NO se observa.**

Lo que sí debe cruzarse es el **importe de la penalidad** (y su base de cálculo), no el residual contractual.

---

## Estructura de análisis — 8 verificaciones obligatorias

Aplicar en este orden, una por una:

### 1. CLASIFICACIÓN DEL EXPEDIENTE
Identificar:
- Tipo de contratación: Contratación Menor (CM ≤ 8 UIT), Adjudicación Simplificada, Concurso Público, Consultor Individual, Servicios Básicos, Acuerdo Marco, etc.
- Tipo de pago: armada única / 1ra / 2da / posterior / única.
- Naturaleza del proveedor: persona natural / persona jurídica.
- Tipo de comprobante: Factura Electrónica / RHE / Boleto aéreo / otro.
- Nº de Orden de Servicio o Compra y Carta Contrato (si aplica).

### 2. VERIFICACIÓN DOCUMENTAL
Ver lista completa en `references/checklist-documentos.md`. Marcar cada documento como ✔ presente / ⚠ incompleto / ❌ ausente.

### 3. COHERENCIA DOCUMENTAL
Cruzar entre TDR, OS/OC, Carta Contrato, Conformidad, RHE/Factura, cuadros de penalidad y Proveído de devengado:
- Nº de armada
- Monto de la armada y monto a pagar (respetando el nivel de cada campo)
- Nº de OS/OC
- Nº de contrato (si lo hay)
- Razón social y RUC del proveedor
- Descripción del servicio / bien
- N° del informe que la Conformidad declara como sustento

### 4. VERIFICACIÓN MATEMÁTICA
- Monto total contractual = suma de todas las armadas previstas.
- **Saldo por devengar (regla crítica)**: en Control Previo, el devengado AÚN NO se ha registrado en SIAF. Por lo tanto:
  `Saldo por devengar = Monto total – Armadas YA pagadas (sin restar la armada actual)`
  La armada que se está revisando puede estar incluida en el saldo por devengar. **NO observar** por este motivo.
- **Neto de la armada** = monto de la armada − suma de TODAS las deducciones de esa armada (penalidades, retención de garantía si corresponde). Debe coincidir con el TOTAL del Proveído. Esta suma la hace el control previo; no se le exige al cuadro de penalidad (ver "Lectura de campos por nivel").

### 5. VERIFICACIÓN DE PLAZOS (cómputo inclusivo)
- El día de inicio cuenta como **día 1**.
- Sumar días calendario inclusivos.
- Si el vencimiento cae en sábado, domingo o feriado, la entrega el primer día hábil siguiente es **válida** (y la fecha límite del cuadro de penalidad puede reflejar ese corrimiento: no observarlo).
- **NO observar presentación anticipada** del entregable o de la conformidad.

### 6. VERIFICACIÓN TRIBUTARIA (RHE / Factura)
Reglas obligatorias:
- **Recibo por Honorarios Electrónico (RHE)**:
  - Si **tiene retención del 8%** efectiva (importe distinto de cero en "Retención (8%) IR") → **OK**, no exigir suspensión.
  - Si **NO tiene retención** (Retención 8% IR = 0.00) → **buscar en TODO el expediente la Constancia de Suspensión de Retenciones de Cuarta Categoría** otorgada por SUNAT (vigente para el ejercicio fiscal en curso). Solo si NO se encuentra → **observar**.
  - **IMPORTANTE — Inciso A del Art. 33 LIR NO es exención**: la mención "Inciso A del Artículo 33 de la Ley del Impuesto a la Renta" aparece **siempre** en todos los RHE como referencia normativa estándar (define qué son rentas de cuarta categoría). **NO debe interpretarse como base de exoneración de retención**. La única base válida para no retener es la Constancia de Suspensión SUNAT vigente.
  - **PROHIBIDO**: observar incumplimiento solo porque el monto sea > S/ 1,500. El umbral lo define la suspensión SUNAT, no el monto del recibo.
  - **PROHIBIDO**: exigir firma manuscrita en RHE o factura electrónica (son documentos electrónicos válidos por sí mismos).
  - El proveído consigna el **monto bruto** (Total por honorarios), no el neto. Que el bruto del proveído sea mayor al neto del RHE por la retención **NO es inconsistencia**.
- **Factura electrónica**: verificar detracción si el servicio está afecto (consultar tipo de servicio en SUNAT).
- Validar: importe neto, condición "al crédito", fecha de emisión dentro del ejercicio fiscal vigente.
- En boletos aéreos: el boleto **es** el comprobante de pago; no exigir factura adicional.

### 7. VERIFICACIÓN DE FIRMAS Y SUSTENTOS
Reglas alineadas con el skill `control-previo-viaticos`:
- La firma puede ser **digital** o **manuscrita**.
- **Firma digital** (Ley 27269): se considera válida si el documento presenta el bloque "FAU 20131370998 hard/soft", el sello "FIRMADO DIGITALMENTE", o un QR/URL de validación institucional (p.ej. apps.firmaperu.gob.pe, esinad.minedu.gob.pe).
- **Firma manuscrita**: debe ir acompañada de **nombres, apellidos, DNI y cargo** del firmante. Si falta alguno, la firma es **incompleta**.
- **ÚNICA EXCEPCIÓN**: NO exigir firma en RHE ni en Factura Electrónica (son comprobantes electrónicos válidos por sí mismos). **Ningún otro documento del expediente está exento**, y en particular NO lo están los cuadros de penalidad ni los formatos generados por sistema (SIGA/SGC).
- **SOLO observar** la ausencia de firma cuando NO exista ninguna de las formas válidas anteriores, tras revisar TODAS las páginas del PDF (ver "Firmas dispersas en múltiples páginas") y tras OCR y **render visual** si la página es imagen.

Para cada documento del checklist, registrar el campo `firma` con uno de: `OK` (firma digital o manuscrita completa), `N.A.` (SOLO RHE/Factura y documentos no suscribibles como constancias SUNAT o cargos de mesa de partes), `INCOMPLETO` (manuscrita sin DNI/cargo), `AUSENTE`.

> **v9.9 — PROHIBIDO marcar `firma: "N.A."` en un cuadro o informe de aplicación de penalidad.** Ese documento SIEMPRE requiere suscripción; si no la tiene, va `firma: "AUSENTE"` y `estado: "OBSERVABLE"`.

---

## Reglas de NO observar (CRÍTICAS — evitan falsos positivos)

Antes de emitir cualquier observación, verificar que NO sea uno de estos casos. Si lo es, **no observar**:

1. **Presentación anticipada**: la conformidad, el entregable o el RHE pueden ser anteriores al fin nominal de la armada.
2. **Saldo por devengar incluyendo la armada actual**: es correcto en Control Previo.
3. **No es primer pago**: no exigir certificación presupuestal ni la propia OS/OC en cada armada (basta que estén en el primer expediente del contrato).
4. **Diferencia entre monto bruto del proveído y monto neto del RHE** por la retención del 8%: NO es inconsistencia, es lo esperado.
5. **RHE o factura electrónica sin firma manuscrita**: válidos.
6. **Campos "Nº de Contrato" o "Nº de Requerimiento" en blanco** cuando se trata de Carta Contrato bajo régimen de Contratación Menor (CM): no es observable.
7. **Errores menores de tipeo o información accesoria** que no afecten la integridad del expediente: por Ley 27444 no se puede detener el pago.
8. **Numeración de anexos distinta** a la directiva más reciente cuando se usan formatos institucionales aún vigentes.
9. **Comprobantes adicionales no listados en TDR**: no generan observación.
10. **Copia previa sin firma de un documento que también obra firmado** (p.ej. dos versiones del mismo Proveído, una sin suscribir y otra suscrita horas después): prevalece la versión suscrita; dejar nota, no observar.
11. **"Monto a pagar" / "Saldo a pagar" contractual del cuadro de penalidad que no coincide con el TOTAL del Proveído** (v9.9): esos campos del formato SGC son de nivel CONTRATO y consideran solo la penalidad de ese cuadro. NO es inconsistencia. Lo que se cruza contra el Proveído es el **importe de la penalidad**, no el residual.
12. **Fecha límite del cuadro de penalidad corrida al primer día hábil** cuando el vencimiento cayó sábado, domingo o feriado: es correcto y favorece al contratista.
13. **Penalidad por mora computada desde el vencimiento del plazo para subsanar observaciones**, cuando el TDR lo prevé: es penalidad por mora, NO una "penalidad adicional"; no observarla aunque el TDR diga "penalidades adicionales: no corresponde".
14. **Documentos ajenos inocuos** (v10.0): PDFs de otro expediente SINAD que no tienen relación alguna con el pago (circulares, oficios múltiples, directivas, resoluciones generales, comunicaciones institucionales) y que no alteran, contradicen ni sustituyen ningún dato o documento del expediente. Si el expediente está completo, NO se observan (Ley 27444): solo se deja una nota "descartar del legajo" y el veredicto sigue siendo "No hay observaciones".

---

## Formato de respuesta obligatorio

Empezar SIEMPRE con una de estas dos líneas exactas:

- **"Sí hay observaciones."**
- **"No hay observaciones."**

Si hay observaciones, enumerarlas de forma directa, una por línea numerada, sin justificar cumplimiento, sin análisis positivo, sin indicar archivo ni página (aunque internamente sí se debe identificar).

Tono: directo, técnico, sin adornos.

---

## Datos fijos de las Unidades Ejecutoras MINEDU

| UE | Nombre | RUC | Dirección fiscal |
|----|--------|-----|------------------|
| 024 | Ministerio de Educación Sede Central | 20131370998 | Calle El Comercio 193 San Borja |
| 026 | Programa Educación Básica Para Todos | 20380795907 | Calle El Comercio 193 San Borja |
| 116 | Colegio Mayor Secundario Presidente del Perú | 20546369383 | Calle El Comercio 193 San Borja |

---

## Informe Excel OBLIGATORIO por expediente

> **FORMATO VIGENTE — leer antes de generar nada.** El libro que se entrega es el del **Protocolo v1.1, siete hojas**, definido en la skill `informe-control-previo-os-oc`: DICTAMEN, PROVEIDO, EXPEDIENTE, FIRMAS, TDR VALIDACIONES, TRIBUTARIO y PROTOCOLO ACUERDOS. Esa skill manda en nombres de hoja, cuadros, paleta, columna de página en formato TEXTO y orden de construcción.
>
> Todo lo que sigue en esta sección conserva su valor como **contenido y contrato de datos**: el JSON, el orden canónico de documentos, las reglas de hyperlinks y el generador `scripts/generar_checklist.py` siguen siendo válidos y NO se eliminan. Se usan como respaldo cuando la skill de salida no esté disponible, y como fuente de los datos que alimentan las siete hojas cuando sí lo esté. Ante conflicto de forma, manda el Protocolo v1.1; ante conflicto de norma o criterio, manda esta skill.

Al finalizar el análisis de cada expediente, **siempre** generar un archivo Excel con el checklist completo y guardarlo **dentro de la misma carpeta del expediente** (no en Downloads, no en outputs). Nombre fijo:

```
INFORME_CONTROL_PREVIO_<NRO_EXPEDIENTE>.xlsx
```

Para generarlo usar el script incluido en la skill:

```bash
python3 scripts/generar_checklist.py "<carpeta_expediente_VM>" /tmp/datos_expediente.json \
  --host-base "C:\\Users\\<usuario>\\...\\<EXPEDIENTE>"
```

El parámetro `--host-base` es **OBLIGATORIO**: es la ruta HOST (Windows) de la carpeta del expediente, necesaria para construir hyperlinks `file:///...#page=N` que abran el PDF directamente en la página correcta. Si los archivos vinieron por montaje de carpeta, esa ruta es la que se usó al montar.

Si el Excel ya está abierto en Excel/WPS al momento de escribirlo, la escritura falla: avisar al usuario que lo cierre y reintentar. NO cambiar el nombre del archivo para esquivar el bloqueo.

donde `/tmp/datos_expediente.json` es un JSON construido por Claude con el inventario completo. La estructura del JSON está documentada en el encabezado de `scripts/generar_checklist.py`. Campos mínimos obligatorios:

- `expediente`, `ue`, `tipo_contratacion`, `orden`, `proveedor`, `ruc`
- `monto_total`, `n_armadas`, `armada_actual`, `monto_armada`
- `fecha_inicio`, `fecha_fin`, `fecha_entregable`, `fecha_conformidad`
- `veredicto` ("No hay observaciones" o "Sí hay observaciones")
- `observaciones` (lista vacía si no hay)
- `checklist`: cada ítem con `item`, `estado` (PRESENTE/AUSENTE/OBSERVABLE/N.A.), `archivo` (nombre EXACTO del PDF tal como aparece en la carpeta — el nombre será el hipervínculo), `pagina` (número entero — primera página donde aparece el documento), `exigible_en` ("1ra" para documentos base que solo se exigen en el primer pago, "cada armada" para los exigibles en todas las armadas), `firma` (OK/N.A./INCOMPLETO/AUSENTE), `comentario`

**Distinción CRÍTICA Conformidad ≠ Proveído de Devengado**:
- La **Conformidad** es el documento técnico emitido por el área usuaria que da por aceptado el entregable. Suele incluir, en formato MINEDU consolidado, una tabla "DETALLE DE LA PRESTACIÓN" con OS, monto, armada, fechas y referencia al Informe técnico. Esa tabla NO es el Proveído.
- El **Proveído de Devengado** es un documento DISTINTO, generado por el área administrativa para autorizar el devengado. **Es exigible SIEMPRE en TODAS las armadas** del expediente que llega a control previo. Si no está → **AUSENTE → OBSERVACIÓN**.

**Separación de exigibilidad por armada — IMPRESCINDIBLE**:

Sólo mostrar y exigir lo que corresponde según la armada en revisión.

### A) PRIMER PAGO (1ra armada) — REVISIÓN COMPLETA Y PROFUNDA
Se debe verificar todo lo relativo a los antecedentes de la contratación, además de los documentos de la armada actual:

1. **Términos de Referencia (TDR)** firmados por el área usuaria — leer a fondo: requisitos del proveedor (nivel de formación, capacitación, experiencia general en años, experiencia específica en años), unidad orgánica que otorga la conformidad, forma de pago, número de armadas, plazo, régimen de penalidades y garantías.
2. **Verificación del perfil del proveedor vs requisitos del TDR**: el CV/Anexo del proveedor (Certificado Único Laboral, certificados de trabajo, diplomas, títulos, constancias) debe **acreditar** el nivel de formación exigido (titulado/bachiller/diplomado/maestría según el caso) y los años de experiencia general y específica solicitados. Si falta alguna acreditación → OBSERVACIÓN.
3. **Estructura de Costos (Anexo 2)**.
4. **Declaración Jurada del Proveedor (Anexo 3)**.
5. **Cotización / propuesta económica**.
6. **Autorización VMGP** y formato A correspondiente.
7. **Cuadro CM (Contratación Menor)** o equivalente según tipo de contratación.
8. **Anexos de contratación**: RNP vigente, declaraciones juradas de no impedimentos, ficha RUC con estado ACTIVO/HABIDO, política institucional firmada, etc.
9. **Certificación de Crédito Presupuestal (CCP)** o, en su defecto, evidencia de SIAF asignado en la OS.
10. **Orden de Servicio / Orden de Compra** firmada digitalmente por las áreas correspondientes.
11. **Carta Contrato** (cuando aplique) o equivalente para Contratación Menor.
12. **CCI - Carta de Autorización de Pago** firmada por el proveedor (debe coincidir el CCI con el banco indicado).
13. **Constancia de Suspensión 4ta Categoría (Form. 1609 SUNAT)** vigente para el ejercicio fiscal — si el RHE no tiene retención.
14. **Constancia de recepción** del entregable (mesa de partes / SIGA-SISMEC).
15. **Entregable / producto** físico del 1er entregable.
16. **Informe técnico** del especialista responsable.
17. **Conformidad del área usuaria**: firmada por **la unidad orgánica indicada en el TDR** como responsable de otorgar la conformidad. Si la firma la otra área → OBSERVACIÓN.
18. **Memorando de remisión**.
19. **RHE / Factura Electrónica** de la armada — verificar retención 8% o Constancia 1609.
20. **Cuadro(s) de Aplicación de Penalidades** — cuando haya mora o deducción en el proveído; **firmado** y con importe coherente con el proveído (ver Verificación 8).
21. **Proveído de Devengado** (siempre exigible).

Cruzar coherencia: proveedor, RUC, OS, monto contractual, monto armada, deducciones, monto neto, descripción del servicio. Cualquier contradicción real entre documentos del antecedente → OBSERVACIÓN.

### B) SEGUNDO PAGO en adelante (2da, 3ra... armada) — REVISIÓN SIMPLIFICADA
Solo se exige y muestra:

1. **Constancia de aceptación / recepción** del entregable de la armada.
2. **Entregable** del periodo.
3. **Informe técnico** del área usuaria (de la armada).
4. **Conformidad** de la armada (firmada por la unidad indicada en el TDR).
5. **RHE / Factura** de la armada — siempre verificar si corresponde retención 8% o si está la Constancia 1609 vigente.
6. **Cuadro(s) de Aplicación de Penalidades** de la armada, firmados, si hubo mora o deducción.
7. **Proveído de Devengado** (siempre exigible).

NO se vuelven a exigir TDR, Anexo 3, CCI, CCP, RNP, etc., ya que se presentaron en la 1ra armada.

### Codificación en `exigible_en` del JSON
- `"1ra"` → ítem que solo se exige en la 1ra armada (NO se mostrará en armadas posteriores).
- `"cada armada"` → ítem que se exige en cada armada (incluyendo Proveído de Devengado y cuadros de penalidad de esa armada).
- `accesos_rapidos`: lista corta con los documentos clave (RHE, Constancia 1609, Proveído de Devengado, OS/OC, Conformidad, Informe técnico, Memorando, Penalidad si la hay) cada uno con `doc`, `archivo`, `pagina` — se renderiza en una hoja "Accesos rápidos" con hipervínculos directos
- `coherencia`: cruce entre documentos (proveedor, RUC, OS, armada, importe de penalidades, monto neto, descripción)
- `tributario`: datos del RHE/factura, retención y constancia 1609 (con archivo y página donde se ubicó)

**Reglas obligatorias del checklist**:
- Cada documento del checklist DEBE indicar el **nombre exacto del archivo PDF** y la **página** (o rango de páginas) donde aparece. Si fue ubicado vía OCR, indicarlo en `comentario` ("vía OCR").
- Cada documento DEBE indicar a qué armada aplica (1ra / 2da / 3ra / todas). Documentos base del contrato (TDR, OS, Carta Contrato, Estructura de Costos) → "todas". Documentos por armada (Conformidad, Informe técnico, RHE, cuadros de penalidad, Anexo administrativo, Proveído) → la armada en revisión.
- Si la armada actual NO es la 1ra, en el comentario de los documentos base anotar: "presentado en la 1ra armada (no exigible)".

Hoja "Observaciones": vacía si veredicto es No hay observaciones; en caso contrario, una fila por observación con descripción + fundamento normativo + gravedad (A subsanable / B devolutivo).

Si el usuario adicionalmente lo pide, también generar `INFORME_CP_OS_[NRO_EXPEDIENTE].xlsx` extendido usando la skill `xlsx` con las siguientes hojas:

1. **Datos del Expediente** — Nº expediente, OS/OC, Carta Contrato, proveedor, RUC, monto total, armada actual, periodo, UE.
2. **Inventario de Documentos** — Nº / nombre / fecha / observación.
3. **Checklist Documental** — documento requerido / estado (PRESENTE/AUSENTE/OBSERVABLE/N.A.) / observación.
4. **Coherencia Documental** — campo / valor en doc 1 / valor en doc 2 / resultado.
5. **Verificación Matemática** — monto contractual / armadas pagadas / armada actual / deducciones / neto / saldo / fórmula.
6. **Verificación de Plazos** — fecha inicio / fecha fin / días contractuales / fecha entregable / fecha conformidad / resultado.
7. **Verificación Tributaria** — RHE/Factura / fecha / importe / retención / suspensión / inciso art. 33 / detracción / resultado.
8. **Observaciones Consolidadas** — Nº / descripción / fundamento / gravedad (A subsanable / B devolutivo) / veredicto final.

Formato condicional: rojo para OBSERVABLE/AUSENTE/INCONSISTENTE, verde para CONFORME/PRESENTE/CONSISTENTE.

---

## Procesamiento de MÚLTIPLES expedientes en paralelo

Cuando el usuario indique de manera explícita varios expedientes (por nombre o por ruta), procesarlos **en paralelo** lanzando un subagente independiente por expediente. Cada subagente debe:

1. Montar la carpeta del expediente si aún no está montada.
2. Ejecutar el pipeline OCR completo (Paso 0 + Paso 1) sobre TODOS los PDFs de SU expediente y construir su propio `_CORPUS.txt` aislado.
3. Aplicar las 8 verificaciones de control previo sobre su corpus.
4. Construir el JSON de datos del expediente.
5. Ejecutar `scripts/generar_checklist.py` con la ruta VM y la ruta HOST de SU expediente como `--host-base`, generando el `INFORME_CONTROL_PREVIO_<EXPEDIENTE>.xlsx` **dentro de la propia carpeta del expediente**.
6. Devolver al orquestador: `{expediente, veredicto, n_observaciones, ruta_xlsx}`.

**Reglas críticas del paralelismo**:

- Cada subagente trabaja en su propio directorio temporal (`/tmp/cp_<expediente>/`) — nunca compartir corpus entre expedientes.
- El orquestador NO emite veredictos por su cuenta; solo consolida los resultados de los subagentes en una tabla resumen al final.
- Capacidad práctica: 5 a 10 expedientes en paralelo en una sola tanda. Si el usuario pasa más de 10, procesarlos en oleadas.
- El orquestador debe entregar al final una tabla resumen `{expediente | tipo (OS/OC) | armada | proveedor | monto | veredicto | observaciones | link al xlsx}` y un link a cada Excel individual.

Si el usuario no pide expresamente varios expedientes, NO se lanzan subagentes — la revisión es secuencial dentro de la conversación principal.

---

## Arquitectura multiagente recomendada (para expedientes complejos o lotes)

Cuando un expediente sea grande (>50 páginas totales) o cuando sea parte de un lote, el subagente del expediente puede a su vez delegar dimensiones específicas en agentes especializados. Cada agente solo "ve" su dimensión, lo que reduce alucinaciones y permite trazabilidad:

1. **Agente OCR/Visión** — corre `pdftoppm + tesseract` sobre todas las páginas image-only y produce el corpus consolidado. Solo entrega texto, no juicios.
2. **Agente Documental/Pautas** — aplica el checklist normativo sobre el corpus y marca PRESENTE/AUSENTE con archivo y página.
3. **Agente TDR/Perfil** (solo 1er pago) — extrae los requisitos del TDR (formación, experiencia general, experiencia específica, unidad que da la conformidad) y los confronta contra el CV/Anexos del proveedor (CUL, certificados, diplomas, títulos). Devuelve OK / INCONSISTENTE por requisito.
4. **Agente Tributario** — RHE/factura, retención 8%, Constancia 1609, detracción, coherencia bruto/neto, regla del Inciso A Art. 33 LIR.
5. **Agente Coherencia** — cruza proveedor, RUC, OS, monto, armada, importe de penalidades, monto neto y descripción del servicio entre TDR, OS, Conformidad, Informe técnico, RHE, cuadros de penalidad, Proveído y Memorando. Reporta cualquier contradicción real, respetando la regla de "Lectura de campos por nivel".
6. **Agente Plazos y Penalidades** — cómputo de plazos, presentación anticipada permitida, fecha de entrega vs fecha fin armada, cálculo, **firma** e importe de las penalidades, incumplimientos contractuales mencionados en Conformidad/Informe técnico/Memorando.
7. **Agente Firmas** — verifica que todo documento exigible tenga firma válida (digital con FAU 20131370998, manuscrita con DNI+cargo, o QR institucional). Verifica especialmente que la **Conformidad esté firmada por la unidad orgánica indicada en el TDR** y que **los cuadros de penalidad estén suscritos**.
8. **Agente Auditor (orquestador)** — consolida los hallazgos, aplica las "Reglas de NO observar", emite el veredicto final y dispara `generar_checklist.py`.

Esta arquitectura es opcional. Para expedientes pequeños (<30 páginas), la conversación principal hace todo.

---

## Verificación 8 — PENALIDADES E INCUMPLIMIENTOS CONTRACTUALES

Verificación obligatoria por cada armada:

1. Comparar `fecha_entregable` vs `fecha_fin_armada`:
   - Si entregable ≤ fin de armada → SIN PENALIDAD.
   - Si entregable > fin de armada → calcular días de mora y penalidad: `0.10 / (0.40 × plazo_del_entregable) × monto_armada × días_mora`, con tope del 10% del monto del contrato (Art. 120 del Reglamento de la Ley 32069 / Pautas MINEDU). En CM la fórmula puede ser distinta — verificar TDR.
   - **Mora en la subsanación**: si el TDR prevé que, vencido el plazo otorgado para subsanar observaciones, corresponde penalidad por mora, esa penalidad es legítima y NO es una "penalidad adicional" — se computa desde el vencimiento del plazo para subsanar hasta la fecha de reingreso. Verificar además que el plazo otorgado no exceda el tope del TDR (típicamente 30% del plazo del entregable).
2. Buscar en Conformidad, Informe técnico, Memorando y Proveído cualquier mención a:
   - "incumplimiento", "subsanación", "observado", "rechazado", "se aplica penalidad", "deducción", "descuento", "amonestación", "suspensión".
3. Si la Conformidad menciona penalidad pero el monto del Proveído NO la deduce → OBSERVACIÓN.
4. Si el entregable se presentó tarde y NO hay penalidad calculada en el expediente → OBSERVACIÓN.
5. Si hay incumplimientos contractuales documentados sin justificación o subsanación → OBSERVACIÓN.

### 8.A — FIRMA DE LOS CUADROS DE PENALIDAD (REGLA OBLIGATORIA — v9.9)

Todo "INFORME/CUADRO DE APLICACIÓN DE PENALIDAD" (por mora, por observación/subsanación, o por cualquier otra causal) que sustente una deducción en el Proveído **DEBE estar suscrito**. Que provenga del SGC/SIGA y traiga cabecera con fecha y hora del sistema **NO reemplaza la firma**.

Procedimiento obligatorio antes de dar por conforme un cuadro de penalidad:
1. Extraer el texto de TODAS sus páginas y buscar `FAU`, `FIRMADO DIGITALMENTE`, `En señal de conformidad`, `Doy V° B°`, o un QR/URL de validación institucional.
2. Si el texto no arroja firma, **renderizar la página a imagen (`pdftoppm -r 130` o superior) y verificarla VISUALMENTE**, porque los sellos y firmas gráficas no siempre son texto extraíble.
3. Solo después de ambos pasos se puede concluir.

Resultado:
- Sin firma digital, sin firma manuscrita con nombres + DNI + cargo, y sin sello del funcionario responsable → **`firma: "AUSENTE"`, `estado: "OBSERVABLE"` y OBSERVACIÓN OBLIGATORIA**.
- **PROHIBIDO** marcar `firma: "N.A."` en un cuadro de penalidad. Esa codificación está reservada a RHE/facturas electrónicas y a documentos no suscribibles (constancias SUNAT, cargos de mesa de partes).
- **PROHIBIDO** despachar la falta de firma como "error formal accesorio" bajo la Ley 27444: el cuadro es el sustento de una deducción sobre el pago del contratista.

### 8.B — LO QUE SÍ SE CRUZA CONTRA EL PROVEÍDO (y lo que NO) — v9.9

**SÍ se verifica:**
1. **Importe de cada penalidad**: el monto del cuadro debe aparecer idéntico como línea PENALIDAD en el Proveído.
2. **Base y fórmula de cálculo**: `0.10 × monto_armada / (0.40 × plazo_del_entregable)` por día de retraso, salvo que el TDR disponga otra. Verificar que la base sea el monto de la armada y el plazo el del entregable.
3. **Correspondencia uno a uno**: cada penalidad deducida en el Proveído tiene su cuadro, y cada cuadro corresponde a una deducción del Proveído. Ni de más ni de menos.
4. **Neto de la armada**: `monto_armada − Σ penalidades = TOTAL del Proveído`. Esta suma la hace el control previo.
5. **Tope acumulado**: la suma de penalidades por mora y otras penalidades no puede exceder el 10% del monto del contrato, considerando las armadas anteriores.
6. **Firma** (ver 8.A).

**NO se observa (error cometido en la primera revisión del caso DIFODS2026-INT-0567802):**
- Que el campo `7. Monto a pagar` del cuadro no coincida con el TOTAL del Proveído. Ese campo, junto con `1. Monto del contrato` y `3. Saldo a pagar`, es de **nivel contrato** y considera **solo la penalidad de ese cuadro**. Con dos penalidades en la misma armada, cada cuadro mostrará el mismo residual contractual y ninguno reflejará el neto de la armada: **así funciona el formato SGC**. Ver "Lectura de campos por nivel".

### 8.C — Marcado en el checklist

Para cada ítem de penalidad:
- `N.A.` → solo si el entregable llegó a tiempo y no hay observación documental alguna (no hay penalidad que aplicar).
- `PRESENTE` → la penalidad fue calculada correctamente, el cuadro está **firmado** y su importe **se traslada** correctamente al Proveído.
- `OBSERVABLE` (rojo) → el cuadro existe pero no está firmado, o su base de cálculo o su importe no corresponden a lo deducido en el Proveído.
- `AUSENTE` (rojo) → correspondía aplicar penalidad y no figura el cuadro.

Si la conformidad técnica indica "EL CONTRATISTA SI INCURRIO EN PENALIDADES" o similar y el expediente NO incluye el Cuadro de Aplicación de Penalidades detallado y firmado (Pautas MINEDU numeral 11) → **OBSERVACIÓN OBLIGATORIA**.

### Caso de referencia (v9.9)
DIFODS2026-INT-0567802 (OS 0005220-2026, ZACARIAS MERCADO CARLOS MANUEL, UE 026, armada 1 de 2). Dos lecciones opuestas del mismo expediente:
- **Falso negativo corregido**: los dos cuadros de penalidad llegaron **sin firma alguna** y en la primera revisión se marcaron erróneamente como `firma: "N.A."` por ser reportes de sistema. De ahí la regla 8.A.
- **Falso positivo corregido**: se observó que cada cuadro consignaba "Monto a pagar S/ 13,943.55" mientras el Proveído N° 12847 pagaba S/ 6,887.10, y se calificó como inconsistencia. **Era incorrecto**: 13,943.55 = 14,000.00 − 56.45 es el residual contractual del formato, no el pago de la armada; el importe de la penalidad (S/ 56.45 por cada cuadro) sí se trasladaba correctamente al Proveído, y la base de cálculo era la correcta (0.10 × 7,000 / (0.40 × 31)). De ahí las reglas 8.B y "Lectura de campos por nivel": entender el nivel de cada campo ANTES de observar una diferencia de montos.

---

## Informe de Conformidad (regla condicional)

El **Informe de Conformidad** NO es un documento exigido en todos los casos por las pautas MINEDU. Sin embargo:

- **Si el documento de Conformidad menciona expresamente** "Informe de Conformidad N° X" o "se sustenta en el Informe de Conformidad…" o "según Informe de Conformidad…" o "Conformidad generada en base a Informe N° X", entonces ese informe **DEBE estar adjunto al expediente y firmado** por el área usuaria. Si no aparece — o si el informe adjunto tiene un **número distinto** al citado — → **OBSERVACIÓN**.
- Si la Conformidad solo se sustenta en un "Informe técnico" del especialista (sin usar la frase "Informe de Conformidad"), basta con verificar el Informe técnico — no se exige adicionalmente un Informe de Conformidad.
- **No confundir**: "Informe técnico" del especialista ≠ "Informe de Conformidad" del área usuaria. Cuando ambos términos aparecen distinguirlos en el checklist como ítems separados.

Cuando aplique, agregar al checklist el ítem "Informe de Conformidad" con su archivo y página, exigible en `cada armada`, y verificar firma del responsable del área usuaria.

---

## Coherencia obligatoria en TODOS los pagos

Regla bloqueante (aplica tanto a 1er pago como a pagos siguientes):

> **Cualquier contradicción REAL entre dos o más documentos del expediente sobre datos sustantivos (proveedor, RUC, N° OS/OC, monto contractual, monto de armada, importe de las deducciones, monto neto a pagar, N° de armada, N° del informe que sustenta la conformidad, descripción del servicio, fechas) → OBSERVACIÓN.**

Errores de tipeo accesorios o variaciones formales (p.ej. "OS 1703-2026" vs "OS0001703-2026") NO son contradicciones reales y NO deben observarse. Tampoco lo son las diferencias entre campos que responden a niveles distintos (contrato vs armada).

---

## Documentos auxiliares (referencias)

- `references/checklist-documentos.md` — lista exhaustiva de documentos por tipo de contratación.
- `references/normativa-clave.md` — extractos clave de las pautas, Ley 32069 y Ley 27444.
- `references/verificaciones.md` — detalle operativo de las verificaciones y casos típicos.

Leer estos archivos cuando el caso lo requiera, no por defecto, para no consumir contexto innecesariamente.

## Orden canónico del checklist (v9.4 — REGLA OBLIGATORIA)

El Excel del informe DEBE mostrar los documentos en este orden, tanto en primera armada como en armadas posteriores (los que no apliquen para armada posterior simplemente se omiten):

1. **Proveído de Devengado**
2. **Informe de Conformidad** (con su Informe Técnico anidado, si existe)
3. **Constancia de Recepción**
4. **Certificación Presupuestal / CCI** (solo 1ra armada)
5. **Compromiso de Pago / Certificación de Compromiso** (solo 1ra armada)
6. **Suspensión 4ta categoría (Form. 1609)** — o, si corresponde, **RHE / Factura**
7. **Orden de Servicio / Orden de Compra**
8. **Carta Contrato**
9. **Entregable / Informe de actividades**
10. Resto (TDR, propuesta económica, anexos, penalidades, etc.)

Este orden está implementado en `scripts/generar_checklist.py` mediante la función `prioridad()` y la lista `ORDEN_CANONICO`. **No alterar el orden manualmente** desde el JSON: el script lo reordena por nombre del ítem usando expresiones regulares.

## Hyperlinks del Excel (REGLA OBLIGATORIA)

Cada ítem del checklist con `archivo` y `pagina` debe abrir el PDF EXACTAMENTE en la página indicada al hacer clic. Para garantizarlo:

- El JSON DEBE consignar el **número de la primera página** donde aparece el documento (entero, no rango).
- El campo `archivo` DEBE ser el nombre EXACTO del PDF tal como está en la carpeta del expediente (con extensión, mayúsculas/minúsculas correctas).
- El parámetro `--host-base` DEBE ser la ruta HOST (Windows) tal como el usuario la pegó al montar la carpeta.
- El script v9.4 URL-encodea espacios y caracteres especiales con `urllib.parse.quote`, de modo que Adobe/Foxit reconozcan `#page=N` correctamente.
- **Verificación obligatoria antes de entregar el Excel**: re-leer el PDF apuntado por cada hyperlink en la página indicada y confirmar que efectivamente contiene el documento listado. Si no coincide, corregir la página en el JSON y regenerar el Excel.

## Verificación tributaria ampliada (v9.4)

El bloque `tributario` del JSON ahora soporta y exige los siguientes campos cuando aplique:

- `condicion_pago`: `"al contado"` o `"al crédito"` (obligatorio para facturas).
- `aplica_retencion`: `"SI"` / `"NO"` con justificación en `comentario` (Form. 1609 vigente, monto < 1500, etc.).
- `aplica_detraccion`: `"SI"` / `"NO"` según el bien o servicio del Anexo 1, 2 o 3 del SPOT.
- `tasa_detraccion`, `monto_detraccion`, `constancia_detraccion`: cuando `aplica_detraccion = "SI"`.
- Para **facturas al crédito**, verificar también que la fecha de pago programada esté dentro del plazo del proveído de devengado.

## Firma del Responsable de Almacén en Órdenes de Compra (v9.5)

Distinguir DOS firmas distintas en expedientes de OC (regla del usuario, validada contra Pautas MINEDU pág. 12):

### A) Suscripción de la OC por Almacén (numeral 2 de las Pautas)
- **Obligatoria desde la 1ra armada**, en TODA Orden de Compra emitida por SIGA.
- Si falta esta firma en el primer pago de una OC → **OBSERVACIÓN**.
- Esta firma típicamente está en la propia hoja de la OC (cabecera o pie), pero **puede estar en una página distinta** del PDF de la OC (segunda, tercera o última hoja). Revisar TODAS las páginas del PDF de la OC antes de marcar como ausente.

### B) Conformidad de Almacén / NEA-PECOSA (numeral 9 de las Pautas)
- Es la conformidad del **internamiento físico** del bien en almacén.
- En contratos con **entregas parciales** puede no estar disponible en la 1ra armada (porque el bien aún no se ha internado totalmente). En esos casos NO se observa por su ausencia en el primer pago — se exige cuando se concreta el internamiento, normalmente en el **último pago**.
- En OC de **entrega única** o cuando ya hubo internamiento → es exigible desde la 1ra armada.
- Para 2da y demás armadas, la pauta indica que el expediente solo debe contener los numerales 8, 9, 10 y 11 (comprobante, conformidad almacén/área usuaria, guía de remisión, penalidades).

### Regla operativa
- En OC de 1ra armada: si falta la firma A → observar; si falta la conformidad B y hay entregas parciales pendientes → NO observar, dejar nota "se exigirá al internamiento total".
- En OC del último pago: ambas firmas (A y B) deben estar presentes.

## Firmas dispersas en múltiples páginas (REGLA OBLIGATORIA)

Tanto en OS como en OC, **las firmas no siempre están todas en la misma página**. He visto casos en los que dos firmas (proveedor + área usuaria) aparecen en la página 1 y la firma del Responsable de Almacén está sola en la página 3 del mismo PDF.

**Por lo tanto, antes de marcar una firma como AUSENTE, hay que:**
1. Extraer texto de TODAS las páginas del PDF de la OS/OC (no solo la primera).
2. Si el PDF tiene páginas en imagen, OCRearlas todas con `pdftoppm -r 250 + tesseract`.
3. **Renderizar y mirar la página** cuando el texto no arroje firma: los sellos y firmas gráficas suelen no ser texto extraíble.
4. Buscar el nombre y/o cargo del firmante (Responsable de Almacén, Jefe de Logística, etc.) en cualquier página.
5. Solo después de revisar TODAS las páginas se puede declarar AUSENTE.

En el JSON del checklist, registrar la página exacta donde se encontró cada firma en el campo `comentario` (ej. *"firma Almacén en pág. 3 del PDF de la OC"*) y apuntar el hyperlink a esa página específica.

## Garantía de Fiel Cumplimiento — Carta Fianza vs Retención (v9.6)

**REGLA CRÍTICA — NUNCA COEXISTEN:** la Garantía de Fiel Cumplimiento (10% del monto contractual) se constituye por **UNO** de estos dos métodos, **nunca por ambos a la vez**:

- **A) Carta Fianza** emitida por entidad financiera autorizada por la SBS, por el 10% del contrato.
- **B) Retención de Garantía** descontada de los pagos al contratista (válida típicamente para MYPES o cuando el contrato lo autoriza expresamente), hasta acumular el 10% del contrato.

Aplicar ambas simultáneamente = doble garantía = supera el tope legal del 10% → **OBSERVACIÓN INMEDIATA** y devolución del expediente.

### Procedimiento de control (obligatorio en CADA pago, no solo el primero)

1. **Leer la cláusula de garantías del contrato o del TDR** (típicamente Cláusula Sétima u Octava; en CM el TDR puede decir "Garantías: No aplica"). Identificar cuál de los dos métodos se pactó, o si no aplica ninguno.
2. **Escenario A — Contrato dice "Carta Fianza"**:
   - Verificar que la Carta Fianza esté en el expediente, vigente y por el monto correcto (10% del contractual).
   - Verificar que en el detalle del Proveído de Devengado **NO exista** ninguna línea de "RETENCIÓN GARANTÍA" o similar.
   - Si aparece tal línea → **OBSERVACIÓN**, devolver para corrección (eliminar la línea del proveído y recalcular el monto a pagar).
3. **Escenario B — Contrato dice "Retención de Garantía"**:
   - Verificar tope: 10% del monto total del contrato es el máximo retenible acumulado.
   - Verificar prorrata: la retención se descuenta proporcionalmente solo durante la **primera mitad** de los pagos.
   - Llevar registro acumulado de lo retenido en pagos previos para no exceder el tope.
   - Verificar que **NO exista** Carta Fianza en el expediente (sería redundante).
4. **Escenario C — TDR dice "No aplica"**: no exigir Carta Fianza ni retención; marcar el ítem como `N.A.` y verificar igualmente que el proveído no traiga línea de retención de garantía.

### Distinción importante: Penalidades ≠ Ejecución de Garantía

- **Penalidades por mora** se descuentan directamente del pago mensual por faltas operativas leves (uniformes, plazos menores, etc.) — son una herramienta independiente.
- **Garantía de fiel cumplimiento** es el último recurso para incumplimientos graves que justifiquen la terminación del contrato.
- Una cosa no excluye a la otra: en un mismo pago pueden aparecer penalidades descontadas Y mantenerse vigente la Carta Fianza. Lo que NO puede aparecer es "Retención de Garantía" si ya hay Carta Fianza.

### Caso de referencia
DEBEDSAR2024-INT-0763236 (PROXUS SECURITY S.A.C., contrato 006-2025-MINEDU/SG-OGA-OL-UE026, COAR Tacna): el Proveído N° 8271 incluyó indebidamente una Retención de Garantía de S/ 2,267.74 cuando ya existía Carta Fianza por S/ 272,012.92 (Cláusula Sétima). El expediente fue devuelto, se eliminó la línea del proveído y se recalculó el pago.

### Implementación en el checklist
Agregar al JSON dos ítems:
- `"item": "Carta Fianza de Fiel Cumplimiento"` con `exigible_en: "1ra"` y referencia a la cláusula del contrato o del TDR.
- `"item": "Verificación exclusividad Carta Fianza vs Retención de Garantía"` con `exigible_en: "cada armada"` — el agente debe leer el proveído y confirmar que no haya doble cobro.

## Snapshot maestro del proyecto (REGLA OBLIGATORIA — v9.7)

Cada vez que se modifique esta skill (o cualquier otra skill del proyecto MINEDU), Claude DEBE:

1. Bumpear versión en el `SKILL.md`.
2. Escribir el changelog puntual en `versiones/v<X.Y>_<YYYYMMDD>_<HHMM>.md`.
3. Generar el ZIP en `Downloads/`.
4. **CREAR UN NUEVO archivo de snapshot maestro** en
   `C:\Users\Hans\Proyectos\COWORK\MINEDU_2026\_DOCUMENTACION_PROYECTO\`
   con nombre `ESTADO_PROYECTO_v<X.Y>_<YYYYMMDD>_<HHMM>.md`.

   El snapshot debe contener TODO el contexto del proyecto en ese momento — no solo el cambio puntual — incluyendo: propósito, estructura de carpetas, lista de skills y versiones, historial completo de versiones, reglas normativas implementadas, contrato del JSON del script, enrutador de expedientes, expedientes procesados, entorno técnico, y la propia convención de mantenimiento.

   **Nunca sobrescribir snapshots anteriores.** La carpeta debe acumular el historial v1, v2, v3 …

   **Objetivo:** que cualquier LLM (Claude, GPT, Cursor, Gemini) pueda leer SOLO el snapshot más reciente y reconstruir el proyecto completo mediante ingeniería inversa.

5. Si la carpeta `MINEDU_2026/_DOCUMENTACION_PROYECTO/` no está montada, solicitar acceso a `C:\Users\Hans\Proyectos\COWORK\MINEDU_2026` antes de escribir.

## Verificación cruzada Proveído ↔ archivos físicos (REGLA OBLIGATORIA — v9.8)

Antes de emitir el veredicto, el agente DEBE realizar dos verificaciones cruzadas:

### A) Pertenencia de cada archivo al expediente
Para cada PDF en la carpeta del expediente:
1. Extraer el código de expediente que aparece en el propio PDF (suele decir `EXPEDIENTE: <CÓDIGO>` o aparece en el SINAD).
2. Comparar con el código de la carpeta.
3. Si no coinciden → aplicar la **Clasificación de documentos ajenos (v10.0)**, que decide si es observación o solo nota.
4. No basta con que el nombre del archivo sea coherente; hay que leer el contenido del PDF, porque archivos pueden venir mal nombrados o haber sido arrastrados por error.
5. **A la inversa** (v9.9): un nombre de archivo que alude a otra persona o a otro trámite NO basta para declararlo ajeno. Comparar el CONTENIDO (si es necesario, con `diff` contra la copia que sí obra en el expediente de contratación) antes de observar. Un antecedente legítimo puede citar otro N° de expediente (p. ej. la autorización del VMGP tramitada en su propio SINAD) sin ser un documento ajeno.

### A.1) Clasificación de documentos ajenos (REGLA OBLIGATORIA — v10.0)
Un documento ajeno solo se observa si hay riesgo real para el pago. Clasificar cada uno:

**OBSERVACIÓN** (cualquiera de estos supuestos):
- Corresponde a **otra persona, proveedor, contrato u orden** (p. ej. una conformidad, RHE, factura, informe o entregable de otro contratista).
- **Tergiversa o contradice** los datos del expediente (proveedor, RUC, OS/OC, montos, armada, fechas, conformidad).
- Se usa como **sustento** de este pago (lo cita el Proveído, la Conformidad o el Informe), o **reemplaza** a un documento exigible que falta.

**NO OBSERVAR — solo nota** (Ley 27444):
- Documento institucional sin relación con el pago (circulares, oficios múltiples, directivas, resoluciones generales, comunicaciones de otras oficinas) que no menciona al proveedor ni a la OS/OC, no altera ningún dato, y el expediente está completo sin él.
- En el checklist: `estado: "N.A."` y comentario "Documento ajeno sin relación con el pago; no se observa (Ley 27444). Descartar del legajo". En `coherencia`: `resultado: "OK (nota)"`. **NO** va en `observaciones` y **NO** cambia el veredicto.

Antes de clasificar, leer el contenido: buscar el nombre/RUC del proveedor, el N° de OS/OC y los montos del expediente dentro del documento ajeno.

### B) Cobertura del proveído por archivos físicos
1. Listar todos los documentos citados en el Proveído de Devengado (conformidades, informes, facturas, RHE, formatos de cálculo de penalidad, CCI, etc.) por número y código.
2. Para cada documento citado, verificar que exista un archivo físico en la carpeta cuyo contenido lo respalde.
3. Si falta alguno → **OBSERVACIÓN OBLIGATORIA** "Documento citado en el Proveído pero ausente en la carpeta: `<nombre + número>`".
4. Inversamente: si hay archivos en la carpeta que NO están citados en el proveído NI son anexos lógicos (TDR, contrato base, sustento), levantar nota "Archivo no referenciado en el proveído — verificar pertinencia".
5. Si obran **dos versiones del mismo Proveído** (una sin firma y otra suscrita), trabajar sobre la suscrita y dejar nota indicando que la copia sin firma debe descartarse.

### Implementación en el JSON
Agregar filas en la sección `coherencia` del JSON:
- `{"campo": "Pertenencia al expediente", "valor_doc1": "<código carpeta>", "doc1": "Carpeta", "valor_doc2": "<código en cada PDF>", "doc2": "Cada PDF", "resultado": "OK | OK (nota) | INCONSISTENTE"}` — "OK (nota)" cuando solo hay documentos ajenos inocuos (A.1).
- `{"campo": "Proveído ↔ archivos físicos", "valor_doc1": "<lista citada>", "doc1": "Proveído", "valor_doc2": "<lista presente>", "doc2": "Carpeta", "resultado": "OK | INCONSISTENTE"}`
- `{"campo": "Firma de los cuadros de penalidad", "valor_doc1": "<hallazgo>", "doc1": "Cuadros de penalidad", "valor_doc2": "Exigible: cuadro detallado y firmado", "doc2": "Pautas MINEDU numeral 11", "resultado": "OK | INCONSISTENTE"}`
- `{"campo": "Importe de penalidades: cuadros vs Proveído", "valor_doc1": "<importes de los cuadros>", "doc1": "Cuadros de penalidad", "valor_doc2": "<líneas PENALIDAD y TOTAL del proveído>", "doc2": "Proveído", "resultado": "OK | INCONSISTENTE"}`

Para cualquier cuadro de penalidad sin firma, o archivo ajeno que caiga en el supuesto de OBSERVACIÓN de A.1, agregar un ítem al `checklist` con `estado: "OBSERVABLE"` y un registro en `observaciones`. Los archivos ajenos inocuos van con `estado: "N.A."` y sin registro en `observaciones`.

### Caso de referencia
TRA2026-INT-0278721 (06-04-2026): se encontró el archivo `CONFORMIDAD-00139-2026-MINEDU-VMGP-DIGESE-DEBEDSAR.pdf` que pertenece al expediente DEBEDSAR2024-INT-0763236 (PROXUS SECURITY S.A.C., COAR Tacna). En la verificación inicial NO se detectó porque solo se revisó el nombre del archivo y no su contenido. Esta regla obliga a leer el código de expediente dentro de cada PDF.

### Caso de referencia (v10.0)
USE2026-INT-0634230 (10-09-2026, OS 5485-2026, CACERES CORDOVA LURIA THANI, UE 026, armada 2 de 4): el expediente estaba completo (Proveído 12914, Conformidad 00590 sustentada en el Informe 0793, RHE E001-160 con Constancia 1609 vigente, entrega a tiempo), pero en la carpeta había tres PDF de otros expedientes: Oficio Múltiple 00019-2026-MINEDU/SPE-OTIC, RSG 063-2026-MINEDU y Oficio Múltiple 00042-2026-MINEDU/SPE-OTIC, todos sobre la Directiva de Seguridad de la Información. En la primera revisión se observaron como "documentos ajenos" y se emitió "Sí hay observaciones". **Era incorrecto**: no mencionaban al proveedor ni a la OS, no alteraban ningún dato ni sustentaban el pago. El veredicto correcto es **"No hay observaciones"**, con una nota para descartarlos. De ahí la regla A.1.
# Verificaciones Operativas — Control Previo OS/OC

Detalle operativo de las 7 verificaciones del SKILL.md, con casos típicos y errores a evitar.

## Verificación 1 — Clasificación del expediente

Determinar antes de cualquier otra cosa:

| Variable | Valores posibles |
|----------|------------------|
| Tipo de contratación | CM (≤8 UIT), AS, CP, LP, Consultor Individual, Servicios Básicos, Acuerdo Marco, Convenio compra boletos |
| Tipo de pago | Armada única / 1ra / 2da / posterior |
| Naturaleza proveedor | Persona Natural / Persona Jurídica |
| Comprobante | RHE / Factura Electrónica / Boleto Aéreo / Otro |

**Fuente**: Carta Contrato u Orden de Servicio/Compra, ficha RUC, proveído.

## Verificación 2 — Documental

Aplicar `references/checklist-documentos.md`. Marcar cada ítem ✔ / ⚠ / ❌. Recordar: si es armada posterior, la lista exigible se reduce.

## Verificación 3 — Coherencia documental

Construir mentalmente esta tabla y completarla con datos del expediente:

| Campo | TDR | OS/Carta | Conformidad | RHE/Factura | Proveído |
|-------|-----|----------|-------------|-------------|----------|
| Proveedor | | | | | |
| RUC | | | | | |
| Nº OS/OC | | | | | |
| Nº armada | | | | | |
| Monto armada | | | | | |
| Descripción servicio | | | | | |

Observar **solo** cuando hay inconsistencia REAL entre dos o más documentos sobre datos sustantivos. Errores de tipeo accesorios → no observar.

## Verificación 4 — Matemática

```
Monto contractual = Σ armadas previstas
Armadas pagadas previas = Σ armadas anteriores conformadas
Saldo por devengar (Control Previo) = Monto contractual – Armadas pagadas previas
                                    = Armada actual + Armadas futuras
```

**Caso típico**: contrato S/15,000 en 3 armadas de S/5,000. Al revisar la 3ra armada, el proveído consigna:
- Monto devengado: S/10,000 (las dos anteriores)
- Saldo por devengar: S/5,000 (la armada actual)

→ **CORRECTO**, no observar.

## Verificación 5 — Plazos

Cómputo inclusivo: el día de inicio cuenta como día 1.

**Ejemplo**: Inicio 05/01/2026, plazo 90 días → fin = 04/04/2026. Si el 04/04/2026 es sábado, el primer día hábil siguiente es válido.

Comparar:
- Fecha inicio servicio
- Fecha fin nominal
- Fecha de presentación del entregable
- Fecha de la conformidad
- Fecha del RHE / factura

**NO observar** si la conformidad o el RHE son anteriores al fin nominal de la armada (presentación anticipada).

## Verificación 6 — Tributaria

### Diagrama de decisión RHE (CORREGIDO)

```
¿RHE tiene retención del 8% efectiva (≠ 0.00)?
├── SÍ → CONFORME. No exigir suspensión.
└── NO (Retención 8% IR = 0.00) →
    ¿Existe Constancia de Suspensión de Retenciones de 4ta categoría
    SUNAT vigente para el ejercicio fiscal en curso, en CUALQUIER parte
    del expediente?
    ├── SÍ → CONFORME.
    └── NO → OBSERVABLE: falta constancia de suspensión SUNAT vigente
              que sustente la no retención.
```

**ADVERTENCIA — Inciso A del Art. 33 LIR**: La frase "Inciso A del Artículo 33 de la Ley del Impuesto a la Renta" aparece **siempre** en todos los RHE como referencia normativa estándar; define qué son rentas de cuarta categoría. **NO es base de exoneración de retención**. La única base válida para no retener es la Constancia de Suspensión SUNAT vigente. No usar el Inciso A como atajo para no observar.

**Coherencia de montos RHE vs Proveído**: El proveído consigna el **monto bruto** (Total por honorarios). El RHE muestra bruto, retención y neto. Que el "Sub Total" del proveído sea igual al bruto del RHE (no al neto) es lo correcto: el bruto va al devengado, la retención del 8% se transfiere a SUNAT y el neto se abona al locador. No observar como inconsistencia.

### Factura

- ¿Servicio afecto a detracción? → exigir constancia y, si aplica, comprobante de depósito en BN.
- Verificar fecha de emisión dentro del ejercicio fiscal vigente.
- Verificar emisión a nombre de la UE correcta (RUC y dirección fiscal de la tabla del SKILL.md).

### Boletos aéreos

- El boleto **es** el comprobante de pago. No exigir factura adicional.
- Verificar que el contrato sea por convenio de compra de boletos.

## Verificación 7 — Firmas

Documento con firma válida si tiene **cualquiera** de:
- Firma digital (Ley 27269) — verificable en apps.firmaperu.gob.pe
- Firma manuscrita acompañada de nombre, DNI, cargo
- QR / código de validación institucional

**Excepción**: NO exigir firma manuscrita en RHE ni Factura Electrónica.

---

## Errores frecuentes a evitar (lecciones aprendidas)

1. **No aplicar OCR EXHAUSTIVO al expediente completo** → es la causa #1 de falsos positivos. El RHE, la Constancia de Suspensión 4ta Categoría (Form. 1609), conformidades y otros comprobantes pueden estar como página escaneada (imagen) en CUALQUIER PDF y CUALQUIER página del expediente, no necesariamente cerca del RHE ni en orden lógico. Procedimiento obligatorio: construir un **corpus OCR consolidado del expediente entero** (todas las páginas image-only de todos los PDFs) y buscar sobre ese corpus por al menos 3 términos (RUC del proveedor + "1609" + "Suspensión", o equivalentes según el documento). Declarar "ausente" sin haber agotado este barrido es una falla grave del control previo.
1-bis. **Buscar la Constancia 1609 solo cerca del RHE**. La constancia puede estar varias páginas antes o después, en otro PDF distinto, o en el Informe Técnico. SIEMPRE buscar en el corpus completo del expediente.
2. **Observar campos en blanco de Nº de Contrato** cuando se trata de Carta Contrato (CM). No es observable.
3. **Observar conformidad emitida antes del fin nominal de la armada**. Es presentación anticipada, no es observable.
4. **Observar saldo por devengar que incluye la armada actual**. Es correcto en Control Previo.
5. **Tomar el "Inciso A del Art. 33 LIR" del RHE como base de exoneración**. Es solo una referencia normativa estándar, no una exención. La base real para no retener es la Constancia de Suspensión SUNAT vigente.
6. **Exigir firma manuscrita en RHE/factura electrónica**. Son documentos electrónicos válidos por sí mismos.

## Veredicto final

- **No hay observaciones.** → expediente CONFORME, pase a Coordinación Financiera.
- **Sí hay observaciones.** → enumerar directo, sin justificar, sin indicar archivo ni página.

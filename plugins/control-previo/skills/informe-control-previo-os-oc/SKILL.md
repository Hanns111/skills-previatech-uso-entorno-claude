---
name: informe-control-previo-os-oc
description: "Formato de salida ÚNICO del informe Excel de control previo de expedientes de pago de Órdenes de Servicio y Órdenes de Compra del MINEDU: siete hojas del Protocolo v1.1 — dictamen, proveído, expediente, firmas, validaciones del TDR, tabla tributaria y protocolo versionado — con enlaces a los PDF y páginas en columna aparte. La norma y el criterio de OS y OC los aporta la skill control-previo-ordenes; esta skill define cómo se presenta el resultado. NO se usa en viáticos, encargos ni caja chica."
---

# Informe de control previo de OS y OC — Protocolo v1.1

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


Formato acordado con el especialista de la Coordinación de Control Previo del MINEDU. Iterado el 18/09/2026 sobre el expediente DEBEDSAR2026-INT-0675957 (OS 0006295-2026, UE 026).

## When to use
Solo para expedientes de Orden de Servicio u Orden de Compra. Cuando haya que revisar un expediente de pago de Orden de Servicio u Orden de Compra del MINEDU y emitir el informe Excel: control previo de OS/OC, trámite de devengado, proveído de devengado, conformidad, recibo por honorarios, factura, armadas, contratación menor a 8 UIT, locación de servicios.

## Regla cero: dos categorías y ninguna más
Todo resultado es **OBSERVACIÓN** (hecho verificable en el legajo) o **VERIFICAR** (no se pudo ver por falta de legibilidad, o no se pudo consultar en un portal externo). Prohibidas las categorías «hallazgo», «constancia», «nota» y «no exigible» como filas de un cuadro de resultados. Un hecho verificable o se observa, o no existe.

## Reglas de criterio (no se alteran)
1. Ninguna observación dice a quién comunicar: la devolución ya lo implica.
2. Cada observación cita la norma con su numeral: 5.1.9 de las Pautas, numeral del TDR, numeral del memorándum de requerimiento del área usuaria, o artículo de la Ley 27444 / Ley 32069 / su Reglamento. Si ni las Pautas ni el TDR lo exigen, decirlo en la misma celda.
3. **Archivo enlazado y página en columna aparte.** Penúltima columna: nombre real del PDF como hipervínculo `file:///C:/<carpeta>/<archivo>#page=N`. Última columna: página o rango como «62 de 72», «3-4 de 50». Nunca la página dentro del nombre ni del comentario. **Aplicar formato TEXTO a la columna de páginas ANTES de escribir**, o Excel convierte «2 y 7-11» y «4 / 5» en fechas.
4. Cabecera de toda hoja: nombre del locador y su DNI, expediente, orden y UE, armadas («1 de 1 — pago único»), importes y fecha de revisión. **Prohibido** «revisor», cargo del comisionado, jefe inmediato, coordinador administrativo y encargatura: son campos de viáticos.
5. Título con semáforo: rojo si hay observaciones, verde si no, banda amarilla adicional para lo pendiente de verificación humana.
6. Separar siempre, en cuadros distintos y de distinto color, lo que exigen las Pautas de lo que se valida por criterio técnico.
7. **Duplicidad y documentos ajenos NO se observan** mientras la documentación base esté completa: basta retirarlos del legajo.
8. **RNP según cuantía**: el art. 24 c) del Reglamento de la Ley 32069 exime de inscripción a las contrataciones ≤ 1 UIT. Comparar el monto contra la UIT del ejercicio y escribir la operación. Si el Reporte de contratación lo declara adjunto y no obra, la observación es por la veracidad de la declaración, no por la ausencia del registro.
9. **Perfil del TDR**: descomponer el requisito en sus vías alternativas antes de observar. Si el TDR admite «técnico egresado» y el proveedor lo acredita, el requisito está cumplido aunque otra vía exija «titulado».
10. Lenguaje llano: nada de píxeles, capas de texto, OCR ni nombres de herramientas. Se escribe «escaneado como fotografía», «firma escaneada», «revisión a simple vista».
11. Nunca inventar norma ni dato: lo que no se pudo leer o consultar va a VERIFICAR con su motivo.

## Verificaciones obligatorias
- **Firmas** (ver skill `deteccion-firmas-expedientes`; si no estuviera instalada, aplicar igualmente sus tres vías: bloque de firma electrónica, firma escaneada en el espacio de suscripción y lectura de la página como imagen): ningún documento exigible sin firma. No se exige a comprobantes electrónicos, constancias SUNAT ni cargos.
- **Coherencia documental** (ver skill `coherencia-documental-expedientes`; si no estuviera instalada, construir igualmente la matriz dato por dato antes de observar): distinguir campos de nivel contrato de los de nivel armada antes de observar diferencias de montos.
- **Cadena de aprobación**: el entregable existe, es el producto que el TDR exige, corresponde a la orden, y la conformidad la otorga exactamente la unidad designada en el TDR con el informe previo que el TDR condicione.
- **Notificación de la orden al proveedor**: obligatoria en el primer pago; sin ella no hay contrato ni inicio de plazo (art. 91 del Reglamento de la Ley 32069).
- **Cruce con el SIAF web público**: obligatorio en cada armada. Consulta Amigable del MEF (`apps5.mineco.gob.pe/transparencia/Navegador/default.aspx`), de libre acceso: pliego, unidad ejecutora, específica de gasto, meta y expediente SIAF del proveído.
- **Medidas temporales vigentes**: una fila por cada una, citada con número, fecha y firmante, y verificada contra las fechas del expediente. Vigente: **Oficio Múltiple N.º 00096-2026-MINEDU/SPE-OPEP** del 12/09/2026, que precisa la RM 523-2026-MINEDU (07/09/2026): la certificación presupuestaria la otorga ahora la UPP de la OPEP; para bienes, servicios y obras la solicitud va por la Oficina de Logística, que la eleva a la UPP. Certificaciones anteriores al 12/09/2026 otorgadas por la OCCP son válidas.
- **Tributario**: leer tasas y umbrales de la hoja TRIBUTARIO del libro, no consultarlas de nuevo. Revalidar cada 15 días. Verificar: comprobante **al crédito** con cuotas y vencimiento; **importe neto** expresamente consignado; detracción (umbral general **S/ 700**; transporte de bienes **S/ 400**; Anexo 1 media UIT; 12% demás servicios gravados, 10% arrendamiento y similares, 4% construcción y transporte de bienes); retención del IGV 3% sobre pagos mayores a S/ 700; retención de 4.ª categoría 8% sobre recibos mayores a S/ 1,500, salvo Formulario 1609 vigente. Un recibo por honorarios nunca está sujeto a detracción ni a retención del IGV: no está gravado con IGV. Escribir el cálculo de control aunque no corresponda deducción.

## Estructura del libro (siete hojas)
1. `DICTAMEN <7 dígitos del SINAD> <primer nombre> <primer apellido>` — máx. 31 caracteres. Cuadro de observaciones y cuadro VERIFICAR.
2. `PROVEIDO <número>` — un campo del proveído por fila, sin omitir ninguno, con su documento fuente. Columna del valor en formato TEXTO.
3. `EXPEDIENTE` — Cuadro A azul (Pautas, numeral 5.1.9, con exigibilidad por armada) y Cuadro B morado (validaciones por criterio).
4. `FIRMAS` — quién debe firmar y por qué norma, quién firmó, cómo se detectó.
5. `TDR VALIDACIONES` — Cuadro A cadena de aprobación, Cuadro B cumplimiento punto por punto del TDR (numeración como TEXTO), Cuadro C incoherencias.
6. `TRIBUTARIO` — reglas del comprobante, tabla de tasas y umbrales con su fecha de revalidación, y aplicación al comprobante del expediente.
7. `PROTOCOLO ACUERDOS v<versión>` — Cuadro A acuerdos de criterio, Cuadro B especificación técnica, Cuadro C normas aplicadas, Cuadro D bitácora de versiones con fecha y expediente SINAD de cada iteración.

## Paleta y formato
Banda 1 azul `#1F3864` blanco 10 pt · banda 2 roja `#C00000` blanco 17 pt · veredicto `#FBE4E4`/`#C00000` u `#E2EFDA`/`#00792E` · aviso `#FFF2CC`/`#BF8F00` · etiquetas de cabecera `#D9E2F3` · encabezados de cuadro: observaciones `#7B0000`, verificar `#BF8F00`, Pautas `#1F3864`, criterio `#7030A0`, incoherencias `#C00000`, bitácora `#00792E`.
Estados: ✔ `#00792E` sobre blanco · ✘ `#C00000` sobre `#FBE4E4` · ⚠ `#BF8F00` sobre `#FFF2CC` · – `#808080` sobre `#F2F2F2`, símbolo a 16 pt centrado.
Cuadrícula desactivada, paneles congelados hasta el encabezado del primer cuadro, enlaces de corroboración al pie en dos columnas a 8 pt.

## Orden de construcción
1. Extraer texto y contar páginas de todos los PDF. 2. Reconocer por imagen las páginas sin texto. 3. Detectar firmas. 4. Construir la matriz de coherencia. 5. Clasificar cada resultado en observación o verificación. 6. Escribir las hojas en orden. 7. **Releer cada rango escrito** y comprobar el texto mostrado. 8. Generar la cédula de verificación externa en PDF. 9. Agregar la fila de la iteración al Cuadro D del protocolo con fecha y expediente SINAD, y subir la versión.
**Done when:** las siete hojas existen, fueron releídas, el recuento de cada leyenda coincide con sus filas, y la bitácora tiene la fila de esta iteración.

## Entregable adicional
Cédula de verificación externa en PDF: bloque I con las comprobaciones que no se pudieron ejecutar y columnas en blanco para resultado, fecha y firma; bloque II con las observaciones y el documento a requerir; bloque III con los criterios normativos por los que no se observó; bloque IV con los enlaces.

## Semaforo y cuadros vacios
- La banda del titulo va **roja** solo si hay al menos una observacion, y **verde con letra blanca cuando no hay ninguna**. La franja de veredicto la acompana con el mismo color, en las siete hojas.
- **Sin observaciones, el cuadro de observaciones NO se escribe**: ni encabezado, ni fila «Sin observaciones». El bloque se omite entero y lo que se reviso y no se observo va al cuadro FUNDAMENTO DE LA CONCLUSION.

## Color por resultado, no por tipo de cuadro
El rojo es exclusivo de una observacion real. Ningun cuadro se pinta de rojo por su nombre.
- Cuadro sin filas: se omite entero, con su encabezado.
- Cuadro cuyas filas salieron todas conformes: encabezado verde. Alcanza al cuadro de incoherencias, que en ese caso se titula «CUADRO C - COHERENCIA DOCUMENTAL - SIN INCOHERENCIAS».
- El cuadro de normas aplicadas es un catalogo, no un hallazgo: va azul, nunca rojo.
- Pendiente de verificacion humana: ambar, nunca rojo.
- Antes de guardar el libro: si el conteo de observaciones es cero, no puede quedar ni una celda roja en ninguna hoja.

## Que va en la banda de cada hoja
En las siete hojas, sin excepcion:
- **Banda del titulo, arriba**: el titulo de la hoja seguido del **numero de expediente E-SINAD**. Ejemplo: DICTAMEN DE CONTROL PREVIO - EXPEDIENTE DEBEDSAR2026-INT-0675929.
- **Franja de veredicto, debajo**: el resultado de esa hoja y, al final, el **numero de la orden de servicio o de compra**.
El expediente E-SINAD manda sobre el numero de orden: es el dato que identifica el tramite.

---
name: control-previo-viaticos-v3
description: "Control previo de expedientes de rendicion de viaticos MINEDU. Entregable unico: un Excel de tres hojas con cabecera fija, veredicto en rojo o verde, gasto diario por dia, checklist de documentos y firmas, y comprobantes. Aplica la Directiva DI-003-01-MINEDU V03 (RSG 023-2026-MINEDU) y los Oficios Multiples 00010 y 00016-2026-MINEDU/SG-OGA. Usar cuando el usuario mencione expediente de viaticos, rendicion de viaticos, planilla de viaticos, control previo, Anexo 3, declaracion jurada, comprobantes de comision de servicios, o adjunte PDFs de rendicion SIGA-VIATICOS. Es dominio y salida a la vez: no usa el formato de dos hojas de informe-control-previo-minedu ni el Protocolo v1.1 de siete hojas de informe-control-previo-os-oc, que son de otros tipos de expediente."
---

# Control Previo — Rendicion de Viaticos MINEDU

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


> **FORMATO OFICIAL v7.0** — 18/09/2026. Unica version vigente.
> Deja sin efecto el formato v5.5 de cuatro hojas, el v6.0 de seis hojas y el HTML espejo.
> El entregable es UN solo Excel de tres hojas. Las reglas de criterio siguen vigentes integras.

## Marco normativo

PDFs en `references/normativa/`:

1. **Directiva DI-003-01-MINEDU V03** — viaticos por comision de servicios (05.02.2026)
2. **RSG N. 023-2026-MINEDU** — aprobatoria de la Directiva V03
3. **Oficio Multiple N. 00010-2026-MINEDU/SG-OGA** — Precisiones
4. **Oficio Multiple N. 00016-2026-MINEDU/SG-OGA** — Verificacion ACTIVO Y HABIDO

Toda observacion cita el numeral textual. **Prohibido inventar numerales.**

---

## PRINCIPIO RECTOR

El control previo verifica **sustancia**, no formalismos. Una observacion solo procede cuando concurren:

1. Existe un **defecto real** frente a un numeral expreso de la Directiva.
2. Ese defecto es **subsanable** por el comisionado o por el area.
3. Su subsanacion **cambia algo** en el fondo: monto, sustento, trazabilidad o legalidad del gasto.

Si la trazabilidad esta intacta, el gasto acreditado y el cuadre exacto, **no se observa**. Ante la duda y sin evidencia concluyente del defecto, **no se observa**.

---

## ENTREGABLE UNICO

`INFORME_CONTROL_PREVIO_VIATICOS_<EXPEDIENTE>.xlsx`, guardado **siempre dentro de la carpeta del expediente**, junto a los PDF. No se entrega HTML, ni archivos de trabajo, ni copias intermedias, ni plantillas sueltas.

Tres hojas, en este orden: **INFORME · CHECKLIST · COMPROBANTES**.

Lo lee un especialista de control previo: **cero lenguaje informatico**. Nada de resoluciones de imagen, OCR, motores, versiones, formulas ni nombres de herramienta en las hojas visibles.

### Cabecera fija — identica en las tres hojas, inmovilizada y repetida al imprimir

- **Fila 1 · Tramite:** expediente E-SINAD · planilla de viaticos · solicitud de viaticos · fecha del informe · numero de ronda.
- **Fila 2 · Comisionado:** apellidos y nombres · DNI · cargo o servicio; si es locador se escribe «Locador de servicios» con el numero y la vigencia de su orden de servicio · regimen o modalidad contractual · escala aplicable y tarifa diaria.
- **Fila 3 · Responsables:** jefe inmediato superior que autorizo la comision, nombre, cargo y estado de su firma · coordinador administrativo o quien haga sus veces, nombre y estado de su visacion.
- **Fila 4 · Comision y dinero:** organo solicitante · unidad ejecutora · ruta · periodo y dias de viatico reconocidos · otorgado · rendido · devuelto.

El cargo del comisionado sale del Formato de Alertas y del Plan de Trabajo Diario. Los nombres del jefe y del coordinador salen de los sellos de firma digital.

### HOJA 1 · INFORME

1. **Franja de veredicto**, debajo de la cabecera, ancho completo: roja con «EXPEDIENTE OBSERVADO» y el conteo, o verde con «SIN OBSERVACIONES».
2. **Observaciones**, una fila cada una: N° · que se observa · documento y pagina · numeral · quien subsana · como se subsana · una columna por ronda. Debajo, en ambar, los puntos por verificar y los asuntos que requieren criterio de la OGA por el Num. 8.9.
3. **Texto para el E-SINAD:** una celda con las observaciones consolidadas en 500 caracteres como maximo, lista para copiar.
4. **Gasto diario por dia**, una fila por dia de comision, columnas en este orden: dia y fecha · alimentacion · hospedaje · movilidad local · traslados hacia y desde el terminal o aeropuerto · **subtotal que computa al tope** · de ese subtotal con comprobante · de ese subtotal con declaracion jurada · **tope del dia** · exceso · margen · pasajes interprovinciales · combustible · otros gastos de viaje · **subtotal que no computa** · **total gastado del dia** · resultado.
   Los pasajes, el combustible y los otros gastos de viaje **se muestran siempre y suman en el total del dia, pero quedan fuera del subtotal que se compara contra el tope**: se separan, no se retiran. Linea fija con la base legal: Num. 4.1.18 para lo que es viatico, y Num. 4.1.8, 4.1.5 y 4.1.7 para lo que no lo es. El exceso de un dia no se compensa con el margen de otro.
5. **Cuadre economico, seis filas:** otorgado · con comprobante · con declaracion jurada · total rendido · devuelto acreditado · saldo pendiente o monto en revision.
6. **Topes y proporciones, tres filas:** proporcion del 70 y del 30 de los Num. 6.4.7 y 6.4.17 · topes de movilidad rendida por declaracion jurada del Num. 6.4.18 · resultado.
7. **Plazo, cinco filas:** fin de comision · vencimiento de los diez dias habiles del Num. 6.4.2 · registro en el SIGA · remision a control previo con el dia habil consumido · en poder de quien esta el expediente.
8. **Validaciones**, tres columnas: que se valido · fuente y fecha · resultado. Filas: validez del comprobante en SUNAT · ficha RUC del emisor, activo y habido, Oficio 00016 · regimen del emisor frente al comprobante presentado · comprobante a nombre de la unidad ejecutora con su RUC y la direccion fiscal Calle El Comercio 193 San Borja · retencion del IGV del 3% cuando el pago supera S/ 700 · firmas digitales con firmante, cargo, fecha y hora · deposito en la cuenta del Num. 6.4.20 con su recibo de ingreso · cruce con el SIGA. El Registro Nacional de Proveedores y SUNEDU **no aplican a viaticos y no se incluyen**.
9. **Pie:** revisado por, cargo, fecha, controles aplicados y cuantos no conformes.

### HOJA 2 · CHECKLIST DE DOCUMENTOS Y FIRMAS

Una fila por documento: documento y anexo, con la numeracion del SIGA y la de la V03 · numeral que lo exige · aplica, con el motivo cuando es no · obra, si, no o parcial · **firmas que exige el numeral** · **firmas que constan**, con nombre, cargo, fecha y hora · pagina · resultado.

Se listan siempre: los literales a hasta m del Num. 6.4.3; los documentos del requerimiento del Num. 6.1.7, incluida para locadores la orden de servicio vigente con su SCTR y sus terminos de referencia; la Nota de Pago del Num. 6.2.2; el recibo de ingreso del saldo devuelto; y la encargatura o delegacion del Num. 6.4.9 solo si el jefe estuvo ausente.

Las firmas van en la misma fila de su documento. **No hay hoja de firmas aparte.** Ningun documento es conforme por el solo hecho de existir.

### HOJA 3 · COMPROBANTES Y DECLARACION JURADA

Una fila por gasto: fecha · tipo de sustento · numero de documento · proveedor y RUC · concepto · importe del documento · importe imputado · si computa al tope · validez SUNAT · ficha RUC activo y habido · pagina · resultado. Al pie: total con comprobante, total con declaracion jurada y total rendido, que debe cuadrar al centimo con la hoja 1.

### Reglas fijas del archivo

1. **Cuatro estados visibles:** CONFORME · OBSERVADO · POR VERIFICAR · NO APLICA. El rojo es exclusivo de OBSERVADO y de los excesos de tope; verde para conforme, ambar para por verificar, gris para no aplica.
2. **Toda fila lleva pagina.** Sin pagina, la fila no entra.
3. **Nada de celdas vacias:** lo que no aplica dice «—» o NO APLICA.
4. **Cada ronda de subsanacion agrega una columna**, nunca reescribe la observacion original.
5. **Sin dashboard, sin graficos, sin hoja de metodologia, sin hoja de conclusiones, sin hoja de evidencias, sin leyenda de estados.**
6. **No se inventan datos ni conclusiones.** Si falta un dato acreditado, la fila dice POR VERIFICAR.
7. **No hay cambios silenciosos de criterio legal:** todo cambio se dice y se sustenta.

---

## PROCEDIMIENTO PARA UN EXPEDIENTE

1. **Leer todos los PDF pagina por pagina**, anotando archivo y pagina de cada dato. Las paginas sin texto se leen como imagen.
2. **Antes de observar una diferencia de digitos** —planilla, comprobante, monto, fecha, RUC, DNI, cuenta— leer el dato ampliado sobre la imagen. Una lectura dudosa no sustenta una observacion.
3. **Antes de declarar que falta un comprobante**, revisar la pagina completa y sus cuadrantes: una sola pagina puede traer varios comprobantes.
4. **Antes de declarar que falta una firma**, revisar toda la pagina, incluidos margenes y zonas fuera de los casilleros: un sello puesto fuera de su casillero tambien se observa.
5. **Armar la base de gastos**, una linea por imputacion diaria, distribuyendo el hospedaje por noche, y recien entonces evaluar topes y proporciones.
6. **Construir el Excel de tres hojas** segun esta regla y guardarlo en la carpeta del expediente.
7. **Antes de entregar, verificar:** que el cuadre de la hoja 1 coincide al centimo con la hoja 3; que toda fila tiene pagina; que el veredicto concuerda con el numero de observaciones; que ningun texto queda cortado al imprimir; y que no aparece ninguna mencion a la herramienta con la que se produjo.

### Rondas de subsanacion

Cuando el area reingresa el expediente no se hace un informe nuevo: se agrega la columna de la ronda a cada observacion y se indica si quedo levantada o subsiste, con el documento, la pagina y la fecha de la firma que la levanta. El veredicto se recalcula con lo que subsiste.

---

## TOPES Y UMBRALES

- **Escala, Num. 5.4:** S/ 380 por dia para Ministro, Viceministro y Secretario General; S/ 320 para los demas sujetos, incluidos los locadores cuyos terminos de referencia prevean expresamente los viajes.
- **Dia de viatico, Num. 5.12:** mas de 4 horas y hasta 24 horas es un dia; hasta 4 horas, proporcional.
- **Computo de la duracion, Num. 6.1.3:** aereo, 3 horas antes y 2 despues, segun el itinerario de la reserva; terrestre, 2 antes y 1 despues, segun el boleto; movilidad del MINEDU, desde que la unidad sale de las instalaciones hasta que retorna, segun la papeleta de la Coordinacion de Transportes.
- **Declaracion jurada, Num. 6.4.7 y 6.4.17:** hasta el 30% del monto otorgado por viaticos, excluidos los pasajes; solo se aplica a viaticos.
- **Topes del Num. 6.4.18 para movilidad rendida por declaracion jurada:** aeropuerto S/ 35 por servicio en regiones; terrapuerto S/ 25 por servicio en regiones; movilidad local S/ 45 por dia en Lima y S/ 30 por dia en regiones. Un traslado sustentado con comprobante no esta sujeto a estos topes.
- **Plazo, Num. 6.4.2:** diez dias habiles desde el dia siguiente al fin del viaje.
- **Anticipacion del requerimiento, Num. 6.1.7:** cinco dias habiles. Los pedidos fuera de plazo debian tramitarse como reembolso, Oficio 00010.
- **Retencion del IGV del 3%, Num. 4.1.13:** solo cuando el pago supera S/ 700, controlada por comprobante y por acumulado del mismo proveedor.
- **Unidades ejecutoras y cuentas de devolucion, Num. 6.4.20:** UE 024 Sede Central, RUC 20131370998, cuenta 00-068-348331 · UE 026 PEBT, RUC 20380795907, cuenta 00-068-348358 · UE 116 COAR, RUC 20546369383, cuenta 00-068-364728. Direccion fiscal para las tres: Calle El Comercio 193 San Borja.

---

## REGLAS DE CRITERIO

### El plazo se resuelve por TRAMOS DE CUSTODIA, nunca por calendario

PLAZO GLOBAL no es lo mismo que TIEMPO IMPUTABLE AL AREA ni que TIEMPO EN CONTROL PREVIO. **Prohibido** observar por el solo hecho de que pasaron los diez dias habiles: primero debe existir trazabilidad de custodia.

Tiempo imputable al area = del fin del viaje a la remision, mas cada tramo de devolucion con observaciones hasta el reingreso. Todo lo demas es tiempo en Control Previo y no se le imputa. Si no obra cargo de recepcion con fecha propia, el computo toma la fecha de remision, que es el dato acreditado y el mas favorable al area.

Se informan dos resultados distintos: el del **Num. 6.4.2**, sobre la actuacion del area usuaria, y el del **Num. 6.4.4**, sobre el plazo global del tramite. Solo se observa si el area remitio fuera de plazo o si agoto los dias habiles que le son imputables.

Caso de referencia: DIPLAN2026-INT-0785576, BARDALES SALAZAR. El area registro la rendicion el 01/09 y la remitio el 03/09, dia habil 5 de 10. Resultado correcto: 6.4.2 conforme y 6.4.4 plazo global vencido, sin observacion al area.

### REQUIERE CRITERIO para lo que la Directiva no resuelve, Num. 8.9

Cuando la situacion no esta prevista, o el texto de la Directiva y su formato exigen cosas distintas, no es imputable al comisionado: se deja constancia y se eleva al jefe de la OGA. No cuenta como observacion, pero impide declarar el expediente conforme. Caso tipico: con devolucion de saldo, el tope del 30% medido sobre el monto otorgado y sobre el viatico efectivamente rendido da resultados opuestos.

### Un asunto por causa, no por linea

Cuando una misma causa afecta a varias lineas, es UN solo asunto de alcance expediente o requerimiento, no uno por linea. Un asunto de alcance expediente jamas pinta de rojo las lineas de gasto.

### Hospedaje en una sola linea del Anexo 3 NO es observacion

La Directiva no obliga a desagregarlo noche por noche. Es responsabilidad del control previo distribuirlo segun el comprobante, que si trae fecha de ingreso y de salida, Num. 6.4.12, y recien entonces evaluar el tope diario. Sigue siendo observable: hospedaje sin fechas de ingreso y salida; clasificacion erronea en el Anexo 3; hospedaje en el domicilio del comisionado en zona urbana.

### La hora o el momento de emision del comprobante NO es limitante

La Directiva no exige que el comprobante se emita en el momento del consumo. **Prohibido** observar por la hora impresa, por dos comprobantes del mismo dia y proveedor con minutos de diferencia, por emision diferida si el gasto cae en la ventana de la comision, o por mesas o cajeros distintos. Sigue siendo observable: gasto fuera de la ventana de la comision; comprobante duplicado; comprobante que la consulta SUNAT reporta como inexistente.

### La calificacion de «viveres» NO es concluyente

El Num. 6.4.16 no se aplica por el solo giro del emisor. Un minimarket, bodega, supermercado, panaderia o tienda de conveniencia puede emitir un comprobante por alimentacion del comisionado, y eso es lo que corresponde presumir. Sigue siendo observable: bebidas alcoholicas, articulos de uso personal, regalos, lavanderia, tarjetas telefonicas, copias, ornamentales o equipos menores, Num. 6.4.13; alimentacion sin detalle que solo diga «por consumo», Num. 6.4.11; volumenes incompatibles con el consumo de una persona.

### Razon social con nucleo identificatorio y trazabilidad NO es observacion

La razon social del Anexo 3 viene del maestro de proveedores del SIGA y puede diferir en su redaccion. No se observa cuando se conserva el nucleo identificatorio del proveedor y coinciden RUC, numero de comprobante e importe. Lo mismo vale para la direccion de un establecimiento anexo. Sigue siendo observable: RUC distinto, numero de comprobante distinto, importe distinto en perjuicio del fisco, o un proveedor completamente distinto.

### Otras reglas vigentes

- Equivalencia de anexos SIGA y V03 — Anx 01 a 6, 02 a 7, 03 a 8, 04 a 9, 05 a 10, 06 a 11: no observable.
- Subdeclaracion del Anexo 3 por debajo del comprobante: favorece al fisco, no observable.
- Padding de ceros en el numero de comprobante: si la consulta SUNAT valida, no observable.
- «Tarjeta de credito» en texto es la unica forma observable bajo el Num. 6.4.10; «Visa», «POS» o «Yape» por si solos no lo son.
- Copia del deposito sin V°B° de la Caja de Recaudacion: conforme si el Recibo de Ingreso de la unidad ejecutora acredita el ingreso.
- Gasto dentro de la ventana de la comision: conforme.
- Toda observacion cita documento, numeral, base legal textual, accion de subsanacion y pagina.
- Formato de Alertas: revisar todas las paginas antes de declararlo en blanco.

---

## Estructura de la skill

```
control-previo-viaticos-v3/
├── SKILL.md                    ← este documento (formato oficial v7.0)
└── references/normativa/
    ├── 01_DIRECTIVA_DI-003-01-MINEDU_V03.pdf
    ├── 02_RSG_023-2026-MINEDU.pdf
    ├── 03_OFICIO_MULTIPLE_00010-2026-PRECISIONES.pdf
    └── 04_OFICIO_MULTIPLE_00016-2026-ACTIVO_HABIDO.pdf
```

La plantilla `templates/PLANTILLA_..._V3.xlsx` queda obsoleta y no se usa.
---
name: coherencia-documental-expedientes
description: "Skill transversal que cruza dato por dato todos los documentos de un expediente de pago del MINEDU —proveedor, RUC, DNI, orden, armada, montos, deducciones, importe neto, descripción del servicio, fechas y el informe que sustenta la conformidad— antes de emitir cualquier observación. Distingue los campos de nivel contrato de los de nivel armada para no generar falsas observaciones, verifica la cobertura del proveído y la cadena de aprobación, y deja escrito lo que NO se observa y por qué. Se aplica encima de cualquier skill de dominio: órdenes de servicio y compra, viáticos, encargos, caja chica, convenios y sentencias."
---

# Coherencia documental de expedientes MINEDU

Skill **transversal**. No sustituye a la skill de dominio ni a su directiva: le entrega la matriz de coherencia ya construida para que decida.

## Regla de oro

**Primero la matriz, después la observación.** Ninguna diferencia de dato se observa antes de estar ubicada en la matriz, con su documento y su página. Una lectura dudosa nunca sustenta una observación: antes de observar una diferencia de dígitos —monto, fecha, número de comprobante, RUC, DNI, número de cuenta— se lee el dato ampliado sobre la imagen.

## Nivel contrato y nivel armada — la distinción que evita falsas observaciones

Antes de comparar dos importes hay que saber de qué nivel es cada uno.

- **Nivel contrato**: monto total, plazo total, número de armadas, TDR, estructura de costos, carta contrato, número de orden, proveedor y RUC. Se repiten idénticos en todas las armadas.
- **Nivel armada**: monto de la armada, periodo, entregable, conformidad, comprobante, deducciones, importe neto, proveído.

Un monto total que no coincide con el monto de la armada **no es incoherencia**: son dos niveles distintos. La incoherencia existe cuando dos documentos del mismo nivel dicen cosas distintas.

## Matriz obligatoria — campo, valor en cada documento, resultado

Se construye una fila por campo y una columna por documento donde ese campo aparece. Campos mínimos:

1. Proveedor o comisionado, y su RUC o DNI.
2. Número de orden, de carta contrato o de planilla.
3. Armada en revisión y total de armadas.
4. Periodo del servicio o de la comisión.
5. Monto contractual, monto de la armada y saldo por pagar.
6. Deducciones: penalidades, detracción, retenciones.
7. Importe neto, que debe ser el bruto menos las deducciones y coincidir con el proveído y con el comprobante.
8. Descripción del servicio o del gasto, comparada entre TDR, orden, comprobante y conformidad.
9. Fechas: inicio, fin de armada, entregable, conformidad, comprobante, proveído.
10. Informe que sustenta la conformidad, con su número exacto.
11. Unidad ejecutora, su RUC y su dirección fiscal, Calle El Comercio 193 San Borja para las tres.

Cada celda lleva documento y página. Resultado por fila: CONFORME, OBSERVADO o POR VERIFICAR.

## Cobertura del proveído

El proveído debe cubrir **todos** los campos del pago. Se lista un campo por fila, sin omitir ninguno, con su documento fuente, y se marca el que no tenga respaldo en el legajo. Un campo del proveído sin documento que lo sustente es observación; un documento que el proveído no recoge es nota, no observación.

## Cadena de aprobación

Se verifica en este orden y se rompe en el primer eslabón que falle: el entregable existe · es el producto que el TDR o la directiva exigen · corresponde a esta orden y a esta armada · la conformidad la otorga exactamente la unidad designada · el informe previo que la conformidad cita obra y coincide en número · el proveído recoge el resultado · el comprobante corresponde al proveído.

## Lo que NO se observa — se deja escrito

La matriz termina con un cuadro de lo advertido y no observado, con su motivo. Entra aquí:

- Diferencias de redacción de la razón social cuando se conserva el núcleo identificatorio del proveedor y coinciden RUC, número de comprobante e importe.
- Ceros a la izquierda en el número de comprobante cuando la consulta validó.
- Documentos duplicados o ajenos inocuos mientras la documentación base esté completa: basta retirarlos del legajo.
- Presentación anticipada del entregable, de la conformidad o del comprobante.
- Diferencias entre nivel contrato y nivel armada.
- Subdeclaración por debajo del comprobante, que favorece al fisco.

Ese cuadro es el respaldo del revisor: deja escrito lo que vio y decidió no observar.

## Salida

La matriz se entrega a la skill de dominio y se vuelca en el cuadro de coherencia o de incoherencias del formato de salida que corresponda al tipo de expediente. Toda fila lleva documento y página; sin página, la fila no entra.

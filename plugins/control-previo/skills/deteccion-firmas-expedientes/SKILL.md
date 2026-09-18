---
name: deteccion-firmas-expedientes
description: "Skill transversal de verificación de firmas en expedientes de pago del MINEDU. Se aplica encima de cualquier skill de dominio —órdenes de servicio y compra, viáticos, encargos, caja chica, convenios, sentencias— y define las tres vías sucesivas para detectar una firma, quién debe firmar cada documento y cuándo la ausencia de firma es observación. Usar siempre que haya que declarar si un documento está suscrito, si la conformidad la firmó la unidad correcta, si un cuadro de penalidad está firmado o si una firma es incompleta. Prohíbe declarar una firma ausente sin agotar las tres vías."
---

# Detección y verificación de firmas en expedientes MINEDU

Skill **transversal**. No define observaciones de fondo ni interpreta directivas: eso lo hace la skill de dominio del tipo de expediente. Esta skill solo responde tres preguntas: **quién debía firmar**, **si firmó** y **cómo se acreditó**.

## Regla de oro

**Prohibido declarar una firma ausente sin haber agotado las tres vías.** Una firma no detectada no es una firma ausente. Si tras las tres vías la página sigue sin poder leerse, el resultado no es observación: es POR VERIFICAR con su motivo.

## Las tres vías sucesivas

1. **Firma electrónica institucional.** Buscar en el texto del documento el bloque FAU de la unidad ejecutora —20131370998 para la UE 024, 20380795907 para la UE 026, 20546369383 para la UE 116—, el sello FIRMADO DIGITALMENTE, la leyenda «En señal de conformidad», «Doy V° B°», o un código QR o dirección de validación institucional del tipo apps.firmaperu.gob.pe o esinad.minedu.gob.pe. Base: Ley 27269, Ley de Firmas y Certificados Digitales.
2. **Firma escaneada o manuscrita.** Revisar el espacio de suscripción y también los márgenes, el pie, la cabecera y las zonas fuera de los casilleros. Un sello puesto fuera de su casillero cuenta como firma puesta, y su ubicación se anota. La firma manuscrita debe ir acompañada de nombres, apellidos, DNI y cargo del firmante; si falta alguno, el resultado es INCOMPLETA, no ausente.
3. **Lectura de la página como imagen.** Cuando las dos vías anteriores no arrojan nada y la página no tiene texto legible, se revisa la página a simple vista sobre la imagen ampliada. Los sellos y las rúbricas gráficas rara vez son texto.

**Firmas dispersas:** revisar TODAS las páginas del PDF antes de concluir. Una firma puede estar en la segunda, la tercera o la última hoja del mismo archivo.

## Estados admitidos

- **OK** — firma electrónica válida, o manuscrita completa con nombres, DNI y cargo.
- **INCOMPLETA** — manuscrita sin DNI o sin cargo, o suscrita por persona distinta de la exigida.
- **AUSENTE** — agotadas las tres vías y revisadas todas las páginas, no hay ninguna forma válida de suscripción. Esto sí es observación.
- **NO APLICA** — reservado exclusivamente a documentos no suscribibles: recibo por honorarios electrónico, factura electrónica, constancias de la SUNAT y cargos de mesa de partes.

## Prohibiciones expresas

- **Prohibido exigir firma manuscrita** en recibo por honorarios electrónico o factura electrónica: son válidos por sí mismos.
- **Prohibido marcar NO APLICA en un cuadro o informe de aplicación de penalidad.** Ese documento siempre requiere suscripción. Que venga del SIGA o del SGC con fecha y hora de sistema no reemplaza la firma. Sin firma va AUSENTE y observación obligatoria.
- **Prohibido despachar la falta de firma de un cuadro de penalidad como error formal accesorio** bajo la Ley 27444: ese cuadro sustenta una deducción sobre el pago del contratista.
- **Prohibido observar** por falta de firma en una copia previa sin suscribir cuando en el mismo legajo obra la versión suscrita: prevalece la suscrita, se deja nota y no se observa.

## Quién debe firmar — contraste obligatorio

No basta con que haya una firma: debe ser **la del obligado**. Contrastar contra la norma y contra el documento fuente de cada tipo de expediente.

- **Conformidad** — la firma exactamente la unidad orgánica que el TDR designa como responsable de otorgarla. Si la firma otra área, es observación aunque esté impecablemente suscrita.
- **Informe de conformidad citado en la conformidad** — debe obrar y estar firmado por el área usuaria, y su número debe coincidir con el citado.
- **Cuadros de aplicación de penalidad** — suscritos por el responsable, con importe coherente con el proveído.
- **Órdenes de compra** — distinguir la firma del responsable de almacén, por el internamiento del bien, de la conformidad del área usuaria. Son dos firmas distintas y ninguna suple a la otra.
- **Viáticos** — jefe inmediato superior que autorizó la comisión, y coordinador administrativo o quien haga sus veces para la visación. Los nombres y cargos se toman de los sellos de firma digital.
- **Encargos y caja chica** — el responsable del fondo y quien aprueba la rendición, según la directiva de su propia skill.

## Cómo se registra el resultado

Cada documento lleva, en la misma fila: qué firma exige la norma y con qué numeral, quién firmó con nombre, cargo, fecha y hora, por cuál de las tres vías se detectó, la página, y el estado. Sin página, la fila no entra.

## Lenguaje

Se escribe «firma electrónica del sistema», «firma escaneada», «revisión a simple vista», «página escaneada como fotografía». Nunca píxeles, capas de texto, reconocimiento óptico ni nombres de herramientas.

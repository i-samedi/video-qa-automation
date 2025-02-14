Feature: Seguimiento de Importaciones

Background:
  Given el área de COMEX utiliza la pantalla principal de seguimiento de importaciones
  And la OC aprobada en Oracle se muestra en esta pantalla


@paso_1 @modulo_visualizacion @tipo_acceso
Scenario: 1 Acceso a la pantalla de seguimiento de importaciones
  When el usuario accede a la pantalla de seguimiento de importaciones
  Then se muestra la pantalla de seguimiento de importaciones correctamente

@paso_2 @modulo_visualizacion @tipo_visualizacion
Scenario: 2 Visualización de datos de la compañía
  When el usuario visualiza los datos de la compañía
  Then se muestran el nombre, dirección antigua, bodegas de entrega, RUT, marca, colección y fecha de emisión de la orden de compra

@paso_3 @modulo_visualizacion @tipo_visualizacion
Scenario: 3 Visualización de datos del proveedor
  When el usuario visualiza los datos del proveedor
  Then se muestran el nombre, RUT ficticio, correlativo, número asignado, dirección y otros datos relevantes

@paso_4 @modulo_visualizacion @tipo_visualizacion
Scenario: 4 Visualización de datos de la proforma del proveedor
  When el usuario visualiza los datos de la proforma del proveedor
  Then se muestran el país de origen, puertos de embarque, vía de embarque, factor, cláusula de compra, cláusula FOP y comisión si existen

@paso_5 @modulo_visualizacion @tipo_visualizacion
Scenario: 5 Visualización de fechas y forma de pago
  When el usuario visualiza las fechas y forma de pago
  Then se muestran la factory date, último plazo de embarque, fecha de necesidad y forma de pago

@paso_6 @modulo_visualizacion @tipo_visualizacion
Scenario: 6 Visualización de datos del forward, expeditors y condiciones de embarque
  When el usuario visualiza los datos del forward, expeditors y condiciones de embarque
  Then se muestran si el embarque es parcial, la moneda empleada y gastos adicionales si existen

@paso_7 @modulo_visualizacion @tipo_visualizacion
Scenario: 7 Visualización de datos relacionados a carta de crédito
  When el usuario visualiza los datos relacionados a carta de crédito
  Then no se muestran si la cláusula de compra es WT

@paso_8 @modulo_visualizacion @tipo_visualizacion
Scenario: 8 Visualización del detalle de la orden de compra
  When el usuario visualiza el detalle de la orden de compra
  Then se muestran el número de OC, clase de producto, género, modelo, nombre del producto, color, código, código color, talla, número de la barra, cantidad comprada, cantidad embarcada y precio

@paso_9 @modulo_visualizacion @tipo_visualizacion
Scenario: 9 Visualización de íconos de acción en la pantalla
  When el usuario visualiza los íconos de acción en la pantalla
  Then se muestran los íconos Factura, ASN, Programa, Envío, Reportes, área de Pagos, Borrar, Anulación, Royalty, opciones de anticipos y funciones de carga B y ver B en el booking

@paso_10 @modulo_visualizacion @tipo_visualizacion
Scenario: 10 Visualización de resumen de la compra
  When el usuario visualiza el resumen de la compra
  Then se muestran el total de tareas, unidades equivalentes, sólidos y total de la compra, confirmando que la diferencia es cero cuando la cantidad comprada es igual a la embarcada


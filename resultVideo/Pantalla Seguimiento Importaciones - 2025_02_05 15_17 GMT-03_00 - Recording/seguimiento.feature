Feature: Seguimiento de importaciones

Background:
  Given el usuario está en la pantalla de seguimiento de importaciones
  And tiene acceso a todas las opciones necesarias
  And los parámetros iniciales están configurados


@paso_1 @modulo_seguimiento @tipo_visualizacion
Scenario: 1 Ingreso de orden de compra
  When el usuario ingresa una orden de compra con número "425376"
  Then se despliega toda la información asociada a la OC

@paso_2 @modulo_seguimiento @tipo_visualizacion
Scenario: 2 Visualización de detalles de la OC
  When el usuario observa los datos de empresa, destinos, proveedores y proforma o planilla Excel
  Then se muestran los detalles completos para respaldar la compra

@paso_3 @modulo_seguimiento @tipo_ingreso
Scenario: 3 Ingreso de datos de embarque y costos
  When el usuario selecciona el país de origen, el puerto de embarque y la vía (por ejemplo, marítimo)
  Then se calcula un factor sobre el precio para estimar el costo de poner la mercadería en destino

@paso_4 @modulo_seguimiento @tipo_visualizacion
Scenario: 4 Visualización de formas de pago y forwarder
  When se muestra la sección con WP, LC (Letter of Credit), cobranza y WT
  Then se visualizan las opciones de pago y el forwarder (por ejemplo, Expeditors o THL)

@paso_5 @modulo_seguimiento @tipo_visualizacion
Scenario: 5 Visualización de detalles de productos en la OC
  When el usuario observa la clase, género, modelo, color, talla, código de barra, cantidad y precio
  Then se distinguen los productos comprados por “sólido” (una talla por SKU) o “tarea” (agrupación de tallas)

@paso_6 @modulo_seguimiento @tipo_visualizacion
Scenario: 6 Visualización de la pantalla ASN
  When el usuario accede al icono ASN desde la OC
  Then se muestra un resumen de los productos embarcados y el total de cantidades

@paso_7 @modulo_seguimiento @tipo_revision
Scenario: 7 Revisión de facturas del proveedor
  When el usuario presiona Enter sobre el VL
  Then se despliegan las facturas emitidas por el proveedor
  And se muestran los montos facturados y las diferencias comparados con la OC

@paso_8 @modulo_seguimiento @tipo_programacion
Scenario: 8 Programación y verificación de embarque
  When el usuario ingresa el número de contenedor o VL
  Then se muestra la información de programación (incluyendo fechas estimadas y confirmadas)
  And se visualizan datos del centro de distribución, cantidades, estatus y modalidad de retiro

@paso_9 @modulo_seguimiento @tipo_reporte
Scenario: 9 Generación de reportes y consulta de información
  When el usuario filtra por contenedor, VL, marca, clase, o define un rango de fechas
  Then se genera un reporte resumido o detallado de la OC
  And se permite descargar el reporte en formato Excel

@paso_10 @modulo_seguimiento @tipo_modificacion
Scenario: 10 Modificación de datos de la cabecera de la OC
  When el usuario modifica las fechas u otros datos y graba los cambios
  Then se actualiza la información de la OC en pantalla

@paso_11 @modulo_seguimiento @tipo_eliminacion
Scenario: 11 Eliminación y anulación de información
  When el usuario selecciona eliminar una invoice o anular una OC utilizando la clave de validación
  Then se elimina o anula la información de forma parcial o completa

@paso_12 @modulo_seguimiento @tipo_gestion
Scenario: 12 Gestión de pagos y Royalty
  When el usuario ingresa el valor a pagar y se aplica la retención correspondiente
  Then se muestra el detalle de los pagos y se genera un reporte para Royalty


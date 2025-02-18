Feature: Seguimiento de importaciones

Background:
  Given el usuario está en la pantalla de seguimiento de importaciones
  And tiene acceso a todas las opciones necesarias
  And los parámetros iniciales están configurados


@paso_1 @modulo_importaciones @tipo_visualizacion
Scenario: 1 Visualización de la orden de compra
  When el usuario ingresa el número de la OC "425376"
  Then el sistema despliega la información completa de la orden de compra

@paso_2 @modulo_importaciones @tipo_visualizacion
Scenario: 2 Visualización de datos generales de la OC
  When se visualizan los datos generales
  Then se muestra la empresa registrada y su vínculo mediante RUT

@paso_3 @modulo_importaciones @tipo_visualizacion
Scenario: 3 Inspección de información del proveedor
  When se inspecciona la información del proveedor
  Then se muestra la dirección y los datos generales del proveedor

@paso_4 @modulo_importaciones @tipo_visualizacion
Scenario: 4 Revisión de documentación de soporte
  When se revisa la documentación de soporte
  Then se muestra la proforma o, en otros casos, la planilla Excel acordada entre Comercial y Oracle

@paso_5 @modulo_importaciones @tipo_creacion
Scenario: 5 Creación de la OC con información de conexión
  When el usuario crea la OC
  Then se selecciona el país correspondiente y se selecciona el puerto de embarque adecuado

@paso_6 @modulo_importaciones @tipo_visualizacion
Scenario: 6 Revisión de opciones de embarque
  When se revisan las opciones disponibles
  Then se muestran las opciones: marítimo (la principal), aéreo y terrestre

@paso_7 @modulo_importaciones @tipo_visualizacion
Scenario: 7 Visualización del campo de comisión
  When se visualiza el campo de comisión
  Then el valor aparece como cero

@paso_8 @modulo_importaciones @tipo_visualizacion
Scenario: 8 Inspección de fechas clave de la OC
  When se inspeccionan los detalles de la OC
  Then se muestran la fecha factory, la fecha del último plazo de embarque y la fecha en que la mercadería debe estar disponible

@paso_9 @modulo_importaciones @tipo_visualizacion
Scenario: 9 Visualización de formas de pago
  When se visualiza el campo "forma de pago"
  Then se muestran las opciones: WT (transferencia individual), LC (Letter of Credit) y cobranza (transferencia agrupada por proveedor)

@paso_10 @modulo_importaciones @tipo_visualizacion
Scenario: 10 Visualización del dato del forwarder
  When se visualiza el dato del forwarder
  Then se muestra la opción seleccionada, ya sea Expeditors o DHL

@paso_11 @modulo_importaciones @tipo_visualizacion
Scenario: 11 Inspección de datos financieros de la OC
  When se inspecciona el total y la tolerancia
  Then se muestra el monto total de la OC y, de ser aplicable, el ajuste por tolerancia

@paso_12 @modulo_importaciones @tipo_visualizacion
Scenario: 12 Revisión del detalle de productos
  When se revisa el contenido del detalle
  Then se muestran el tipo de clase, género, modelo, nombre del producto, color (y su código), talla, código de barras, cantidad y cantidad embarcada

@paso_13 @modulo_importaciones @tipo_verificacion
Scenario: 13 Verificación del código de barras
  When se verifica el código de barras
  Then se reconoce si el código tiene 12 o 13 dígitos (producto sólido) o 6 dígitos (agrupa varias tallas en tareas)

@paso_14 @modulo_importaciones @tipo_interaccion
Scenario: 14 Interacción con íconos operativos
  When el usuario interactúa con los íconos (factura, ASN, programa, envío, reportes, consultas, pagos, seguimiento)
  Then el sistema permite acceder a un resumen de la operación y ejecutar la anulación de la OC si esta ya no es vigente

@paso_15 @modulo_importaciones @tipo_visualizacion
Scenario: 15 Selección de ícono de royalty
  When se selecciona el ícono de royalty
  Then se muestran únicamente los proveedores con royalty

@paso_16 @modulo_importaciones @tipo_visualizacion
Scenario: 16 Revisión de la sección de booking
  When se revisa la sección de booking
  Then se muestran los campos de carga, booking y ver booking en cero y deshabilitados


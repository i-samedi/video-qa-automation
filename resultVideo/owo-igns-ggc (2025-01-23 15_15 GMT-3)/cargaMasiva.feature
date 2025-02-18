Feature: Carga masiva de pedidos

Background:
  Given el usuario está en la pantalla principal de la aplicación de carga masiva
  And se visualizan los tipos de pedido en el panel izquierdo con el tipo normal marcado por defecto
  And se muestra la bodega de despacho por defecto (SDFORCE)


@paso_1 @modulo_login @tipo_interaccion
Scenario: 1 Ingreso de nombre de usuario
  When el usuario digita el nombre de usuario
  And presiona Enter para confirmar la bodega por defecto
  Then el cursor se posiciona en el campo RUT

@paso_2 @modulo_cliente @tipo_interaccion
Scenario: 2 Ingreso de RUT del cliente
  When el usuario ingresa el RUT del cliente
  Then el RUT es validado correctamente

@paso_3 @modulo_cliente @tipo_ayuda
Scenario: 3 Búsqueda de cliente por razón social
  When el usuario desconoce el RUT
  And presiona el botón de ayuda
  And escribe parte de la razón social
  And presiona Enter
  Then la aplicación muestra los clientes que coinciden con el patrón

@paso_4 @modulo_cliente @tipo_seleccion
Scenario: 4 Selección de cliente
  When el usuario selecciona el cliente adecuado con doble clic sobre el RUT
  And presiona Enter
  Then la pantalla principal muestra el RUT y la razón social del cliente
  And la aplicación indica que el cliente tiene crédito suficiente

@paso_5 @modulo_pedido @tipo_seleccion
Scenario: 5 Selección de ubicación y condiciones de venta
  When el usuario selecciona la ubicación de destino mediante el combo o a partir de la plantilla
  And selecciona las condiciones de venta
  And digita la orden de compra del cliente
  And presiona Enter
  Then el sistema cambia el campo activo al porcentaje de descuento

@paso_6 @modulo_pedido @tipo_interaccion
Scenario: 6 Ingreso de porcentaje de descuento
  When el usuario ingresa 15% de descuento
  And presiona Enter
  Then el cursor se posiciona en el botón de lectura de archivo

@paso_7 @modulo_archivo @tipo_interaccion
Scenario: 7 Selección y lectura de archivo CSV
  When el usuario selecciona el botón de lectura
  And selecciona el archivo CSV con doble clic
  Then la aplicación lee el archivo y valida cada registro

@paso_8 @modulo_archivo @tipo_validacion
Scenario: 8 Validación de registros del archivo
  Then la aplicación valida el código de tienda, modelo, color, talla, cantidad de pedido
  And marca en rojo las líneas con error y en verde las correctas

@paso_9 @modulo_archivo @tipo_recuperacion
Scenario: 9 Recuperación de datos adicionales
  Then la aplicación recupera datos adicionales como ID del cliente, SiteUsageID, TypeID, ItemID, y otros

@paso_10 @modulo_pedido @tipo_registro
Scenario: 10 Registro de pedidos
  When el usuario activa el botón "Grabar pedido"
  And presiona este botón para registrar el pedido
  Then la aplicación registra los pedidos y asigna un número de pedido a cada grupo de líneas

@paso_11 @modulo_pedido @tipo_agrupacion
Scenario: 11 Agrupación y visualización de pedidos
  Then la aplicación agrupa los pedidos según la marca, clase y género
  And muestra en la pantalla los números de pedido generados

@paso_12 @modulo_inyeccion @tipo_exportacion
Scenario: 12 Exportación de datos de inyección
  When el usuario activa la opción "Pruebas de inyección" y guarda
  Then la aplicación exporta los datos de la inyección
  And el respaldo DBF contiene el detalle de la grilla

@paso_13 @modulo_finalizacion @tipo_validacion
Scenario: 13 Validación final y cierre de aplicación
  Then el usuario valida que la carga se realizó satisfactoriamente
  And que la información en el respaldo coincide con la grilla de la pantalla principal
  And el usuario cierra la aplicación


Feature: Carga de pedidos a bodegas

Background:
  Given el usuario está en la pantalla para carga de pedidos a bodegas
  And el proceso de pedido desde el almacén central está habilitado


@paso_1 @modulo_carga_pedidos @tipo_seleccion
Scenario: 1 Selección de bodega de origen
  When el usuario selecciona el apartado "Bodegas de origen"
  And selecciona "Bodega 2"
  Then la bodega de origen es seleccionada correctamente

@paso_2 @modulo_carga_pedidos @tipo_ingreso_datos
Scenario: 2 Ingreso de RUT
  When el usuario completa el campo RUT con "123456789"
  Then el RUT es ingresado correctamente

@paso_3 @modulo_carga_pedidos @tipo_seleccion
Scenario: 3 Selección de destino
  When el usuario selecciona el destino "Ubicación 1" en el dropdown
  Then el destino es seleccionado correctamente

@paso_4 @modulo_carga_pedidos @tipo_ingreso_datos
Scenario: 4 Ingreso de número de pedido
  When el usuario completa el campo número de pedido con "987"
  Then el número de pedido es ingresado correctamente

@paso_5 @modulo_carga_pedidos @tipo_accion
Scenario: 5 Grabación del pedido
  When el usuario hace clic en el botón "Grabar pedidos"
  Then el pedido se completa
  And el pedido queda persistido en la base de datos


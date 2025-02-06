Feature: Carga de pedidos a bodegas

Background:
  Given el usuario está en la pantalla para cargar pedidos a bodegas
  And el sistema permite realizar pedidos desde el almacén central a distintas bodegas


@paso_1 @modulo_carga_pedidos @tipo_seleccion
Scenario: 1 Selección de bodega origen
  When el usuario selecciona el apartado "Bodega origen" y elige "Bodega 2"
  Then la bodega origen es seleccionada correctamente

@paso_2 @modulo_carga_pedidos @tipo_ingreso_datos
Scenario: 2 Ingreso de RUT
  When el usuario completa el campo "RUT" con "123456789"
  Then el RUT es ingresado correctamente

@paso_3 @modulo_carga_pedidos @tipo_seleccion
Scenario: 3 Selección de destino
  When el usuario selecciona el apartado "Destino" y elige "ubicación número 1"
  Then el destino es seleccionado correctamente

@paso_4 @modulo_carga_pedidos @tipo_ingreso_datos
Scenario: 4 Ingreso de número de pedido
  When el usuario completa el campo "número de pedido" con "987"
  Then el número de pedido es ingresado correctamente

@paso_5 @modulo_carga_pedidos @tipo_accion
Scenario: 5 Grabación del pedido
  When el usuario hace clic en el botón "grabar pedidos"
  Then el pedido se completa
  And el pedido queda guardado en la base de datos


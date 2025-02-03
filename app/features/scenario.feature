Feature: Proceso de carga de pedidos a bodegas

Background:
  Given el usuario está en la pantalla de carga de pedidos
  And tiene acceso a todas las opciones necesarias
  And los parámetros iniciales están configurados


@paso_1 @modulo_carga_pedidos @tipo_seleccion
Scenario: 1 Selección de bodega origen
  When el usuario selecciona la bodega origen del despacho
  Then la bodega 2 es seleccionada correctamente

@paso_2 @modulo_carga_pedidos @tipo_ingreso
Scenario: 2 Ingreso de RUT
  When el usuario ingresa el RUT correspondiente al pedido
  Then el RUT 123456789 es ingresado correctamente

@paso_3 @modulo_carga_pedidos @tipo_seleccion
Scenario: 3 Selección de destino
  When el usuario selecciona el destino en el dropdown
  Then la ubicación número 1 es seleccionada correctamente

@paso_4 @modulo_carga_pedidos @tipo_ingreso
Scenario: 4 Ingreso de número de pedido
  When el usuario ingresa el número de pedido en el campo correspondiente
  Then el número de pedido 987 es ingresado correctamente

@paso_5 @modulo_carga_pedidos @tipo_confirmacion
Scenario: 5 Confirmación de grabación de pedido
  When el usuario hace clic en el botón grabar pedidos
  Then el pedido es grabado y el proceso queda completado


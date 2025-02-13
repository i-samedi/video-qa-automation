Feature: Carga de pedidos a bodegas

Background:
  Given el proceso se inicia desde el almacén central para realizar un pedido a una bodega
  And la información del pedido se guarda en la base de datos


@paso_1 @modulo_carga_pedidos @tipo_interaccion
Scenario: 1 Interacción inicial con la pantalla de carga de pedidos
  When el usuario interactúa con la pantalla de carga de pedidos
  Then la pantalla de carga de pedidos está lista para recibir datos

@paso_2 @modulo_carga_pedidos @tipo_seleccion
Scenario: 2 Selección de bodega de origen
  When el usuario selecciona apartado "Bodegas de origen" y selecciona "Bodega 2"
  Then la bodega de origen "Bodega 2" es seleccionada correctamente

@paso_3 @modulo_carga_pedidos @tipo_completado
Scenario: 3 Completar campo RUT
  When el usuario completa el campo RUT con "123456789"
  Then el campo RUT es completado correctamente con "123456789"

@paso_4 @modulo_carga_pedidos @tipo_seleccion
Scenario: 4 Selección de destino
  When el usuario selecciona apartado "Destino" y selecciona "Ubicación número 1"
  Then la ubicación de destino "Ubicación número 1" es seleccionada correctamente

@paso_5 @modulo_carga_pedidos @tipo_completado
Scenario: 5 Completar campo número de pedido
  When el usuario completa el campo "Número de pedido" con "987"
  Then el campo "Número de pedido" es completado correctamente con "987"

@paso_6 @modulo_carga_pedidos @tipo_accion
Scenario: 6 Grabar el pedido
  When el usuario hace clic en el botón "Grabar pedidos"
  Then el sistema guarda el pedido correctamente

@paso_7 @modulo_carga_pedidos @tipo_finalizacion
Scenario: 7 Finalización del proceso de carga
  When el proceso de carga se completa
  Then el proceso de carga de pedidos a bodegas se completa exitosamente


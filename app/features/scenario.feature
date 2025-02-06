Feature: Carga de pedidos a bodegas

Background:
  Given el usuario está en la pantalla de carga de pedidos a bodegas
  And existe un pedido realizado desde el almacén central


@paso_1 @modulo_carga_pedidos @tipo_seleccion
Scenario: 1 Selección de bodega de origen
  When el usuario selecciona el apartado "Bodegas de origen"
  And selecciona "Bodega 2"
  Then la bodega de origen es seleccionada correctamente

@paso_2 @modulo_carga_pedidos @tipo_completado
Scenario: 2 Completar campo RUT
  When el usuario completa el campo RUT con "123456789"
  Then el campo RUT es completado correctamente

@paso_3 @modulo_carga_pedidos @tipo_seleccion
Scenario: 3 Selección de ubicación de destino
  When el usuario selecciona "Ubicación 1" en el dropdown de destino
  Then la ubicación de destino es seleccionada correctamente

@paso_4 @modulo_carga_pedidos @tipo_completado
Scenario: 4 Completar campo número de pedido
  When el usuario completa el campo número de pedido con "987"
  Then el campo número de pedido es completado correctamente

@paso_5 @modulo_carga_pedidos @tipo_accion
Scenario: 5 Grabar pedido
  When el usuario hace clic en el botón "Grabar pedidos"
  Then el pedido se persiste en la base de datos
  And el proceso de carga se completa exitosamente


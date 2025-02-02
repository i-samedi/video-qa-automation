Feature: Proceso de carga de pedidos a bodegas

Background:
  Given El usuario ha iniciado sesión en el sistema
  And Se encuentra en la pantalla de carga de pedidos


@paso_1 @modulo_seleccion @tipo_entrada
Scenario: 1. Selección de la bodega origen del despacho
  When El usuario selecciona la "Bodega 2" como bodega origen del despacho
  Then La "Bodega 2" queda seleccionada como origen

@paso_2 @modulo_entrada_datos @tipo_entrada
Scenario: 2. Completar el RUT del pedido
  When El usuario completa el campo RUT con "1, 2, 3, 4, 5, 6, 7, 8, 9"
  Then El RUT "1, 2, 3, 4, 5, 6, 7, 8, 9" queda registrado en el campo correspondiente

@paso_3 @modulo_seleccion @tipo_entrada
Scenario: 3. Selección del destino del pedido
  When El usuario selecciona la "Ubicación número 1" como destino del pedido
  Then La "Ubicación número 1" queda seleccionada como destino

@paso_4 @modulo_entrada_datos @tipo_entrada
Scenario: 4. Completar el número de pedido
  When El usuario completa el campo número de pedido con "9, 8, 7"
  Then El número de pedido "9, 8, 7" queda registrado en el campo correspondiente

@paso_5 @modulo_confirmacion @tipo_accion
Scenario: 5. Confirmación y grabación del pedido
  When El usuario hace clic en el botón "Grabar pedidos"
  Then El pedido queda grabado y persistido en la base de datos


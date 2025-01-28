Scenario: Selección de bodega para el despacho de mercadería
    Given que el usuario está en la pantalla de creación de pedidos
    And el tipo de pedido normal está seleccionado por defecto
    When el usuario despliega el combo de origen del despacho
    And selecciona una bodega diferente a la predeterminada
    Then la bodega seleccionada debe reflejarse como el origen del despacho
    And el sistema debe permitir continuar con el proceso de pedido sin problemas
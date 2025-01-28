Scenario: Realización de un pedido con validación de crédito y selección de destino

    Given que la aplicación está abierta en la pantalla de creación de pedidos
    And el usuario tiene suficiente crédito para realizar el pedido
    When el usuario selecciona la sucursal de destino desde el menú desplegable
    And carga los datos desde una plantilla
    And selecciona una condición de venta y presiona Enter
    And digita la orden de compra del cliente y presiona Enter
    Then la aplicación debe confirmar la selección de la sucursal de destino
    And debe registrar la orden de compra del cliente exitosamente.
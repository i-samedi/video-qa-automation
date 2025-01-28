Scenario: Validación de carga masiva y exportación de resultados

    Given que la aplicación de carga masiva está abierta
    And los datos han sido inyectados correctamente
    When el usuario selecciona la opción para generar un respaldo del tipo DBF
    And activa la opción de exportar los datos
    Then la aplicación debe mostrar un respaldo con el detalle de los números de pedido generados
    And el usuario puede cerrar la aplicación sin problemas, validando que la carga fue satisfactoria
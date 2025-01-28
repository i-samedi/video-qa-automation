Feature: Operación de la aplicación de carga masiva

Scenario: Selección de bodega y cliente
Given el usuario está en la pantalla principal de la aplicación
When selecciona la bodega por defecto
And ingresa el RUT del cliente
Then el sistema muestra la razón social del cliente

Scenario: Búsqueda de cliente por razón social
Given el usuario no conoce el RUT del cliente
When presiona el botón de búsqueda
And ingresa parte de la razón social del cliente
Then el sistema muestra una lista de clientes coincidentes
And el usuario selecciona el cliente deseado

Scenario: Validación de crédito y selección de sucursal
Given el usuario ha seleccionado un cliente
When el sistema verifica el crédito disponible
Then el usuario selecciona la sucursal de destino

Scenario: Ingreso de condiciones de venta y orden de compra
Given el usuario ha seleccionado la sucursal de destino
When ingresa las condiciones de venta
And ingresa la orden de compra del cliente
Then el sistema permite el ingreso del porcentaje de descuento

Scenario: Carga y validación de archivo CSV
Given el usuario ha ingresado el porcentaje de descuento
When selecciona el archivo CSV para cargar
Then el sistema valida los registros del archivo
And muestra los datos validados en la pantalla

Scenario: Generación de pedidos
Given los datos del archivo han sido validados
When el usuario presiona el botón de grabar pedidos
Then el sistema genera números de pedido
And muestra los números de pedido generados

Scenario: Exportación de datos de inyección
Given los pedidos han sido generados
When el usuario exporta los datos de inyección
Then el sistema guarda un archivo de respaldo
And el usuario puede cerrar la aplicación


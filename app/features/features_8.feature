Scenario: Generación de números de pedido según género en aplicación de carga masiva
   Given que la aplicación de carga masiva está abierta
   And hay datos de vestuario disponibles con diferentes géneros
   When el usuario procesa los datos para generar pedidos
   And los datos incluyen prendas de hombre y de mujer
   Then la aplicación debe generar un número de pedido para las prendas de hombre
   And debe generar un pedido distinto para las prendas de mujer, aunque sean de la misma marca y clase de vestuario
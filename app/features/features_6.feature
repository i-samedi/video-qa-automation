Scenario: Validación y recuperación de datos al cargar archivo de registros
  Given que el usuario ha cargado un archivo de registros en la aplicación
  And el archivo contiene códigos de tienda, modelo, color, talla y cantidad de pedido
  When el sistema valida cada registro del archivo
  And recupera datos faltantes como nombre del modelo, color, SKU y precio desde el maestro de productos
  Then los datos validados deben coincidir con los campos obligatorios resaltados en el archivo
  And las líneas con errores deben marcarse en rojo, impidiendo la generación de pedidos para esas líneas
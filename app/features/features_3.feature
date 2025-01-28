Scenario: Búsqueda y selección de cliente por razón social y actualización de datos en pantalla
   Given que la aplicación está abierta en la pantalla de despacho
   And el cursor está posicionado en el campo de RUT
   When el usuario presiona el botón con el signo de interrogación para buscar un cliente
   And el usuario digita "Falcao" como parte de la razón social del cliente
   And presiona Enter
   Then la aplicación debe mostrar una lista de clientes que concuerden con el patrón "Falcao"
   And el usuario selecciona el cliente adecuado con un doble clic
   And el RUT y la razón social del cliente seleccionado deben aparecer en la pantalla principal
   And el usuario presiona Enter para confirmar la selección
Scenario: Navegación a la pantalla principal de la aplicación
   Given que el usuario ha iniciado sesión exitosamente en la aplicación
   And está viendo la página de inicio
   When el usuario hace clic en el botón "Pendientes" en el menú principal
   And espera a que la pantalla se actualice
   Then la aplicación debe mostrar la pantalla de "Pendientes"
   And el usuario debe ver una lista de tareas pendientes en la pantalla
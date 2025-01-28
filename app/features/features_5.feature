
    Scenario: Aplicación de descuento y carga de archivo CSV
        Given que la aplicación permite la edición de campos
        And el usuario está viendo el campo del porcentaje de descuento
        When el usuario ingresa un 15 por ciento en el campo correspondiente
        And presiona Enter
        Then la aplicación debe posicionarse en el botón para la lectura del archivo
        And el usuario selecciona el archivo de tipo CSV
        And realiza doble clic para cargar el archivo
        Then la aplicación debe cargar el archivo correctamente
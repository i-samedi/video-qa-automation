# El proceso del sistema sigue una serie de pasos bien definidos

## a) Carga y análisis del video

- El usuario sube un video a la interfaz.
- El sistema muestra el video y extrae información básica como el nombre, tamaño y tipo de archivo.

## b) Extracción y procesamiento de la transcripción 

- Se extrae el audio y se genera una transcripción.
- La transcripción se procesa aplicando glosario técnico y se transforma en casos de prueba escritos en formato Gherkin.

## c) Generación de escenarios y definiciones de pasos

- Los escenarios de prueba definidos en formato Gherkin son interpretados para generar código de definiciones de pasos automáticamente.
- Esto permite verificar el correcto funcionamiento de la aplicación (por ejemplo, que al seleccionar "Bodega 2" se confirme la selección y que se completen correctamente los campos de RUT y número de pedido).

## d) Ejecución y verificación

- Los archivos generados se integran con Playwright para ejecutar pruebas en la interfaz de usuario.
- Se implementa un sistema robusto de manejo de errores, donde se guardan logs, capturas de pantalla y el estado completo de la aplicación en casos de fallos.

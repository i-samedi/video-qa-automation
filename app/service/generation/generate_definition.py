import os
import re
import logging
from openai import OpenAI

# Configuración del logger para trazabilidad
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def clean_code(code: str) -> str:
    """
    Limpia el código generado eliminando formato markdown y espacios o líneas innecesarias.

    Args:
        code (str): Código en formato Markdown o con formato extra.

    Returns:
        str: Código limpio y formateado.
    """
    # Eliminar bloques de formato markdown (```python ... ```)
    code = re.sub(r'```python\s*', '', code)
    code = re.sub(r'```\s*', '', code)
    
    # Eliminar espacios finales y líneas vacías innecesarias
    lines = [line.rstrip() for line in code.splitlines() if line.strip()]
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if line.strip():
            cleaned_lines.append(line)
            prev_empty = False
        elif not prev_empty:
            cleaned_lines.append(line)
            prev_empty = True
    return "\n".join(cleaned_lines)

def create_step_definitions(feature_content: str) -> str:
    """
    Genera el código de definiciones de pasos en formato Behave a partir del contenido
    del archivo .feature, utilizando GPT-4.

    Cada definición de paso se generará con decoradores (@given, @when, @then) y
    se asignarán nombres descriptivos a los métodos basados en el contenido del paso.

    Args:
        feature_content (str): Contenido completo del archivo .feature.

    Returns:
        str: Código Python con las definiciones de pasos para Behave.
    """
    client = OpenAI()
    
    prompt = f"""
Lee el siguiente archivo .feature y genera las definiciones de pasos utilizando Behave.
Cada definición de paso debe tener un nombre descriptivo basado en el contenido del paso.
Utiliza los decoradores @given, @when y @then, y asigna nombres de métodos significativos.
El código debe estar en formato Python, sin explicaciones adicionales y con un espaciado adecuado para su legibilidad.

FEATURE:
{feature_content}
    """
    
    try:
        logger.info("Generando definiciones de pasos utilizando GPT-4...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un generador de código Python que produce definiciones de pasos para Behave de forma profesional."
                },
                {"role": "user", "content": prompt}
            ]
        )
        code = response.choices[0].message.content
    except Exception as e:
        logger.exception("Error al generar las definiciones de pasos.")
        raise RuntimeError("Error al generar las definiciones de pasos utilizando GPT-4.") from e
    
    cleaned_code = clean_code(code)
    logger.info("Definiciones de pasos generadas correctamente.")
    return cleaned_code

def generate_step_definitions(feature_file: str) -> int:
    """
    Lee el archivo .feature, genera las definiciones de pasos correspondientes y
    guarda el resultado en un archivo Python dentro del directorio 'features/steps'.

    Args:
        feature_file (str): Ruta del archivo .feature.

    Returns:
        int: Retorna 1 si la generación del archivo fue exitosa.
    """
    # Crear el directorio 'features/steps' si no existe
    steps_dir = os.path.join("features", "steps")
    os.makedirs(steps_dir, exist_ok=True)
    
    # Leer el contenido del archivo .feature
    try:
        with open(feature_file, 'r', encoding='utf-8') as f:
            feature_content = f.read()
    except Exception as e:
        logger.exception("Error al leer el archivo .feature: %s", feature_file)
        raise RuntimeError(f"Error al leer el archivo {feature_file}") from e

    # Generar el código de definiciones de pasos
    step_code = create_step_definitions(feature_content)
    
    # Definir el nombre del archivo de pasos basado en el nombre del feature
    feature_name = os.path.splitext(os.path.basename(feature_file))[0]
    step_file = os.path.join(steps_dir, f"{feature_name}_steps.py")
    
    # Guardar el código generado en el archivo de definiciones
    try:
        with open(step_file, 'w', encoding='utf-8') as f:
            f.write(step_code + "\n")
        logger.info("Archivo de definiciones de pasos generado en: %s", step_file)
    except Exception as e:
        logger.exception("Error al escribir el archivo de definiciones de pasos.")
        raise RuntimeError("Error al generar el archivo de definiciones de pasos.") from e

    return 1

if __name__ == '__main__':
    # Archivo .feature con el flujo completo de Proceso de Carga Masiva de Pedidos
    feature_file = "proceso_carga_masiva.feature"
    generate_step_definitions(feature_file)

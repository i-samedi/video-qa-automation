import json
import re
import http.client
import os
import time
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def extract_locators_to_json() -> str:
    """
    Extrae los locators desde la API y los guarda en un archivo JSON.

    Realiza la consulta a la API con reintentos, formatea el resultado mediante GPT-4 y
    guarda el JSON formateado en el directorio correspondiente.

    Returns:
        str: Ruta completa del archivo JSON generado.

    Raises:
        Exception: Si no se puede extraer o parsear la información.
    """
    try:
        max_retries = 3
        retry_count = 0
        data = None

        while retry_count < max_retries:
            try:
                conn = http.client.HTTPSConnection("codacle-graph-service.fly.dev", timeout=30)
                payload = json.dumps({
                    "query": ("MATCH (a:Application {name: 'CargaMasivaPedidos'})-[:has_module|has_class*1..2]->(c:Class) "
                              "RETURN c.locators, c.name")
                })
                headers = {
                    'Content-Type': "application/json",
                    'User-Agent': "insomnia/10.3.0",
                    'x-api-key': "4bca697be480f14731e32a9a8058f7652dbe8ee7cf75580768861ee802b3d370"
                }
                conn.request("POST", "/api/v1/cypher-query", payload, headers)
                res = conn.getresponse()
                data_bytes = res.read()
                conn.close()
                data = json.loads(data_bytes.decode("utf-8"))
                break
            except Exception as exc:
                retry_count += 1
                logger.warning("Intento %s fallido: %s", retry_count, exc)
                if retry_count == max_retries:
                    raise Exception(f"Error después de {max_retries} intentos: {exc}")
                time.sleep(2)

        load_dotenv()
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        prompt = f"""
Extrae y formatea los locators del siguiente resultado de query.
Necesito que extraigas específicamente el contenido de c.locators donde c.name es "TFormPedidoNcr".

Resultado de la query:
{json.dumps(data, indent=2)}

El resultado debe ser un JSON válido con la estructura jerárquica de los locators.
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un experto en procesamiento de JSON. Extrae y formatea los locators manteniendo su estructura exacta."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        locators_str = response.choices[0].message.content
        # Eliminar delimitadores markdown
        locators_str = re.sub(r'```json\s*', '', locators_str)
        locators_str = re.sub(r'```\s*', '', locators_str)

        try:
            locators_json = json.loads(locators_str)
        except json.JSONDecodeError as exc:
            logger.error("Error al parsear locators: %s", exc)
            logger.error("String problemático: %s", locators_str)
            raise

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        locators_dir = os.path.join(base_dir, "app", "features", "locators")
        os.makedirs(locators_dir, exist_ok=True)
        locators_file = os.path.join(locators_dir, "page_locators.json")
        with open(locators_file, 'w', encoding='utf-8') as f:
            json.dump(locators_json, f, indent=4, ensure_ascii=False)

        logger.info("Locators extraídos y guardados en: %s", locators_file)
        return locators_file

    except Exception as e:
        logger.exception("Error al extraer locators")
        if 'data' in locals() and data is not None:
            logger.error("Respuesta de la API: %s", json.dumps(data, indent=2))
        raise


def generate_playwright_steps_with_gpt4(steps_content: str, locators_file: str) -> str:
    """
    Genera código Playwright para los steps de Behave utilizando GPT-4o.

    El código generado usará solo los locators disponibles en el JSON proporcionado y
    seguirá una estructura que incluya:
      - Esperas explícitas con page.wait_for_selector.
      - Validaciones con expect.
      - Manejo especial de listas desplegables (Dropdown lists) usando select_option.
      - En el primer step definido con @given se incluirá una única llamada a page.goto("https://example.com")
        para ingresar a la página.
      - NO se deben repetir llamadas a page.goto en steps posteriores.

    Args:
        steps_content (str): Código de steps de Behave (definiciones de pasos).
        locators_file (str): Ruta al archivo JSON de locators.

    Returns:
        str: Código Python con los steps implementados en Playwright.
    """
    with open(locators_file, 'r', encoding='utf-8') as f:
        locators = json.load(f)

    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"""
Genera código Playwright para los steps de Behave siguiendo estas reglas:
1. SOLO usa los locators que existen en el JSON proporcionado, NO inventes nuevos.
2. Cada selector debe existir exactamente en el archivo de locators.
3. Usa la estructura jerárquica correcta para acceder a los locators (ej: LOCATORS['groupBox1']['selects']['bodega']).
4. Incluye esperas explícitas con page.wait_for_selector antes de cada interacción.
5. Agrega validaciones con expect después de cada acción.
6. Usa context.page para acceder a la página.
7. Maneja errores con try/except.
8. Identifica y maneja las listas desplegables (Dropdown lists) usando select_option.
9. En el primer step definido con @given, incluye una única llamada a page.goto("http://localhost:3000") para ingresar a la página; NO repitas page.goto en pasos adicionales.
10. NO agregues comentarios ni imports, utiliza los existentes.
Los locators disponibles son:
{json.dumps(locators, indent=2)}

Steps a implementar:
{steps_content}

IMPORTANTE:
- NO inventes selectores o IDs que no existan en el JSON.
- Usa la estructura exacta de los locators proporcionados.
- Si un locator no existe para una acción específica, maneja el caso apropiadamente.
- Mantén los nombres de funciones y decoradores exactos.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un experto en automatización con Playwright. Genera código usando SOLO los locators proporcionados, sin inventar nuevos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4000
    )
    code = response.choices[0].message.content
    # Limpiar delimitadores markdown y comentarios
    code = re.sub(r'```python\s*', '', code)
    code = re.sub(r'```\s*', '', code)
    code = re.sub(r'^#.*$', '', code, flags=re.MULTILINE)
    code = '\n'.join(line for line in code.split('\n') if line.strip())
    # Eliminar declaraciones de importación para evitar duplicados
    code = re.sub(r'^\s*(import|from)\s+.*$', '', code, flags=re.MULTILINE)
    code = '\n'.join(line for line in code.split('\n') if line.strip())

    # Validar que se usen solo locators existentes
    used_locators = re.findall(r"LOCATORS\['([^']+)'\]\['([^']+)'\](?:\['([^']+)'\])?", code)
    for loc in used_locators:
        path = list(filter(None, loc))
        current = locators
        try:
            for key in path:
                current = current[key]
        except KeyError:
            logger.warning("Locator no existente usado: %s", '.'.join(path))

    return code


def update_steps_file() -> str:
    """
    Actualiza el archivo de steps (scenario_steps.py) generando un archivo nuevo con el código Playwright.

    El proceso es:
      1. Extraer los locators y guardarlos en JSON.
      2. Leer el archivo de steps original.
      3. Generar código Playwright usando GPT-4.
      4. Respaldar (renombrar) el archivo original para evitar pasos duplicados.
      5. Prependé la configuración necesaria (imports, carga de locators, timeout).
      6. Guardar el archivo final en el directorio 'features/steps'.

    Returns:
        str: Ruta completa del archivo de steps generado.

    Raises:
        FileNotFoundError: Si no se encuentra el archivo de steps original.
        Exception: Para otros errores durante el proceso.
    """
    try:
        locators_file = extract_locators_to_json()
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        steps_dir = os.path.join(base_dir, "app", "features", "steps")
        os.makedirs(steps_dir, exist_ok=True)
        input_file = os.path.join(steps_dir, "scenario_steps.py")
        output_file = os.path.join(steps_dir, "scenario_steps_playwright.py")
        

        # Si existe el archivo original, respaldarlo para evitar duplicidad de pasos
        if os.path.exists(input_file):
            backup_file = os.path.join(steps_dir, "scenario_steps_original.py")
            os.rename(input_file, backup_file)
            logger.info("Archivo original respaldado como: %s", backup_file)
        else:
            raise FileNotFoundError(f"No se encontró el archivo de steps en: {input_file}")
        
        
        
        with open(os.path.join(steps_dir, "scenario_steps_original.py"), 'r', encoding='utf-8') as f:
            original_content = f.read()
        playwright_code = generate_playwright_steps_with_gpt4(original_content, locators_file)
        final_content = (
            "from behave import given, when, then\n"
            "from playwright.sync_api import expect, TimeoutError\n"
            "import os\n"
            "import json\n\n"
            "TIMEOUT = 5000  # 5 segundos\n\n"
            "with open(os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json'), 'r') as f:\n"
            "    LOCATORS = json.load(f)\n\n"
            f"{playwright_code}\n"
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        logger.info("Archivo de steps actualizado en: %s", output_file)
        
        #necesito eliminar el archivo scenario_steps_original
        os.remove(os.path.join(steps_dir, "scenario_steps_original.py"))
        
        return output_file


    except Exception as exc:
        logger.exception("Error en update_steps_file: %s", exc)
        raise


if __name__ == "__main__":
    try:
        logger.info("Iniciando actualización de steps...")
        output_path = update_steps_file()
        logger.info("Proceso completado exitosamente. Archivo generado: %s", output_path)
    except Exception as err:
        logger.error("Error inesperado al actualizar los steps: %s", err)

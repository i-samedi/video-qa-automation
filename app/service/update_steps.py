import json
import re
import http.client
import os
import time
import logging
from openai import OpenAI
from dotenv import load_dotenv

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
                    'x-api-key': os.getenv('X_API_KEY')
                }
                conn.request("POST", "/api/v1/cypher-query", payload, headers)
                res = conn.getresponse()
                data_bytes = res.read()
                conn.close()
                data = json.loads(data_bytes.decode("utf-8"))
                
                # --- NUEVO: Filtrar solo los resultados donde "c.locators" no sea NULL ---
                valid_results = [row for row in data.get("results", []) if row.get("c.locators") is not None]
                if not valid_results:
                    raise Exception("No se encontraron locators no nulos en la respuesta de la API")
                
                load_dotenv()
                client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                prompt = f"""
Extrae y formatea los locators del siguiente resultado de query.
Debes extraer en JSON únicamente los c.locators que no sean NULL.
Utiliza solamente aquellos resultados que tengan datos, por ejemplo, cuando c.name es "TFormPedidoNcr".

Resultados de la query filtrados:
{json.dumps(valid_results, indent=2)}

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
                locators_str = re.sub(r'```(?:json)?\s*', '', locators_str)
                locators_str = re.sub(r'\s*```', '', locators_str)

                try:
                    locators_json = json.loads(locators_str)
                except json.JSONDecodeError as exc:
                    logger.error("Error al parsear locators: %s", exc)
                    logger.error("String problemático: %s", locators_str)
                    raise

                # Se determina la ruta base (3 niveles arriba de este archivo)
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                # Se define la carpeta donde se guardarán los locators: app/features/locators
                locators_dir = os.path.join(base_dir, "app", "features", "locators")
                os.makedirs(locators_dir, exist_ok=True)
                locators_file = os.path.join(locators_dir, "page_locators.json")
                
                # Se guarda el JSON de locators en la carpeta locators
                with open(locators_file, 'w', encoding='utf-8') as f:
                    json.dump(locators_json, f, indent=4, ensure_ascii=False)

                logger.info("Locators extraídos y guardados en: %s", locators_file)
                return locators_file

            except Exception as exc:
                retry_count += 1
                logger.warning("Intento %s fallido: %s", retry_count, exc)
                if retry_count == max_retries:
                    raise Exception(f"Error después de {max_retries} intentos: {exc}")
                time.sleep(2)

    except Exception as e:
        logger.exception("Error al extraer locators")
        if 'data' in locals() and data is not None:
            logger.error("Respuesta de la API: %s", json.dumps(data, indent=2))
        raise


def generate_playwright_steps_with_gpt4(steps_content: str, locators_file: str) -> str:
    """
    Genera código Playwright para los steps de Behave utilizando GPT-4o.

    Se deben emplear ejemplos que muestren el manejo de componentes individuales
    como inputs, clicks, dropdowns/selects, validaciones y la implementación correcta de los given iniciales.

    Ejemplos:
    - Input:
      ---------------------------------------------------------------------------
      @when('el usuario ingresa el RUT correspondiente')
      def step_ingreso_rut(context):
          try:
              context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
          except Exception as e:
              raise Exception(f"Error al ingresar el RUT: {{e}}")
      ---------------------------------------------------------------------------
    - Click / Botón:
      ---------------------------------------------------------------------------
      @when('el usuario hace clic en el botón grabar pedidos')
      def step_click_grabar(context):
          try:
              boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
              expect(boton).to_be_visible(timeout=TIMEOUT)
              try:
                  expect(boton).to_be_enabled(timeout=TIMEOUT)
                  boton.click()
              except Exception as e:
                  boton.click(force=True)
          except Exception as e:
              raise Exception(f"Error al hacer clic en el botón: {{str(e)}}")
      ---------------------------------------------------------------------------
    - Dropdown / Select:
      ---------------------------------------------------------------------------
      @when('el usuario selecciona la opción en el dropdown')
      def step_seleccion_dropdown(context):
          try:
              combo = context.page.locator("#groupbox1 button[role='combobox']")
              expect(combo).to_be_visible(timeout=TIMEOUT)
              expect(combo).to_be_enabled(timeout=TIMEOUT)
              combo.click()
              opcion = context.page.locator('[role="option"]', has_text="Opción 1")
              expect(opcion).to_be_visible(timeout=TIMEOUT)
              opcion.click()
          except Exception as e:
              raise Exception(f"Error al seleccionar en el dropdown: {{str(e)}}")
      ---------------------------------------------------------------------------
    - Validación:
      ---------------------------------------------------------------------------
      @then('el valor esperado se muestra en el campo')
      def step_validacion_input(context):
          expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
      ---------------------------------------------------------------------------

    Además, se debe generar el código completo como un profesional en Playwright, implementando correctamente
    el given inicial (por ejemplo, el acceso a la página) y utilizando los locators extraídos de la query.

    Los locators disponibles son:
    {json.dumps(json.load(open(locators_file, 'r', encoding='utf-8')), indent=2)}

    Steps a implementar:
    {steps_content}

    IMPORTANTE:
    - No inventes selectores o IDs que no existan en el JSON.
    - Usa siempre la estructura exacta de los locators proporcionados.
    - Maneja errores y excepciones como se muestra en los ejemplos.
    - No crees nuevos TIMEOUT, solo debes usar el TIMEOUT que ya existe. No generes un TIMEOUT= valor.
    """
    with open(locators_file, 'r', encoding='utf-8') as f:
        locators = json.load(f)

    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""
Genera código Playwright para los steps de Behave siguiendo estas reglas:
1. Utiliza los siguientes ejemplos modulares para cada componente:

Ejemplo para un input:
-----------------------------------------------------------
@when('el usuario ingresa el RUT correspondiente')
def step_ingreso_rut(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
    except Exception as e:
        raise Exception(f"Error al ingresar el RUT: {{e}}")
-----------------------------------------------------------

Ejemplo para un click / botón:
-----------------------------------------------------------
@when('el usuario hace clic en el botón grabar pedidos')
def step_click_grabar(context):
    try:
        boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
        expect(boton).to_be_visible(timeout=TIMEOUT)
        try:
            expect(boton).to_be_enabled(timeout=TIMEOUT)
            boton.click()
        except Exception as e:
            boton.click(force=True)
    except Exception as e:
        raise Exception(f"Error al hacer clic en el botón: {{str(e)}}")
-----------------------------------------------------------

Ejemplo para un dropdown / select:
-----------------------------------------------------------
@when('el usuario selecciona la opción en el dropdown')
def step_seleccion_dropdown(context):
    try:
        combo = context.page.locator("#groupbox1 button[role='combobox']")
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        combo.click()
        opcion = context.page.locator('[role="option"]', has_text="Opción 1")
        expect(opcion).to_be_visible(timeout=TIMEOUT)
        opcion.click()
    except Exception as e:
        raise Exception(f"Error al seleccionar en el dropdown: {{str(e)}}")
-----------------------------------------------------------

{{ Nuevo: Ejemplo para un checkbox }}
-----------------------------------------------------------
@when('el usuario marca el checkbox de aceptar términos')
def step_checkbox_aceptar(context):
    try:
        checkbox = context.page.locator(LOCATORS['groupBox1']['checkboxes']['aceptarTerminos'])
        expect(checkbox).to_be_visible(timeout=TIMEOUT)
        if not checkbox.is_checked():
            checkbox.check()
    except Exception as e:
        raise Exception(f"Error al marcar el checkbox: {{str(e)}}")
-----------------------------------------------------------

Ejemplo para una validación:
-----------------------------------------------------------
@then('el valor esperado se muestra en el campo')
def step_validacion_input(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
-----------------------------------------------------------

Genera código Playwright completo y profesional utilizando los locators extraídos (guardados en formato JSON) para su utilización, y aplicando estos ejemplos en la generación de los steps.

RECUERDA:
- No generes comentarios o texto que afecten el funcionamiento del código.
- No generes comentarios que no sean necesarios y que no afecten el funcionamiento del código.

Los locators disponibles son:
{json.dumps(locators, indent=2)}

Steps a implementar:
{steps_content}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un profesional en automatización con Playwright. Genera código para steps de Behave utilizando solo los locators proporcionados, siguiendo los ejemplos para given, inputs, clicks, dropdowns, checkboxes y validaciones."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=4000
    )
    code = response.choices[0].message.content
    # Limpiar delimitadores markdown y comentarios innecesarios
    code = re.sub(r'```(?:python)?\s*', '', code)
    code = re.sub(r'\s*```', '', code)
    code = re.sub(r'^#.*$', '', code, flags=re.MULTILINE)
    code = '\n'.join(line for line in code.split('\n') if line.strip())
    # Eliminar declaraciones de importación para evitar duplicados
    code = re.sub(r'^\s*(import|from)\s+.*$', '', code, flags=re.MULTILINE)
    code = '\n'.join(line for line in code.split('\n') if line.strip())
    
    # --- NUEVO: Eliminar texto adicional que pueda afectar el funcionamiento ---
    if "This code implements" in code:
        code = code.split("This code implements")[0].strip()
    # -------------------------------------------------------------------------

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
        7. NO genere comentarios que no sean necesarios y que no afecten el funcionamiento del código.
        8. No generes comentarios o texto que afecten el funcionamiento del código.
   
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
        
        # Respaldar el archivo original si existe
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
            "TIMEOUT = 15000\n\n"
            "LOCATORS_PATH = os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json')\n"
            "with open(LOCATORS_PATH, 'r') as f:\n"
            "    LOCATORS = json.load(f)\n\n"
            f"{playwright_code}\n"
        )
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        logger.info("Archivo de steps actualizado en: %s", output_file)
        
        # Eliminar el archivo original respaldado para evitar duplicados
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
import http.client
import json
import os
import time
import logging
from openai import OpenAI
from dotenv import load_dotenv
import re

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
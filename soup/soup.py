import sys
import json
import os
import requests
import openai
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def extract_locators(html_content):
    """
    Extrae locators de un contenido HTML utilizando BeautifulSoup.
    
    Se buscan elementos con atributo 'id' y se agrupan en:
      - "page": extrae el título (primer <h1> encontrado) formateado como 'h1:text("...")'
      - "inputs": inputs comunes (inputs de type distinto de checkbox o radio)
      - "selects": elementos <select>
      - "textareas": elementos <textarea>
      - "buttons": elementos <button>
      - "checkboxes": inputs de type "checkbox"
      - "radioButtons": inputs de type "radio"
      
    Retorna un diccionario con la estructura de locators.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    locators = {}
    
    # Extraer título principal (si existe) y guardarlo en la clave "page"
    title_tag = soup.find("h1")
    if title_tag:
        title_text = title_tag.get_text(strip=True)
        locators["page"] = {
            "title": f'h1:text("{title_text}")'
        }
    
    # Inicializar diccionarios para cada grupo
    groups = {
        "inputs": {},
        "selects": {},
        "textareas": {},
        "buttons": {},
        "checkboxes": {},
        "radioButtons": {}
    }
    
    # Procesar los inputs y clasificarlos según el atributo type
    for input_tag in soup.find_all("input", id=True):
        input_type = input_tag.get("type", "text").lower()  # por defecto es text.
        tag_id = input_tag["id"]
        selector = f"#{tag_id}"
        if input_type == "checkbox":
            groups["checkboxes"][tag_id] = selector
        elif input_type == "radio":
            groups["radioButtons"][tag_id] = selector
        else:
            groups["inputs"][tag_id] = selector

    # Procesar los selects
    for select_tag in soup.find_all("select", id=True):
        tag_id = select_tag["id"]
        groups["selects"][tag_id] = f"#{tag_id}"
    
    # Procesar los textareas
    for textarea in soup.find_all("textarea", id=True):
        tag_id = textarea["id"]
        groups["textareas"][tag_id] = f"#{tag_id}"
    
    # Procesar los botones (elemento <button>)
    for button in soup.find_all("button", id=True):
        tag_id = button["id"]
        groups["buttons"][tag_id] = f"#{tag_id}"
    
    # Incluir los grupos si tienen elementos
    for group_name, items in groups.items():
        if items:  # Sólo añade si se encontraron elementos en ese grupo.
            locators[group_name] = items
    
    return locators

def ai_analyze_locators(locators):
    """
    Envía el JSON de locators a la API de OpenAI para obtener un análisis y sugerencias
    de cómo mejorar su estructura.
    """
    prompt = (
        "A continuación se muestra el JSON de locators extraídos de una página web. "
        "Analiza su estructura y ofrece sugerencias para mejorar su organización si es posible.\n\n"
        f"{json.dumps(locators, indent=2)}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error al comunicarse con la API de OpenAI: {e}"

def main():
    # Cargar variables de entorno desde .env
    load_dotenv()

    # Inicializar OpenAI usando la variable de entorno
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        openai.api_key = openai_api_key
    else:
        print("No se encontró OPENAI_API_KEY en las variables de entorno. La funcionalidad de AI no estará disponible.")

    # Manejo de entrada: si no se pasan argumentos, se pide la URL y el nombre del archivo JSON.
    if len(sys.argv) == 1:
        url = "https://www.weplay.cl/"
        output_json = "page_locators.json"
        # Agregar cabecera para simular un navegador real
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            html_content = response.text
        except Exception as e:
            print(f"Error al obtener la URL: {e}")
            sys.exit(1)
    else:
        # Si se pasan argumentos, se evalúa si el primero es una URL o una ruta a archivo HTML.
        if sys.argv[1].startswith("http"):
            url = sys.argv[1]
            # Agregar cabecera para simular un navegador real
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/95.0.4638.69 Safari/537.36"
            }
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                html_content = response.text
            except Exception as e:
                print(f"Error al obtener la URL: {e}")
                sys.exit(1)
        else:
            input_html = sys.argv[1]
            with open(input_html, "r", encoding="utf-8") as f:
                html_content = f.read()
        output_json = sys.argv[2] if len(sys.argv) >= 3 else "page_locators.json"

    # Extraer locators
    locators = extract_locators(html_content)

    # Guardar en archivo JSON con indentación
    with open(output_json, "w", encoding="utf-8") as fo:
        json.dump(locators, fo, indent=4, ensure_ascii=False)
    print(f"Locators extraídos y guardados en {output_json}")

    # Llamar a la función de análisis de inteligencia artificial
    print("Obteniendo análisis de inteligencia artificial...")
    ai_result = ai_analyze_locators(locators)
    print("Respuesta de AI:")
    print(ai_result)

if __name__ == '__main__':
    main()

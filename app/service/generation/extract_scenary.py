from langchain_openai import ChatOpenAI
import os
from typing import List, Dict

def get_gherkin_from_gpt(transcript: str, model: str = "gpt-4o", temperature: float = 0.0, language: str = "es") -> str:
    """
    Convierte la transcripción en escenarios Gherkin secuenciales que forman un flujo completo.

    Args:
        transcript: Texto de la transcripción.
        model: Modelo de GPT a utilizar.
        temperature: Temperatura para la generación (0.0 - 1.0).
        language: Idioma para generar los escenarios ('es' o 'en').

    Returns:
        str: Escenarios secuenciales en formato Gherkin.
    """
    chat = ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    language_prompts = {
        'es': """
Analiza la siguiente transcripción y genera escenarios Gherkin secuenciales.
Divide el flujo principal en pasos atómicos, donde cada paso sea un escenario.
Los escenarios deben estar conectados y seguir un orden lógico.

IMPORTANTE: 
1. Cada escenario debe representar UN SOLO paso atómico del flujo.
2. Los escenarios deben estar numerados y seguir una secuencia lógica.
3. El Background debe tener UN SOLO Given que agrupe todas las condiciones relacionadas a la misma pantalla/contexto:
   - INCORRECTO:
     Given el usuario está en la pantalla de carga
     Given el usuario tiene acceso a las opciones
   - CORRECTO:
     Given el usuario está en la pantalla de carga
     And tiene acceso a las opciones
4. Cada escenario debe tener tags relevantes:
   - @paso_{numero} - Indica el orden del paso.
   - @modulo_<nombre> - Indica el módulo principal.
   - @tipo_<tipo_operacion> - Indica el tipo de operación.
5. Cuando se usen números, NO incluir puntos ni comas entre ellos (ejemplo: usar "123" en lugar de "1,2,3" o "1.2.3")
6. Los steps deben seguir el formato para poder generar automáticamente los step definitions:
   - Background debe tener UN SOLO Given que agrupe el contexto completo
   - Usar And para condiciones adicionales del mismo contexto
   - Los steps de escenarios deben usar 'When' para acciones y 'Then' para validaciones
   - Usar nombres de steps descriptivos y únicos

Formato esperado:
Feature: [Nombre del Feature]

Background:
  Given el usuario está en la pantalla de carga del sistema
  And tiene acceso a todas las opciones necesarias
  And los parámetros iniciales están configurados

@paso_1 @modulo_login @tipo_validacion
Scenario: 1 Inicio del proceso
  When el usuario ingresa los datos requeridos
  Then los datos son validados correctamente

[... y así sucesivamente para cada paso]
        """,
        'en': """
[Similar estructura en inglés...]
        """
    }
    
    rules = {
        'es': """
Sigue estas reglas:
1. Comienza con una línea que indique 'Feature:'.
2. El Background debe tener UN SOLO Given que agrupe todo el contexto de la misma pantalla.
3. Divide el flujo en escenarios atómicos y secuenciales.
4. Cada escenario debe representar UN SOLO paso del flujo.
5. Numera los escenarios en orden secuencial.
6. Usa When para acciones y Then para validaciones.
7. Cada escenario debe incluir los tags: @paso_X, @modulo_<nombre> y @tipo_<tipo_operacion>.
8. Mantén continuidad lógica en el flujo.
9. Los steps deben ser únicos y descriptivos.
10. NUNCA uses múltiples Given para el mismo contexto o pantalla.
        """,
        'en': """
[Similar rules in English...]
        """
    }
    
    prompt = f"""
{language_prompts.get(language, language_prompts['en'])}

{rules.get(language, rules['en'])}

Transcripción: {transcript}
    """
    
    response = chat.invoke(prompt)
    return response.content

def parse_gherkin_scenarios(gherkin_text: str, include_tags: bool = True) -> Dict:
    """
    Parsea el texto Gherkin y separa el Feature, el Background (si existe) y los escenarios individuales.

    Args:
        gherkin_text: Texto completo en formato Gherkin.
        include_tags: Si se deben conservar los tags asociados a cada escenario.

    Returns:
        Dict: Diccionario con las claves 'feature', 'background' y 'scenarios' (lista de escenarios).
    """
    # Limpiar marcadores de código si existen
    gherkin_text = gherkin_text.replace('```gherkin', '').replace('```', '').strip()
    
    lines = gherkin_text.strip().splitlines()
    feature = ""
    background = ""
    scenarios = []
    
    current_block = []  # Para ir acumulando líneas de un bloque (Background o Scenario)
    mode = None         # Puede ser "background" o "scenario"

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith("Feature:"):
            feature = line
            i += 1
            continue

        # Capturar Background (si existe)
        if line.startswith("Background:"):
            mode = "background"
            current_block = [line]
            i += 1
            while i < len(lines):
                next_line = lines[i].rstrip()
                # Finaliza el bloque si se encuentra un tag o un Scenario (comienzo de otro bloque)
                if next_line.startswith("@") or next_line.startswith("Scenario:"):
                    break
                current_block.append(next_line)
                i += 1
            background = "\n".join(current_block)
            continue

        # Capturar cada escenario (incluyendo los tags previos si se desean conservar)
        if line.startswith("@"):
            mode = "scenario"
            current_block = [line]
            i += 1
            # Si se tienen varios tags consecutivos, los acumulamos
            while i < len(lines) and lines[i].lstrip().startswith("@"):
                current_block.append(lines[i].rstrip())
                i += 1
            # La siguiente línea debe ser la cabecera del Scenario
            if i < len(lines) and lines[i].startswith("Scenario:"):
                current_block.append(lines[i].rstrip())
                i += 1
            # Continuar hasta encontrar otro tag o Scenario o el fin del archivo
            while i < len(lines):
                next_line = lines[i].rstrip()
                if next_line.startswith("@") or next_line.startswith("Scenario:") or next_line.startswith("Feature:") or next_line.startswith("Background:"):
                    break
                current_block.append(next_line)
                i += 1
            scenarios.append("\n".join(current_block))
            continue
        
        # En caso de encontrar un Scenario sin tag (rara vez, pero se contempla)
        if line.startswith("Scenario:"):
            mode = "scenario"
            current_block = [line]
            i += 1
            while i < len(lines):
                next_line = lines[i].rstrip()
                if next_line.startswith("@") or next_line.startswith("Scenario:") or next_line.startswith("Feature:") or next_line.startswith("Background:"):
                    break
                current_block.append(next_line)
                i += 1
            scenarios.append("\n".join(current_block))
            continue

        # Si la línea no pertenece a ningún bloque reconocido, avanzar.
        i += 1

    return {
        'feature': feature,
        'background': background,
        'scenarios': scenarios
    }

def generate_feature_file(gherkin_dict: Dict, output_path: str, encoding: str = 'utf-8') -> None:
    """
    Genera un archivo .feature con el contenido completo (Feature, Background y escenarios).

    Args:
        gherkin_dict: Diccionario con 'feature', 'background' y 'scenarios'.
        output_path: Ruta donde se guardará el archivo .feature.
        encoding: Codificación del archivo de salida.
    """
    with open(output_path, 'w', encoding=encoding) as f:
        # Escribir Feature
        if gherkin_dict.get('feature'):
            f.write(gherkin_dict['feature'] + '\n\n')
        # Escribir Background si existe
        if gherkin_dict.get('background'):
            f.write(gherkin_dict['background'] + '\n\n')
        # Escribir cada escenario, separándolos por líneas en blanco
        for scenario in gherkin_dict.get('scenarios', []):
            f.write(scenario.strip() + '\n\n')

def process_transcript_to_scenarios(
    transcript: str, 
    output_path: str, 
    model: str = "gpt-4o",
    temperature: float = 0.0,
    language: str = "es",
    include_tags: bool = True,
    encoding: str = 'utf-8'
) -> None:
    """
    Procesa una transcripción completa y genera un archivo .feature con múltiples escenarios en formato Gherkin profesional.

    Args:
        transcript: Texto de la transcripción.
        output_path: Ruta donde se guardará el archivo .feature.
        model: Modelo de GPT a utilizar.
        temperature: Temperatura para la generación.
        language: Idioma para generar los escenarios.
        include_tags: Si se deben incluir las etiquetas en el parsing.
        encoding: Codificación del archivo de salida.
    """
    gherkin_text = get_gherkin_from_gpt(transcript, model, temperature, language)
    gherkin_dict = parse_gherkin_scenarios(gherkin_text, include_tags)
    generate_feature_file(gherkin_dict, output_path, encoding)

# Ejemplo de uso:
if __name__ == '__main__':
    # Suponiendo que 'transcript' contiene la descripción o flujo de escenarios
    transcript = """
    [Aquí se coloca la transcripción que describe el proceso de carga masiva de pedidos...]
    """
    output_path = "proceso_carga_masiva.feature"
    process_transcript_to_scenarios(transcript, output_path)

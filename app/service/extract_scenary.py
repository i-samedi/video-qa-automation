from langchain_openai import ChatOpenAI
import os
from typing import List, Dict

def get_gherkin_from_gpt(transcript: str) -> str:
    """
    Convierte la transcripción en múltiples escenarios Gherkin usando GPT-4
    Args:
        transcript: Texto de la transcripción
    Returns:
        str: Escenarios en formato Gherkin
    """
    chat = ChatOpenAI(
        model="gpt-4o-2024-08-06",
        temperature=0.0,
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    prompt = f"""
    Analiza la siguiente transcripción y genera múltiples escenarios Gherkin.
    Identifica diferentes flujos o casos de uso en la transcripción.
    Para cada flujo, crea un escenario separado.
    
    Sigue estas reglas:
    1. Comienza con una descripción general en 'Feature:'
    2. Crea múltiples 'Scenario:' según los diferentes flujos identificados
    3. Usa Given, When, Then para cada escenario
    4. Usa And para pasos adicionales cuando sea necesario
    5. Mantén los escenarios concisos y enfocados
    6. No incluyas comentarios explicativos
    7. No uses comillas triples para docstrings
    8. No incluyas marcadores de código como ```python
    
    Transcripción: {transcript}
    """
    
    response = chat.invoke(prompt)
    return response.content

def parse_gherkin_scenarios(gherkin_text: str) -> Dict:
    """
    Parsea el texto Gherkin y separa los diferentes escenarios
    Args:
        gherkin_text: Texto completo en formato Gherkin
    Returns:
        Dict: Diccionario con feature y lista de escenarios
    """
    lines = gherkin_text.strip().split('\n')
    feature = ""
    scenarios = []
    current_scenario = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('Feature:'):
            feature = line
        elif line.startswith('Scenario:'):
            if current_scenario:
                scenarios.append('\n'.join(current_scenario))
            current_scenario = [line]
        elif line and current_scenario:
            current_scenario.append(line)
    
    if current_scenario:
        scenarios.append('\n'.join(current_scenario))
    
    return {
        'feature': feature,
        'scenarios': scenarios
    }

def generate_feature_file(gherkin_dict: Dict, output_path: str) -> None:
    """
    Genera un archivo .feature con todos los escenarios
    Args:
        gherkin_dict: Diccionario con feature y escenarios
        output_path: Ruta donde se guardará el archivo .feature
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(gherkin_dict['feature'] + '\n\n')
        for scenario in gherkin_dict['scenarios']:
            f.write(scenario + '\n\n')

def process_transcript_to_scenarios(transcript: str, output_path: str) -> None:
    """
    Procesa una transcripción completa y genera un archivo .feature con múltiples escenarios
    Args:
        transcript: Texto de la transcripción
        output_path: Ruta donde se guardará el archivo .feature
    """
    gherkin_text = get_gherkin_from_gpt(transcript)
    gherkin_dict = parse_gherkin_scenarios(gherkin_text)
    generate_feature_file(gherkin_dict, output_path)

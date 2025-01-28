import os
import re
import streamlit as st
from openai import OpenAI

def time_to_seconds(time_str):
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 4:
        days, hours, minutes, seconds = map(int, parts)
        return days * 86400 + hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")

def extract_test_case(lines, start, end):
    return "\n".join(lines[start:end+1])

def get_gherkin_from_gpt(test_case_text):
    """
    Utiliza GPT-4o para generar escenarios Gherkin en formato específico
    """
    client = OpenAI()
    
    prompt = f"""
    Convert the following test case description into a Gherkin scenario following this EXACT format:
    
    Scenario: [Título descriptivo del escenario en español]
        Given que [condición inicial en español]
        And [condición adicional en español]
        When [acción del usuario en español]
        And [acción adicional en español]
        Then [resultado esperado en español]
        And [resultado adicional en español]

    Rules:
    1. Start each Given step with "que"
    2. Make steps clear and specific
    3. Use natural Spanish language
    4. Keep steps concise but descriptive
    5. Focus on user actions and system responses
    6. Do not include technical details unless necessary
    
    Example format:
    Scenario: Búsqueda de cliente por parte de su razón social y validación de crédito
        Given que la aplicación está abierta en la pantalla de despacho
        And el usuario no conoce el RUT del cliente
        When el usuario presiona el botón con el signo de interrogación para buscar un cliente
        And el usuario digita "Falcao" como parte de la razón social del cliente
        And presiona Enter
        Then la aplicación debe mostrar una lista de clientes que concuerden con el patrón "Falcao"

    Test case to convert:
    {test_case_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a QA automation expert that creates Gherkin scenarios. You must follow the exact format provided, starting Given steps with 'que' and writing natural, clear steps in Spanish."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating Gherkin scenario: {str(e)}")
        return None

def split_test_case_file(input_filename):
    """
    Lee el archivo de casos de prueba y genera archivos Gherkin separados usando GPT-4o
    """
    with open(input_filename, 'r') as file:
        content = file.read()
    
    # Separar por bloques de texto vacíos (dos o más saltos de línea)
    test_cases = [tc.strip() for tc in content.split('\n\n') if tc.strip()]
    
    # Crear directorio para features si no existe
    features_dir = "features"
    if not os.path.exists(features_dir):
        os.makedirs(features_dir)
    
    # Generar un archivo .feature para cada caso de prueba
    for i, test_case in enumerate(test_cases, 1):
        # Limpiar el texto del caso de prueba
        cleaned_text = '\n'.join([
            re.sub(r'\{.*?\}', '', line).strip()
            for line in test_case.split('\n')
            if line.strip()
        ])
        
        if cleaned_text:  # Solo procesar si hay texto después de la limpieza
            # Obtener el escenario Gherkin usando GPT-4
            gherkin_content = get_gherkin_from_gpt(cleaned_text)
            
            if gherkin_content:
                feature_file = os.path.join(features_dir, f"features_{i}.feature")
                with open(feature_file, 'w', encoding='utf-8') as f:
                    f.write(gherkin_content)
                
                #st.success(f"Generated Gherkin scenario in features_{i}.feature")
            else:
                st.warning(f"Could not generate Gherkin scenario for test case {i}")

    st.success(f"Test cases processed and saved in '{features_dir}' directory")

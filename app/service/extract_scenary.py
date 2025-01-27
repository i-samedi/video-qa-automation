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
    Utiliza GPT-4 para generar escenarios Gherkin en inglés
    """
    client = OpenAI()
    
    prompt = f"""
    Convert the following test case description into a Gherkin scenario in English. 
    Make it detailed and follow BDD best practices. The scenario should include:
    - Feature description
    - Scenario name
    - Given/When/Then steps
    - And steps where appropriate
    
    Test case:
    {test_case_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a QA automation expert that creates Gherkin scenarios."},
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
    Lee el archivo de casos de prueba y genera archivos Gherkin separados usando GPT-4
    """
    with open(input_filename, 'r') as file:
        content = file.read()
    
    # Separar por bloques de texto vacíos
    test_cases = content.split('\n\n')
    
    # Crear directorio principal para features si no existe
    features_base_dir = "features"
    if not os.path.exists(features_base_dir):
        os.makedirs(features_base_dir)
    
    # Generar un archivo .feature para cada caso de prueba
    for i, test_case in enumerate(test_cases, 1):
        if not test_case.strip():
            continue
        
        # Crear subdirectorio para cada caso
        feature_dir = os.path.join(features_base_dir, f"features_{i}")
        if not os.path.exists(feature_dir):
            os.makedirs(feature_dir)
            
        # Limpiar el texto del caso de prueba
        cleaned_text = '\n'.join([
            re.sub(r'\{.*?\}', '', line).strip()
            for line in test_case.split('\n')
            if line.strip()
        ])
        
        # Obtener el escenario Gherkin usando GPT-4
        gherkin_content = get_gherkin_from_gpt(cleaned_text)
        
        if gherkin_content:
            feature_file = os.path.join(feature_dir, f"test_case_{i}.feature")
            with open(feature_file, 'w', encoding='utf-8') as f:
                f.write(gherkin_content)
            
            st.success(f"Generated Gherkin scenario in {feature_file}")
        else:
            st.warning(f"Could not generate Gherkin scenario for test case {i}")

    st.success(f"Test cases processed and saved in '{features_base_dir}' directory")

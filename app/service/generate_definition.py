import os
from openai import OpenAI
import re

def clean_code(code):
    """
    Limpia el código generado eliminando texto innecesario y formateando correctamente
    """
    # Eliminar bloques de texto markdown si existen
    code = re.sub(r'```python\n', '', code)
    code = re.sub(r'```\n?', '', code)
    
    # Eliminar espacios y líneas vacías extras
    lines = [line.rstrip() for line in code.splitlines()]
    lines = [line for line in lines if line.strip()]
    
    # Asegurar que solo hay una línea en blanco entre definiciones
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if line.strip():
            cleaned_lines.append(line)
            prev_empty = False
        elif not prev_empty:
            cleaned_lines.append(line)
            prev_empty = True
    
    return '\n'.join(cleaned_lines)

def create_step_definitions(feature_content):
    """
    Genera el código de definición de pasos para todo el archivo feature usando GPT-4o
    """
    client = OpenAI()
    
    prompt = f"""
    Lee el siguiente archivo .feature y genera las definiciones de pasos en formato Behave.
    Asigna nombres descriptivos a los métodos que coincidan con el texto del paso.
    Solo genera el código Python, sin explicaciones adicionales.

    FEATURE:
    {feature_content}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un generador de código Python que produce definiciones de pasos Behave."},
            {"role": "user", "content": prompt}
        ]
    )
    
    code = response.choices[0].message.content
    return clean_code(code)

def generate_step_definitions(feature_file):
    """
    Lee el archivo .feature y genera un único archivo de definiciones de pasos completo con este escenario que trascribimos de un video.
    Debe estar en formato behave y asignale un nombre descriptivo que sea el mismo del paso al metodo.
    """
    # Crear directorio steps si no existe
    steps_dir = os.path.join("features", "steps")
    if not os.path.exists(steps_dir):
        os.makedirs(steps_dir)
    
    # Leer el contenido del archivo feature
    with open(feature_file, 'r', encoding='utf-8') as f:
        feature_content = f.read()
    
    # Generar definiciones para todo el feature
    step_code = create_step_definitions(feature_content)
    
    # Guardar en un único archivo, sin agregar el encoding
    feature_name = os.path.splitext(os.path.basename(feature_file))[0]
    step_file = os.path.join(steps_dir, f'{feature_name}_steps.py')
    
    with open(step_file, 'w', encoding='utf-8') as f:
        f.write(step_code + "\n")
    
    return 1

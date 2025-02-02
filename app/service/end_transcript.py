import streamlit as st
from openai import OpenAI
import os

def process_final_transcript():
    try:
        # Leer la transcripción inicial
        with open("transcript.txt", "r", encoding="utf-8") as file:
            initial_transcript = file.read()

        client = OpenAI(
            base_url="https://api.openai.com/v1"
        )

        # Prompt optimizado para formato compatible con Gherkin
        system_prompt = """Procesa el texto siguiendo estas instrucciones específicas:
        1. Elimina todas las referencias temporales (fechas, horas, momentos específicos)
        2. Estructura el texto en un formato compatible con Gherkin:
           - Usa frases cortas y directas
           - Enfócate en acciones y resultados esperados
           - Usa voz activa
           - Mantén un formato "Dado/Cuando/Entonces" implícito
        3. Mantén todos los detalles técnicos y funcionales importantes
        4. Organiza el contenido en secciones lógicas separadas por líneas en blanco
        5. Elimina información redundante o no esencial
        6. Asegúrate que cada frase sea clara y autocontenida
        7. Mantén el significado original del texto pero optimízalo para la creación de casos de prueba"""

        # Realizar la llamada a GPT-4 con el prompt para formato Gherkin
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convierte el siguiente texto a un formato compatible con Gherkin:\n\n{initial_transcript}"}
            ],
            temperature=0.1  # Temperatura baja para mantener consistencia y precisión
        )

        improved_transcript = response.choices[0].message.content

        # Guardar la transcripción procesada
        output_path = "extracted_transcript.txt"
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(improved_transcript)

        st.success(f"Texto procesado y optimizado para Gherkin guardado en '{output_path}'")
        return improved_transcript

    except FileNotFoundError:
        st.error("No se encontró el archivo de transcripción inicial 'transcript.txt'")
        return None
    except Exception as e:
        st.error(f"Error al procesar el texto: {str(e)}")
        if hasattr(e, 'response'):
            st.error(f"Estado de la respuesta: {e.response.status_code}")
            st.error(f"Contenido de la respuesta: {e.response.text}")
        return None

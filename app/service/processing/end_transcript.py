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

        # Prompt optimizado para formato compatible con Gherkin y mejorado para acciones de selección de componentes
        system_prompt = """Procesa el texto siguiendo estas instrucciones específicas:
1. Elimina todas las referencias temporales (fechas, horas, momentos específicos).
2. Transforma el texto en un formato compatible con Gherkin, asegurándote de que:
   - Si se menciona la acción de seleccionar un componente y posteriormente se especifica una opción (por ejemplo, 'Bodegas de origen' y 'Bodega 2'), fusiona estas referencias en un único paso de acción: "Seleccionar apartado 'Bodegas de origen' y seleccionar 'Bodega 2'".
3. Utiliza frases cortas y directas.
4. Enfócate en acciones y resultados esperados.
5. Utiliza voz activa.
6. Organiza el contenido en secciones lógicas separadas por líneas en blanco, formando un formato implícito "Dado/Cuando/Entonces".
7. Conserva todos los detalles técnicos y funcionales importantes.
8. Elimina información redundante o no esencial.
9. Asegúrate de que cada frase sea clara, autocontenida y refleje una acción específica.
10. Mantén el significado original del texto, optimizándolo para la creación de casos de prueba en formato Gherkin."""

        # Realizar la llamada a o3-mini con el prompt para formato Gherkin
        response = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convierte el siguiente texto al formato compatible con Gherkin siguiendo las instrucciones detalladas:\n\n{initial_transcript}"}
            ],
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

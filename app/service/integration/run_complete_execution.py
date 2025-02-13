import os
import streamlit as st
from service.processing.extract_audio import extract_audio
from service.processing.extract_transcript import extract_transcript
from service.processing.end_transcript import process_final_transcript
from service.generation.extract_scenary import process_transcript_to_scenarios
from service.generation.generate_definition import generate_step_definitions
from service.integration.update_steps import update_steps_file

def run_complete_execution(video_file) -> None:
    """
    Ejecuta de forma completa los pasos de análisis:
      1. Guarda el video de forma temporal.
      2. Extrae el audio del video.
      3. Transcribe el audio y procesa la transcripción usando GPT-4.
      4. Genera escenarios en formato Gherkin.
      5. Genera las definiciones de pasos.
      6. Actualiza los steps con Playwright.
      
    Args:
        video_file: Objeto de archivo del video proveniente del uploader.
    """
    if not video_file:
        st.error("No se proporcionó un archivo de video.")
        return

    try:
        # 1. Guardar el video temporalmente
        temp_video_path = "temp_video.mp4"
        with open(temp_video_path, "wb") as f:
            f.write(video_file.getbuffer())

        # 2. Extraer audio
        with st.spinner("Extrayendo audio..."):
            extract_audio(temp_video_path)
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        st.success("Audio extraído correctamente.")

        # Verificar que existe el archivo de audio extraído
        if not os.path.exists("extracted_audio.ogg"):
            st.error("El archivo de audio no existe. Por favor, verifique la extracción.")
            return

        # 3. Transcribir audio
        with st.spinner("Transcribiendo audio..."):
            extract_transcript("extracted_audio.ogg")

        # 4. Procesar la transcripción con GPT-4
        with st.spinner("Mejorando la transcripción con IA..."):
            process_final_transcript()

        

    except Exception as e:
        st.error(f"Error en la ejecución completa: {str(e)}") 
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
    Ejecuta de forma completa los pasos de análisis en una única iteración:
      1. Guarda el video de forma temporal.
      2. Extrae el audio del video.
      3. Transcribe el audio y procesa la transcripción usando GPT-4.
      4. Genera features de cada escenario en formato Gherkin.
      5. Genera las definitions de pasos para cada escenario.
      6. Actualiza los steps con Playwright.
      
    Args:
        video_file: Objeto de archivo del video proveniente del uploader.
    """
    if not video_file:
        st.error("No se proporcionó un archivo de video.")
        return

    try:
        with st.status("Procesando video...") as status:
            # 1. Guardar el video temporalmente
            status.write("Guardando video temporalmente...")
            temp_video_path = "temp_video.mp4"
            with open(temp_video_path, "wb") as f:
                f.write(video_file.getbuffer())

            # 2. Extraer audio
            status.write("Extrayendo audio...")
            extract_audio(temp_video_path)
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)

            # 3. Transcribir y procesar audio
            if not os.path.exists("extracted_audio.ogg"):
                raise FileNotFoundError("El archivo de audio no existe. Por favor, verifique la extracción.")
            
            status.write("Transcribiendo audio...")
            extract_transcript("extracted_audio.ogg")
            
            status.write("Procesando transcripción con IA...")
            process_final_transcript()
            
            # 4. Generar features en formato Gherkin
            if not os.path.exists("extracted_transcript.txt"):
                raise FileNotFoundError("No se encontró la transcripción procesada.")
            
            status.write("Generando escenarios Gherkin...")
            with open("extracted_transcript.txt", "r", encoding="utf-8") as f:
                transcript = f.read()

            features_dir = "features"
            if not os.path.exists(features_dir):
                os.makedirs(features_dir)
            
            feature_file = os.path.join(features_dir, "scenario.feature")
            process_transcript_to_scenarios(transcript, feature_file)
            
            # 5. Generar las definitions de pasos
            status.write("Generando definiciones de pasos...")
            generate_step_definitions(feature_file)
            
            # 6. Actualizar los steps con Playwright
            status.write("Actualizando steps con Playwright...")
            update_steps_file()
            
            status.update(label="¡Proceso completado!", state="complete")

        # Mostrar resumen final
        st.success("Proceso completado exitosamente")
        
        # Mostrar resultados
        if os.path.exists(feature_file):
            with st.expander("Ver escenarios generados", expanded=True):
                with open(feature_file, 'r', encoding='utf-8') as f:
                    st.code(f.read(), language='gherkin')

    except FileNotFoundError as e:
        st.error(f"Error: {str(e)}")
    except Exception as e:
        st.error(f"Error en la ejecución: {str(e)}") 
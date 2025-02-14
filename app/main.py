import os
import sys
import streamlit as st
from dotenv import load_dotenv
from service.processing.extract_audio import extract_audio
from service.processing.extract_transcript import extract_transcript
import json
import re
from service.generation.extract_scenary import *
from service.generation.generate_definition import generate_step_definitions


# Cargar variables de entorno
load_dotenv()

# Configuración de la aplicación
def setup_page_config():
    st.set_page_config(
        page_title="Video QA Automation",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Configurar estilos sin fondo blanco
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            margin-top: 5px;
        }
        .stTextArea>div>div>textarea {
            font-family: monospace;
        }
        .stMarkdown {
            font-size: 1.1em;
        }
        img {
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)
    

def main():
    setup_page_config()
    
    st.title("*🎥 Video QA Automatizado - beta*")
    
    # Crear tabs 
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎥 Análisis del Video",
        "🎭 Escenarios de Prueba",
        "📝 Definiciones de Pasos",
        "🎭 Actualizar con Playwright"
    ])
    
    with tab1:
        st.markdown("### 📤 Subir Video")
        video_file = st.file_uploader(
            "Arrastra o selecciona un video para analizar",
            type=['mp4', 'mov', 'avi'],
            help="Formatos soportados: MP4, MOV, AVI"
        )
    
        if video_file:
            col1, col2 = st.columns([3,2])
            
            with col1:
                st.video(video_file)
                st.markdown("### 📋 Detalles del Video")
                st.json({
                    "Nombre": video_file.name,
                    "Tamaño": f"{video_file.size / 1024 / 1024:.2f} MB",
                    "Tipo": video_file.type
                })
            
            with col2:
                st.markdown("### 🎯 Acciones")
                
                if st.button("🎥 Ejecución Completa", type="primary"):
                    try:
                        from service.integration.run_complete_execution import run_complete_execution
                        run_complete_execution(video_file) 
                    except Exception as e:
                        st.error(f"Error en la ejecución completa: {str(e)}")
                
                if st.button("📝 Generar Transcripción de la Prueba"):
                    if video_file:
                        try:
                            # 1. Extraer audio    
                            with st.spinner("Extrayendo audio..."):
                                with open("temp_video.mp4", "wb") as f:
                                    f.write(video_file.getbuffer())
                            extract_audio("temp_video.mp4")
                            if os.path.exists("temp_video.mp4"):
                                os.remove("temp_video.mp4")
                            st.success("Audio extraído correctamente")
                           
                            # 2. Transcribir audio
                            if not video_file:
                                st.error("Please upload a video file first.")
                            elif os.path.exists("extracted_audio.ogg"):
                                with st.spinner("Transcribiendo audio..."):
                                    extract_transcript("extracted_audio.ogg")
                                    # 3. Procesar transcripción con GPT-4
                                    with st.spinner("Mejorando la transcripción con IA..."):
                                        from service.processing.end_transcript import process_final_transcript
                                        process_final_transcript()
                            else:
                                st.error("El archivo de audio no existe. Por favor, extrae el audio primero.")
                        except Exception as e:
                            st.error(f"Ocurrió un error durante el proceso: {str(e)}")
                    else:
                        st.error("Por favor, suba un archivo de video primero.")
                    
                # 3. Generar escenario Gherkin
                if st.button("🎭 Generar Escenarios de la Prueba"):
                    with st.spinner("Generando escenarios de prueba..."):
                        try:
                            # Verificar si existe la transcripción
                            if not os.path.exists("extracted_transcript.txt"):
                                st.error("No se encontró la transcripción. Por favor, genere primero la transcripción.")
                                return
                            
                            # Leer la transcripción
                            with open("extracted_transcript.txt", "r", encoding='utf-8') as f:
                                transcript = f.read()
                            
                            # Crear directorio features si no existe
                            features_dir = "features"
                            if not os.path.exists(features_dir):
                                os.makedirs(features_dir)
                            
                            # Ruta del archivo feature
                            feature_file = os.path.join(features_dir, "scenario.feature")
                            
                            # Procesar la transcripción y generar los escenarios
                            process_transcript_to_scenarios(transcript, feature_file)
                            
                            st.success("Escenarios Gherkin generados y guardados correctamente")
                            
                            # Mostrar los escenarios generados
                            with open(feature_file, 'r', encoding='utf-8') as f:
                                gherkin_content = f.read()
                            
                            # Parsear los escenarios para mostrar estadísticas
                            scenarios_dict = parse_gherkin_scenarios(gherkin_content)
                            num_scenarios = len(scenarios_dict['scenarios'])
                            
                            # Mostrar estadísticas
                            st.info(f"Se generaron {num_scenarios} escenarios de prueba")
                            
                        except Exception as e:
                            st.error(f"Error al generar los escenarios: {str(e)}")
                    
                    
    with tab2:
        st.markdown("### 📀 Features Generados")
        col1, col2 = st.columns([2,1])
    
        with col1:
            feature_file = os.path.join("features", "scenario.feature")
            if os.path.exists(feature_file):
                with open(feature_file, 'r', encoding='utf-8') as f:
                    gherkin_content = f.read()
            
                scenarios_dict = parse_gherkin_scenarios(gherkin_content)
            
                st.success(f"Se encontraron {len(scenarios_dict['scenarios'])} escenarios de prueba")
            
                with st.expander("📝 Feature General", expanded=True):
                    st.code(scenarios_dict['feature'], language='gherkin')
            
                for i, scenario in enumerate(scenarios_dict['scenarios'], 1):
                    with st.expander(f"🎭 Escenario {i}", expanded=False):
                        st.code(scenario, language='gherkin')
                        
            else:
                st.error("*Aún no se ha generado ningún escenario de prueba. Por favor, sube un video y genera escenarios en la pestaña 'Análisis del Video'*")
    
        with col2:
            if st.button("🎭 Generar Definition", type="primary"):
                try:
                    feature_file = os.path.join("features", "scenario.feature")
                    if not os.path.exists(feature_file):
                        st.error("No se encontró el archivo feature. Por favor, genera primero los escenarios.")
                        return
                    
                    with st.spinner("Generando definiciones de pasos..."):
                        generate_step_definitions(feature_file)
                        st.success("Se generaron las definiciones de pasos exitosamente")
                                        
                except Exception as e:
                    st.error(f"Error al generar las definiciones: {str(e)}")
    
    with tab3:
        st.markdown("### 📝 Definiciones de Pasos")
    
        col1, col2 = st.columns([2,1])
        
        with col1:
            if os.path.exists("features/steps/scenario_steps.py"):
                steps_dir = os.path.join("features", "steps")
                step_file = os.path.join(steps_dir, "scenario_steps.py")
                if os.path.exists(step_file):
                    with st.expander("📝 Definiciones de pasos", expanded=True):
                        with open(step_file, 'r', encoding='utf-8') as f:
                            st.code(f.read(), language='python')
            else:
                st.error("*Aún no se han generado las definiciones de pasos. Por favor, genera primero los escenarios.*")
        
        with col2:
            if st.button("🎭 Actualizar con Playwright", type="primary"):
                try:
                    from service.integration.update_steps import update_steps_file
                    
                    with st.spinner("Actualizando steps con Playwright..."):
                        output_file = update_steps_file()
                        
                    st.success("Steps actualizados con Playwright exitosamente")
                        
                except FileNotFoundError as e:
                    st.error(f"Error: {str(e)}")
                except Exception as e:
                    st.error(f"Error inesperado al actualizar los steps: {str(e)}")
    
    with tab4:
        st.markdown("### 🎭 Definitions con Playwright")
        col1, col2 = st.columns([3,1])
    
        with col1:
            if os.path.exists("features/steps/scenario_steps_playwright.py"):
                with open("features/steps/scenario_steps_playwright.py", 'r', encoding='utf-8') as f:
                    st.code(f.read(), language='python')
            else:
                st.error("*Aún no se han generado las actualizaciones con Playwright. Por favor, genera primero los definitions.*")
    
if __name__ == "__main__":
    main()




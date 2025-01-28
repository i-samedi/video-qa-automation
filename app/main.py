import streamlit as st
import os
from dotenv import load_dotenv
from service.extract_audio import extract_audio
from service.extract_transcript import extract_transcript
import json
import re
from service.extract_scenary import *
from service.generate_definition import generate_step_definitions


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
    

def sidebar_content():
    with st.sidebar:
        st.image("https://static.wixstatic.com/media/0b7cad_d93db1cbf404473fa826423825390a4b~mv2.png/v1/fill/w_534,h_128,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/logo%20botman.png", width=200)
        st.title("*Transforme su negocio con el poder de la Inteligencia Artificial.*")
        
        st.markdown("### ℹ️ Ayuda")
        with st.expander("🚀 Guía de Uso Rápida"):
            st.markdown("""
                1. Sube video de prueba (MP4, MOV, AVI).
                2. Obtener la transcripción del video.
                3. Identificar los escenarios de prueba.
                4. Generar los escenarios en formato Gherkin.
            """)


def main():
    setup_page_config()
    sidebar_content()
    
    st.title("*🎥 Video QA Automatizado - BotMan IA beta*")
    
    #crear tabs 
    tab1, tab2, tab3 = st.tabs(["🎥 Análisis del Video", "🎭 Escenarios de Prueba", "📝 Definiciones de Pasos"])
    
    with tab1:
        st.markdown("### 📤 Subir Video")
        video_file = st.file_uploader(
            "Arrastra o selecciona un video para analizar",
            type=['mp4', 'mov', 'avi'],
            help="Formatos soportados: MP4, MOV, AVI"
        )
    
        if video_file:
            col1, col2 = st.columns([2,3])
            
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
                if st.button("📝 Generar Transcripción de la Prueba"):
                    if video_file:
                        try:
                            # 1. Extraer audio
                            if not os.path.exists("extracted_audio.ogg"):
                                with st.spinner("Extrayendo audio..."):
                                    with open("temp_video.mp4", "wb") as f:
                                        f.write(video_file.getbuffer())
                                extract_audio("temp_video.mp4")
                                if os.path.exists("temp_video.mp4"):
                                    os.remove("temp_video.mp4")
                                st.success("Audio extraído correctamente")
                            else:
                                st.info("El archivo de audio ya existe. No se extraerá nuevamente.")

                            # 2. Transcribir audio
                            if not video_file:
                                st.error("Please upload a video file first.")
                            elif os.path.exists("extracted_audio.ogg"):
                                with st.spinner("Transcribiendo audio..."):
                                    extract_transcript("extracted_audio.ogg")
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
                    
            # Opción para descargar el archivo feature
            # st.download_button(
            #     label="⬇️ Descargar archivo .feature",
            #     data=gherkin_content,
            #     file_name="scenario.feature",
            #     mime="text/plain"
            # )
        else:
            st.error("*Aún no se ha generado ningún escenario de prueba. Por favor, sube un video y genera escenarios en la pestaña 'Análisis del Video'*")

        col1, col2 = st.columns([2,3])
        with col1:
            if st.button("🎭 Generar Definition"):
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

        if os.path.exists("features/steps/scenario_steps.py"):
            steps_dir = os.path.join("features", "steps")
            step_file = os.path.join(steps_dir, "scenario_steps.py")
            if os.path.exists(step_file):
                with st.expander("📝 Definiciones de pasos", expanded=True):
                    with open(step_file, 'r', encoding='utf-8') as f:
                        st.code(f.read(), language='python')
        else:
            st.error("*Aún no se han generado las definiciones de pasos. Por favor, genera primero los escenarios.*")
                    
                    
                    
if __name__ == "__main__":
    main()




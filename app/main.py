import streamlit as st
import os
from dotenv import load_dotenv
from service.extract_audio import extract_audio
from service.extract_transcript import extract_transcript
from service.identify_scenery import identify_test_case_indices
import json
import re
from service.extract_scenary import extract_test_case, split_test_case_file, time_to_seconds


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
    
    tabs = st.tabs(["📹 Análisis del Video", "🎬 Escenarios de Prueba", "BETA"])
    
    with tabs[0]:
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
                if st.button("📝 Iniciar Transcripción del Video"):
                    if video_file:
                        with st.spinner("Extrayendo audio..."):
                            with open("temp_video.mp4", "wb") as f:
                                f.write(video_file.getbuffer())
                            extract_audio("temp_video.mp4")
                            if os.path.exists("temp_video.mp4"):
                                os.remove("temp_video.mp4")
                            st.success("Audio extraído correctamente")
                    else:
                        st.error("Please upload a video file first.")
                
                    if not video_file:
                        st.error("Please upload a video file first.")
                    elif os.path.exists("extracted_audio.ogg"):
                        with st.spinner("Transcribiendo audio..."):
                            transcript = extract_transcript("extracted_audio.ogg")
                            st.session_state['transcription'] = transcript
                            st.success("Transcripción completada")
                    else:
                        st.error("Audio file not found. Please extract audio first.")

                if st.button("🚀 Identificar Escenarios de Prueba"):
                    with st.spinner("Reading transcript..."):
                        transcript = open("extracted_transcript.txt", "r").read()

                    st.success("Transcript read successfully!")

                    with st.spinner("Identifying test case indices..."):
                        test_case_indices = identify_test_case_indices(transcript)

                    if test_case_indices:
                        st.success("Test case indices extracted successfully!")
                        with open("identify_test_case_indices_output.json", "w") as f:
                            json.dump(test_case_indices, f, indent=2)                                  
                            
    with tabs[1]:
        if st.button("🎭 Extraer Escenarios de Prueba"):
            with st.spinner("Extrayendo escenarios de prueba..."):
                input_filename_converted = "extracted_transcript.txt"
                with open(input_filename_converted, 'r') as file:
                    transcript_text = file.read()
                try:
                    with open("identify_test_case_indices_output.json", "r") as f:
                        indices_data = json.load(f)
                except FileNotFoundError:
                    st.error("Test case indices file not found. Please run 'Identify Test Case Indices' first.")
                    st.stop()

                lines = transcript_text.split('\n')
                test_cases = []

                for i, test_case_info in enumerate(indices_data['test_cases']):
                    start_time = time_to_seconds(test_case_info['start_time'])
                    end_time = time_to_seconds(test_case_info['end_time'])

                    # Find the closest matching lines
                    start = 0
                    end = len(lines) - 1
                    for j, line in enumerate(lines):
                        match = re.search(r'\{(.+?)\}\{(\d{2}:\d{2}:\d{2}:\d{2})\}', line)
                        if match:
                            line_time = time_to_seconds(match.group(2))
                            if line_time >= start_time and start == 0:
                                start = j
                            if line_time >= end_time:
                                end = j
                                break

                    test_case = extract_test_case(lines, start, end)
                    test_cases.append(test_case)  # Simplemente agregamos el contenido del test case

                # Save test cases to a file
                output_filename = "extracted_test_cases.txt"
                with open(output_filename, "w") as f:
                    f.write("\n\n".join(test_cases))  # Unimos los test cases con doble salto de línea

                st.success(f"Escenarios de prueba extraídos en {output_filename}")

                split_test_case_file(output_filename)
                
                # Mostrar los escenarios Gherkin generados
                features_dir = "features"
                if os.path.exists(features_dir):
                    st.success("Escenarios de prueba generados en 'features'")
                    
                    # Contenedor para mostrar los escenarios
                    with st.container():
                        # Estilo CSS para un diseño más minimalista
                        st.markdown("""
                            <style>
                            .stExpander {
                                border: none;
                                box-shadow: none;
                                background-color: transparent;
                            }
                            .streamlit-expanderHeader {
                                font-size: 1rem;
                                color: #262730;
                                background-color: #f0f2f6;
                                border-radius: 4px;
                                margin-bottom: 0.5rem;
                            }
                            </style>
                        """, unsafe_allow_html=True)
                        
                        # Ordenar los archivos numéricamente
                        feature_files = sorted(
                            [f for f in os.listdir(features_dir) if f.endswith('.feature')],
                            key=lambda x: int(''.join(filter(str.isdigit, x)))
                        )
                        
                        # Mostrar cada escenario en un expander con formato mejorado
                        for feature_file in feature_files:
                            with st.expander(f"📀 Escenario {feature_file.split('_')[1].split('.')[0]}"):
                                with open(os.path.join(features_dir, feature_file), 'r') as f:
                                    content = f.read()
                                    st.code(content, language='gherkin')

        

if __name__ == "__main__":
    main()




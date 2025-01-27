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
            margin-top: 10px;
        }
        .stTextArea>div>div>textarea {
            font-family: monospace;
        }
        .stMarkdown {
            font-size: 1.1em;
        }
        </style>
    """, unsafe_allow_html=True)
    
video_file = None

def sidebar_content():
    with st.sidebar:
        st.image("https://static.wixstatic.com/media/0b7cad_d93db1cbf404473fa826423825390a4b~mv2.png/v1/fill/w_534,h_128,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/logo%20botman.png", width=200)
        st.title("🛠️ Configuración")
        
        st.markdown("### ℹ️ Ayuda")
        with st.expander("Guía Rápida"):
            st.markdown("""
                1. Sube un video de prueba
                2. Espera la transcripción
                3. Revisa el análisis
                4. Descarga el script generado
            """)


def main():
    setup_page_config()
    sidebar_content()
    
    st.title("🎥 Video QA Automation - BotMan v0.1.5")
    
    tabs = st.tabs(["📹 Análisis de Video", "📊 Resultados", "🤖 Script Generator"])
    
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
                if st.button("🔍 Iniciar Transcripción del Video"):
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

                if st.button("🔍 Identificar Escenarios de Prueba"):
                    with st.spinner("Reading transcript..."):
                        # transcript = transcript_file.getvalue().decode("utf-8")
                        transcript = open("extracted_transcript.txt", "r").read()

                    st.success("Transcript read successfully!")

                    with st.spinner("Identifying test case indices..."):
                        test_case_indices = identify_test_case_indices(transcript)

                    if test_case_indices:
                        st.success("Test case indices extracted successfully!")

                        # Save test case indices to a file
                        with open("identify_test_case_indices_output.json", "w") as f:
                            json.dump(test_case_indices, f, indent=2)                                  
                            
    with tabs[1]:
        if st.button("Extraer Casos de Prueba"):
            with st.spinner("Extracting test cases..."):
                input_filename_converted = "extracted_transcript.txt"
                with open(input_filename_converted, 'r') as file:
                    transcript_text = file.read()

                # Read the test case indices from the JSON file
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
                    test_cases.append({
                        "title": f"Test Case {i+1}: {test_case_info['name']}",
                        "content": test_case
                    })

                for i, test_case in enumerate(test_cases, 1):
                    st.text_area(f"Test Case {i}", test_case['content'], height=200)

                # Save test cases to a file
                output_filename = "extracted_test_cases.txt"
                with open(output_filename, "w") as f:
                    f.write("\n\n".join([tc['content'] for tc in test_cases]))

                st.success(f"Test cases extracted and saved to {output_filename}")

                split_test_case_file(output_filename)
                
                # Mostrar los escenarios Gherkin generados
                features_dir = "features"
                if os.path.exists(features_dir):
                    st.success("Gherkin scenarios generated in 'features' directory")
                    
                    # Mostrar cada escenario en un expander
                    for feature_folder in sorted(os.listdir(features_dir)):
                        if feature_folder.startswith('features_'):
                            folder_path = os.path.join(features_dir, feature_folder)
                            if os.path.isdir(folder_path):
                                with st.expander(f"Scenario {feature_folder}"):
                                    for feature_file in os.listdir(folder_path):
                                        if feature_file.endswith('.feature'):
                                            with open(os.path.join(folder_path, feature_file), 'r') as f:
                                                st.code(f.read(), language='gherkin')

        

if __name__ == "__main__":
    main()




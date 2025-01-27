import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from faster_whisper import WhisperModel
import ffmpeg
import re
import torch

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

def sidebar_content():
    with st.sidebar:
        st.image("https://static.wixstatic.com/media/0b7cad_d93db1cbf404473fa826423825390a4b~mv2.png/v1/fill/w_534,h_128,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/logo%20botman.png", width=200)
        st.title("🛠️ Configuración")
        
        st.markdown("### 📝 Opciones de Análisis")
        model_type = st.selectbox(
            "Modelo de Transcripción",
            ["base", "small", "medium", "large"],
            help="Selecciona el tamaño del modelo Whisper"
        )
        
        temperature = st.slider(
            "Creatividad del LLM",
            0.0, 1.0, 0.7,
            help="Mayor valor = más creatividad"
        )
        
        st.markdown("### 🎯 Acciones Rápidas")
        if st.button("📋 Ver Historial"):
            st.info("Función en desarrollo")
        
        if st.button("⚙️ Configurar API Keys"):
            st.text_input("OpenAI API Key", type="password")
            st.button("Guardar")
        
        st.markdown("### ℹ️ Ayuda")
        with st.expander("Guía Rápida"):
            st.markdown("""
                1. Sube un video de prueba
                2. Espera la transcripción
                3. Revisa el análisis
                4. Descarga el script generado
            """)

# Inicialización de directorios
DIRS = {
    "video": "./videos",
    "output": "./output",
    "script": "./scripts"
}

for dir_path in DIRS.values():
    os.makedirs(dir_path, exist_ok=True)

# Configuración del modelo Whisper
@st.cache_resource
def load_whisper_model():
    try:
        # Intentar cargar el modelo con configuración específica
        model = WhisperModel(
            "base",
            device="cpu" if not torch.cuda.is_available() else "cuda",
            compute_type="int8",
            download_root=os.path.join(os.path.dirname(__file__), "models")
        )
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo Whisper: {str(e)}")
        return None

def transcribe_video(video_path):
    model = load_whisper_model()
    if model is None:
        st.error("No se pudo cargar el modelo de transcripción")
        return ""
    
    try:
        segments, _ = model.transcribe(
            video_path,
            beam_size=5,
            language='es',  # o el idioma que necesites
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=400
            )
        )
        return " ".join([segment.text for segment in segments])
    except Exception as e:
        st.error(f"Error durante la transcripción: {str(e)}")
        return ""

def clean_input_text(text):
    """Limpia el texto para juntar números y letras que deberían estar unidos."""
    # Patrones para encontrar números y códigos separados
    patterns = [
        # Números separados por espacios o comas (1 2 3 -> 123)
        (r'(\d)\s+(\d)', r'\1\2'),
        # Letras y números separados (TC 123 -> TC123)
        (r'([A-Za-z])\s+(\d)', r'\1\2'),
        # Números y letras separados (123 ABC -> 123ABC)
        (r'(\d)\s+([A-Za-z])', r'\1\2'),
        # Códigos comunes separados (INV 123 -> INV123)
        (r'(INV|TC|ORD|CL|DP|ST|CT|DOC)\s*[-_]?\s*(\d+)', r'\1\2'),
        # Números separados por puntos (120.000 -> 120000)
        (r'(\d+)\s*[-_]?\s*(\d+)', r'\1\2'),
    ]
    
    # Aplicar cada patrón iterativamente
    for pattern, replacement in patterns:
        while re.search(pattern, text):
            text = re.sub(pattern, replacement, text)
    
    return text

def analyze_with_llm(text, system_prompt, user_prompt):
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Limpiar el texto antes de procesarlo
    cleaned_text = clean_input_text(text)
    
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        {text}
        
        IMPORTANTE: 
        - Todos los números y códigos deben estar juntos sin espacios (ejemplo: TC123 en lugar de TC 123)
        - Los números secuenciales deben unirse (ejemplo: 123456 en lugar de 1 2 3 4 5 6)
        - Los códigos de referencia deben mantener este formato:
          * Trailer: TC[números]
          * Factura: INV[números]
          * Orden: ORD[números]
          * Cliente: CL[números]
          * Departamento: DP[números]
          * Tienda: ST[números]
          * Carro: CT[números]
          * Documento: DOC[números]
        """ + user_prompt
    )
    
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        output_parser=StrOutputParser()
    )
    
    response = chain.invoke({"text": cleaned_text})
    return response['text'] if isinstance(response, dict) else response

def generate_playwright_script(analysis):
    # Limpiar el análisis antes de generar el script
    cleaned_analysis = clean_input_text(analysis)
    
    playwright_prompt = """
    Genera un script de Playwright en TypeScript basado en el siguiente análisis:
    
    {text}
    
    IMPORTANTE:
    - Usa los códigos exactamente como aparecen en el análisis (ejemplo: TC123, INV456)
    - No separes los números o códigos con espacios
    - Mantén el formato de los códigos:
      * TC[números] para tráilers
      * INV[números] para facturas
      * ORD[números] para órdenes
      * CL[números] para clientes
      * DP[números] para departamentos
      * ST[números] para tiendas
      * CT[números] para carros
      * DOC[números] para documentos
    
    El script debe seguir esta estructura exacta:
    1. Importar desde '@playwright/test'
    2. Usar test.describe para el conjunto de pruebas
    3. Usar test.beforeAll, test.afterAll, test.beforeEach y test.afterEach
    4. Incluir manejo de errores con try/catch y throw
    5. Usar page.goto, page.fill, page.click, etc. para las acciones
    6. Usar expect para las aserciones
    
    Estructura base a seguir (adapta según el análisis):
    
    import {{ test, expect, chromium, type Browser, type Page }} from '@playwright/test';

    let browser: Browser;
    let page: Page;

    test.describe('Nombre Suite', () => {{
      test.beforeAll(async () => {{
        browser = await chromium.launch();
      }});
      
      test.afterAll(async () => {{
        await browser.close();
      }});
      
      test.beforeEach(async () => {{
        page = await browser.newPage();
      }});
      
      test.afterEach(async () => {{
        await page.close();
      }});
      
      test('Nombre Test', async () => {{
        try {{
          // Acciones de prueba aquí
        }} catch (error) {{
          console.error('Error:', error);
          throw error;
        }}
      }});
    }});
    
    Devuelve SOLO el código del script, sin explicaciones adicionales.
    """
    
    script = analyze_with_llm(
        cleaned_analysis,
        "Eres un experto en automatización de pruebas con Playwright.",
        playwright_prompt
    )
    
    if isinstance(script, dict):
        script = script.get('text', '')
    
    return script

def main():
    setup_page_config()
    sidebar_content()
    
    st.title("🎥 Video QA Automation")
    
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
                if st.button("🔍 Iniciar Análisis", use_container_width=True):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                        tmp_file.write(video_file.getvalue())
                        video_path = tmp_file.name

                    with st.spinner("🎙️ Transcribiendo video..."):
                        transcription = transcribe_video(video_path)
                        st.session_state['transcription'] = transcription
                        st.success("✅ Transcripción completada")

                    with st.spinner("🧠 Analizando contenido..."):
                        analysis = analyze_with_llm(
                            transcription,
                            "Eres un analista de QA experto.",
                            """
                            Analiza esta transcripción y extrae:
                            1. Pasos de prueba
                            2. Inputs esperados
                            3. Outputs esperados
                            4. Condiciones especiales
                            
                            {text}
                            """
                        )
                        st.session_state['analysis'] = analysis
                        st.success("✅ Análisis completado")

                    os.unlink(video_path)
                    
                    # Cambiar a la pestaña de resultados
                    tabs[1].active = True

    with tabs[1]:
        if 'transcription' in st.session_state:
            st.markdown("### 📝 Transcripción")
            st.text_area(
                "Texto transcrito",
                st.session_state['transcription'],
                height=200
            )
            
            st.markdown("### 🔍 Análisis")
            st.text_area(
                "Resultados del análisis",
                st.session_state['analysis'],
                height=200
            )
            
            if st.button("🤖 Generar Script de Pruebas", use_container_width=True):
                with st.spinner("⚙️ Generando script..."):
                    playwright_script = generate_playwright_script(st.session_state['analysis'])
                    st.session_state['script'] = playwright_script
                    # Cambiar a la pestaña de script
                    tabs[2].active = True

    with tabs[2]:
        if 'script' in st.session_state:
            st.markdown("### 📜 Script de Pruebas")
            st.code(st.session_state['script'], language="typescript")
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Descargar Script",
                    data=st.session_state['script'],
                    file_name="test.spec.ts",
                    mime="text/plain",
                    use_container_width=True
                )
            with col2:
                if st.button("▶️ Ejecutar Pruebas", use_container_width=True):
                    st.info("Función de ejecución en desarrollo")

if __name__ == "__main__":
    main()




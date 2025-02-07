# Automatización QA con IA para Videos
El sistema permite la generación automática de casos de prueba a partir de videos demostrativos, facilitando la creación y mantenimiento de pruebas automatizadas.

## Instrucciones paso a paso
1. brew install cmake pkg-config
2. python -m venv venv
3. source venv/bin/activate
4. pip install --upgrade pip
5. pip install -r requirements.txt
6. playwright install
7. cd web && npm install

## Creación archivo .env
- Crear archivo .env en la raiz del proyecto con las siguientes variables:
    - OPENAI_API_KEY= ...
    - GOOGLE_API_KEY= ... (gemini)
    - CLAUDE_API_KEY= ...

## Ejecutar el proyecto
1. cd web && npm run dev (localhost:3000)
2. cd app && streamlit run main.py (localhost:8501)
3. // && behave

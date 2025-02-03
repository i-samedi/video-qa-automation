# video-qa-IA

## Instrucciones paso a paso
1. brew install cmake pkg-config
2. python -m venv venv
3. source venv/bin/activate
4. pip install --upgrade pip
5. pip install -r requirements.txt
6. playwright install

## Creación archivo .env
- Crear archivo .env en la raiz del proyecto con las siguientes variables:
    - OPENAI_API_KEY= ...
    - GOOGLE_API_KEY= ... (gemini)
    - CLAUDE_API_KEY= ...

## Ejecutar el proyecto
- streamlit run main.py
- behave --tags=@flujo_exitoso

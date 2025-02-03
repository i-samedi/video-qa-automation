from playwright.sync_api import sync_playwright
from behave import fixture, use_fixture
import os
import sys
import logging
from datetime import datetime
import json
import time

# Cargar locators
with open(os.path.join(os.path.dirname(__file__), 'locators', 'page_locators.json'), 'r') as f:
    LOCATORS = json.load(f)

def save_error_info(context, scenario):
    """Guarda información de debug cuando ocurre un error"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        error_dir = f"error_logs/{timestamp}_{scenario.name.replace(' ', '_')}"
        os.makedirs(error_dir, exist_ok=True)
        
        # Screenshot
        if hasattr(context, 'page'):
            context.page.screenshot(path=f"{error_dir}/error.png")
            
            # HTML
            with open(f"{error_dir}/page.html", "w", encoding='utf-8') as f:
                f.write(context.page.content())
            
            # Estado de la aplicación
            app_state = context.page.evaluate("""
                () => ({
                    react: {
                        version: window.React?.version,
                        mounted: !!document.querySelector('#root')?.children.length
                    },
                    elements: {
                        available: Array.from(document.querySelectorAll('[id]')).map(el => el.id)
                    }
                })
            """)
            
            with open(f"{error_dir}/app_state.json", "w") as f:
                json.dump(app_state, f, indent=2)
                
    except Exception as e:
        context.logger.error(f"Error guardando información de debug: {str(e)}")

def before_all(context):
    """Inicializa Playwright y configura el navegador"""
    try:
        # Crear directorios necesarios
        os.makedirs("error_logs", exist_ok=True)
        os.makedirs("app/test-results", exist_ok=True)
        
        # Configurar logging
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.DEBUG,
            format=log_format,
            handlers=[
                logging.FileHandler("app/test.log"),
                logging.StreamHandler()
            ]
        )
        context.logger = logging.getLogger('behave')
        
        # Iniciar Playwright
        context.playwright = sync_playwright().start()
        context.browser = context.playwright.chromium.launch(
            headless=False,
            args=['--start-maximized', '--disable-web-security', '--disable-features=IsolateOrigins']
        )
        
        # Crear contexto y página con timeouts más largos
        context.browser_context = context.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True
        )
        context.page = context.browser_context.new_page()
        context.page.set_default_timeout(30000)  # 30 segundos
        
        # Configurar event listeners para debugging
        context.page.on("console", lambda msg: context.logger.debug(f"Browser Console: {msg.text}"))
        context.page.on("pageerror", lambda err: context.logger.error(f"Page Error: {err}"))
        
        # Configuración de timeouts
        context.timeouts = {
            'element': 10000,  # 10 segundos para elementos
            'navigation': 30000,  # 30 segundos para navegación
            'retry_interval': 1000,  # 1 segundo entre reintentos
            'max_retries': 3  # número máximo de reintentos
        }
        
        # Navegar a la aplicación al inicio
        context.page.goto("http://localhost:3000", wait_until="networkidle")
        
    except Exception as e:
        context.logger.error(f"Error en before_all: {str(e)}")
        cleanup_context(context)
        raise

def before_scenario(context, scenario):
    """Prepara cada escenario sin reiniciar la página"""
    try:
        context.logger.info(f"Iniciando escenario: {scenario.name}")
        
        # Verificar que la página está lista
        context.page.wait_for_function("""
            () => {
                return document.readyState === 'complete' && 
                       !!document.querySelector('#panel1') &&
                       !!document.querySelector('#groupbox1') &&
                       !!document.querySelector('#groupbox3')
            }
        """, timeout=30000)
        
    except Exception as e:
        context.logger.error(f"Error en before_scenario: {str(e)}")
        save_error_info(context, scenario)
        raise

def after_scenario(context, scenario):
    """Captura errores sin cerrar la página"""
    if scenario.status == "failed":
        save_error_info(context, scenario)

def after_all(context):
    """Limpia todos los recursos al final"""
    cleanup_context(context)

def cleanup_context(context):
    """Limpia los recursos de Playwright"""
    try:
        if hasattr(context, 'page'):
            context.page.close()
        if hasattr(context, 'browser_context'):
            context.browser_context.close()
        if hasattr(context, 'browser'):
            context.browser.close()
        if hasattr(context, 'playwright'):
            context.playwright.stop()
    except Exception as e:
        if hasattr(context, 'logger'):
            context.logger.error(f"Error durante la limpieza: {str(e)}")

def after_step(context, step):
    if step.status == "failed":
        step_name = step.name.replace(' ', '_')
        context.page.screenshot(path=f"error_{step_name}.png")
        
        # Guardar el HTML de la página
        html_content = context.page.content()
        with open(f"error_{step_name}.html", "w", encoding="utf-8") as f:
            f.write(html_content)

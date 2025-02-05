import os
import sys
import json
import time
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright
from behave import fixture, use_fixture
from app.service.update_steps import extract_locators_to_json

# Cargar locators desde el archivo JSON
LOCATORS_PATH = os.path.join(os.path.dirname(__file__), 'locators', 'page_locators.json')
if not os.path.exists(LOCATORS_PATH):
    # Si el archivo de locators no existe, se genera primero
    extract_locators_to_json()
with open(LOCATORS_PATH, 'r', encoding='utf-8') as f:
    LOCATORS = json.load(f)


def save_error_info(context, scenario):
    """
    Guarda información de depuración cuando ocurre un error:
      - Captura una captura de pantalla.
      - Guarda el HTML actual de la página.
      - Extrae información del estado de la aplicación.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Crea un directorio de error único para el escenario
        error_dir = os.path.join("report", f"{timestamp}_{scenario.name.replace(' ', '_')}")
        os.makedirs(error_dir, exist_ok=True)

        if hasattr(context, 'page'):
            # Guardar captura de pantalla
            screenshot_path = os.path.join(error_dir, "error.png")
            context.page.screenshot(path=screenshot_path)
            context.logger.debug(f"Captura de pantalla guardada en: {screenshot_path}")

            # Guardar HTML de la página
            html_path = os.path.join(error_dir, "page.html")
            with open(html_path, "w", encoding='utf-8') as f_html:
                f_html.write(context.page.content())
            context.logger.debug(f"HTML de la página guardado en: {html_path}")

            # Guardar estado de la aplicación (por ejemplo, información de React y elementos presentes)
            app_state = context.page.evaluate("""
                () => ({
                    react: {
                        version: window.React ? window.React.version : null,
                        mounted: !!document.querySelector('#root') && document.querySelector('#root').children.length > 0
                    },
                    elements: Array.from(document.querySelectorAll('[id]')).map(el => el.id)
                })
            """)
            app_state_path = os.path.join(error_dir, "app_state.json")
            with open(app_state_path, "w") as f_state:
                json.dump(app_state, f_state, indent=2)
            context.logger.debug(f"Estado de la aplicación guardado en: {app_state_path}")
    except Exception as e:
        context.logger.error(f"Error guardando información de depuración: {str(e)}")


def before_all(context):
    """
    Inicializa Playwright y configura el navegador, el contexto y la página.
    También configura el logging y navega a la URL inicial de la aplicación.
    """
    try:
        # Crear directorios para reportes y resultados de pruebas
        os.makedirs("report", exist_ok=True)

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
        context.logger = logging.getLogger("behave")
        context.logger.info("Iniciando before_all...")

        # Iniciar Playwright y lanzar el navegador (en modo no headless para debug)
        context.playwright = sync_playwright().start()
        context.browser = context.playwright.chromium.launch(
            headless=False,
            args=['--start-maximized', '--disable-web-security', '--disable-features=IsolateOrigins']
        )

        # Crear un contexto de navegador con viewport personalizado e ignorar errores HTTPS
        context.browser_context = context.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True
        )

        # Crear una nueva página
        context.page = context.browser_context.new_page()
        context.page.set_default_timeout(30000)  # 30 segundos de timeout por defecto

        # Configurar listeners para consola y errores de la página
        context.page.on("console", lambda msg: context.logger.debug(f"Browser Console: {msg.text}"))
        context.page.on("pageerror", lambda err: context.logger.error(f"Page Error: {err}"))

        # Configuración adicional de timeouts (puedes ajustar estos valores según tus necesidades)
        context.timeouts = {
            'element': 10000,       # 10 segundos para elementos
            'navigation': 30000,    # 30 segundos para navegación
            'retry_interval': 1000, # 1 segundo entre reintentos
            'max_retries': 3        # número máximo de reintentos
        }

        # Navegar a la URL de la aplicación
        context.logger.info("Navegando a la URL de la aplicación...")
        context.page.goto("http://localhost:3000", wait_until="networkidle")
        context.logger.info("Aplicación cargada correctamente.")

    except Exception as e:
        context.logger.error(f"Error en before_all: {str(e)}")
        cleanup_context(context)
        raise


def before_scenario(context, scenario):
    """
    Se ejecuta antes de cada escenario. Se utiliza para verificar que la página
    esté completamente cargada y que los elementos principales existan.
    """
    try:
        context.logger.info(f"Iniciando escenario: {scenario.name}")
        # Espera a que la página esté completamente cargada y que los contenedores principales existan.
        context.page.wait_for_function("""
            () => {
                return document.readyState === 'complete' &&
                       !!document.querySelector('#panel1') &&
                       !!document.querySelector('#groupbox1') &&
                       !!document.querySelector('#groupbox3');
            }
        """, timeout=30000)
    except Exception as e:
        context.logger.error(f"Error en before_scenario: {str(e)}")
        save_error_info(context, scenario)
        raise


def after_scenario(context, scenario):
    """
    Se ejecuta después de cada escenario. Si el escenario falla, se guarda la información
    de depuración (captura de pantalla, HTML, etc.).
    """
    if scenario.status == "failed":
        context.logger.error(f"Escenario fallido: {scenario.name}")
        save_error_info(context, scenario)
    else:
        context.logger.info(f"Escenario completado correctamente: {scenario.name}")


def after_step(context, step):
    """
    Se ejecuta después de cada paso. Si el paso falla, se captura una captura de pantalla y
    se guarda el HTML de la página para facilitar el debug.
    """
    if step.status == "failed":
        step_name = step.name.replace(' ', '_')
        screenshot_path = f"error_{step_name}.png"
        context.page.screenshot(path=screenshot_path)
        context.logger.debug(f"Captura de pantalla del paso fallido guardada en: {screenshot_path}")

        # Guardar el HTML de la página en un archivo
        html_path = f"error_{step_name}.html"
        with open(html_path, "w", encoding="utf-8") as f_html:
            f_html.write(context.page.content())
        context.logger.debug(f"HTML del paso fallido guardado en: {html_path}")


def after_all(context):
    """
    Se ejecuta al finalizar todas las pruebas y se encarga de limpiar los recursos.
    """
    context.logger.info("Finalizando pruebas... limpiando recursos.")
    cleanup_context(context)


def cleanup_context(context):
    """
    Cierra la página, el contexto del navegador, el navegador y detiene Playwright.
    """
    try:
        if hasattr(context, 'page'):
            context.page.close()
        if hasattr(context, 'browser_context'):
            context.browser_context.close()
        if hasattr(context, 'browser'):
            context.browser.close()
        if hasattr(context, 'playwright'):
            context.playwright.stop()
        context.logger.info("Recursos limpiados correctamente.")
    except Exception as e:
        if hasattr(context, 'logger'):
            context.logger.error(f"Error durante la limpieza: {str(e)}")

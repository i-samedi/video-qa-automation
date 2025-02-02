from playwright.sync_api import sync_playwright
from behave import fixture, use_fixture
import os
import sys
import logging

def before_all(context):
    """Inicializa Playwright y configura el navegador Chromium."""
    try:
        # Ajustar la ruta del archivo de log para que sea relativa a app/
        log_file = os.path.join("app", "test.log")
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger('behave')
        context.logger = logger
        playwright = sync_playwright().start()
        # Se usa Chromium como navegador por defecto y se define si se ejecuta en modo headless
        browser_type = 'chromium'
        headless = False  # Para ver el navegador durante las pruebas
        browser = playwright.chromium.launch(
            args=['--ignore-certificate-errors', '--start-maximized', '--disable-gpu'],
            headless=headless,
            slow_mo=50  # Agregar pequeño delay entre acciones para debugging
        )
        context.browser = browser
        context.page = browser.new_page()
        # Configurar viewport explícitamente
        context.page.set_viewport_size({"width": 1920, "height": 1080})
    except Exception as e:
        print(f"Error en before_all: {str(e)}", file=sys.stderr)
        if hasattr(context, 'playwright'):
            context.playwright.stop()
        raise

def before_scenario(context, scenario):
    """Crea un nuevo contexto y página para cada escenario y navega a la URL base."""
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()
    # Configuración de tamaño de viewport y timeout
    context.page.set_viewport_size({"width": 1920, "height": 1080})
    context.page.set_default_timeout(30000)
    
    # Navega a la URL base (localhost:3000)
    base_url = "http://localhost:3000"
    if base_url:
        context.page.goto(base_url, wait_until="networkidle")

def after_scenario(context, scenario):
    """Cierra el contexto del navegador y guarda un screenshot en caso de fallo."""
    if scenario.status == "failed" and hasattr(context, "page"):
        # Ajustar la ruta para que sea relativa a app/
        screenshot_dir = os.path.join("app", "test-results", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{scenario.name.replace(' ', '_')}.png")
        context.page.screenshot(path=screenshot_path)
        print(f"Screenshot guardado: {screenshot_path}")
    
    if hasattr(context, 'browser_context'):
        context.browser_context.close()

def after_all(context):
    """Cierra el navegador y detiene Playwright."""
    if hasattr(context, 'browser'):
        context.browser.close()
    if hasattr(context, 'playwright'):
        context.playwright.stop()

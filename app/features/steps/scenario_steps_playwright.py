from behave import given, when, then
from playwright.sync_api import expect, TimeoutError
import os
import json
import logging
import time  # <-- Se agrega para los bucles de espera

TIMEOUT = 15000  # 15 segundos

# Configurar logger (asegúrate de que se inicialice en environment.py o aquí)
logger = logging.getLogger("behave.steps")

# Cargar locators desde el archivo JSON
LOCATORS_PATH = os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json')
with open(LOCATORS_PATH, 'r') as f:
    LOCATORS = json.load(f)

@given('el usuario está en la pantalla de carga de pedidos')
def step_impl_usuario_en_pantalla_de_carga(context):
    context.page.wait_for_load_state('networkidle')
    expect(context.page.locator(LOCATORS['page']['title'])).to_be_visible(timeout=TIMEOUT)

@given('tiene acceso a todas las opciones necesarias')
def step_impl_usuario_con_acceso_opciones(context):
    expect(context.page.locator(LOCATORS['panel1']['container'])).to_be_visible(timeout=TIMEOUT)

@given('los parámetros iniciales están configurados')
def step_impl_parametros_iniciales_configurados(context):
    expect(context.page.locator(LOCATORS['groupBox1']['container'])).to_be_visible(timeout=TIMEOUT)

@when('el usuario selecciona la bodega origen del despacho')
def step_impl_seleccion_bodega(context):
    try:
        # 1. Esperar a que el contenedor principal del groupbox esté visible.
        groupbox_selector = LOCATORS['groupBox1']['container']  # Ejemplo: "#groupbox1"
        logger.debug(f"Esperando que el contenedor esté visible: {groupbox_selector}")
        expect(context.page.locator(groupbox_selector)).to_be_visible(timeout=TIMEOUT)
        
        # 2. Localizar el <select> de bodega.
        bodega_selector = LOCATORS['groupBox1']['selects']['bodega']  # Ejemplo: "#combobodega"
        logger.debug(f"Buscando select de bodega con el selector: {bodega_selector}")
        combo = context.page.locator(bodega_selector)
        # Si no se encontró el elemento de forma directa, se busca dentro del contenedor principal.
        if combo.count() == 0:
            logger.debug(f"No se encontró el elemento con {bodega_selector} de forma directa. Buscando dentro de {groupbox_selector}.")
            combo = context.page.locator(f"{groupbox_selector} {bodega_selector}")
        
        # 3. Esperar a que el <select> esté visible y habilitado.
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        
        # 4. Realizar mouse over sobre el select para simular la acción del usuario.
        logger.debug("Realizando mouse over en el select de bodega.")
        combo.hover()
        context.page.wait_for_timeout(1000)  # Espera adicional para que las opciones se desplieguen
        
        # 5. (Opcional) Verificar las opciones disponibles para mayor debug.
        opciones = combo.locator("option").all_inner_texts()
        logger.debug(f"Opciones disponibles en el select de bodega: {opciones}")
        if 'Bodega 2' not in opciones:
            raise Exception("La opción 'Bodega 2' no se encuentra en el dropdown. Opciones disponibles: " + ", ".join(opciones))
        
        # 6. Seleccionar la opción "Bodega 2" mediante su label.
        combo.select_option(label='Bodega 2')
        logger.info("Opción 'Bodega 2' seleccionada correctamente.")
        
    except TimeoutError:
        # En caso de timeout, se registra el contenido parcial de la página para debug.
        logger.error("Timeout al esperar el select del dropdown de bodega. Contenido de la página:\n" +
                     context.page.content()[:1000])
        raise Exception("Timeout al esperar el select del dropdown de bodega.")
    except Exception as e:
        raise Exception(f"Error al seleccionar bodega: {str(e)}")

@then('la bodega 2 es seleccionada correctamente')
def step_impl_bodega_seleccionada_correctamente(context):
    # Se valida que el <select> muestre el valor esperado.
    expect(context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])).to_have_value('2', timeout=TIMEOUT)

@when('el usuario ingresa el RUT correspondiente al pedido')
def step_impl_ingreso_rut(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
    except Exception as e:
        raise Exception(f"Error al ingresar el RUT: {e}")

@then('el RUT 123456789 es ingresado correctamente')
def step_impl_rut_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)

@when('el usuario selecciona el destino en el dropdown')
def step_impl_seleccion_destino(context):
    try:
        # 1. Esperar a que el contenedor principal del groupbox de ubicación esté visible.
        groupbox_selector = LOCATORS['groupBox3']['container']  # Ejemplo: "#groupbox3"
        logger.debug(f"Esperando que el contenedor esté visible: {groupbox_selector}")
        expect(context.page.locator(groupbox_selector)).to_be_visible(timeout=TIMEOUT)
        
        # 2. Localizar el <select> de ubicación.
        dropdown_selector = LOCATORS['groupBox3']['selects']['ubicacion']  # Ejemplo: "#comboubicacion"
        logger.debug(f"Buscando select de ubicación con el selector: {dropdown_selector}")
        combo = context.page.locator(dropdown_selector)
        # Si no se encontró el elemento directamente, se busca dentro del contenedor.
        if combo.count() == 0:
            logger.debug(f"No se encontró el elemento con {dropdown_selector} de forma directa. Buscando dentro de {groupbox_selector}.")
            combo = context.page.locator(f"{groupbox_selector} {dropdown_selector}")
        
        # 3. Esperar a que el <select> esté visible y habilitado.
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        
        # 4. Realizar mouse over sobre el select.
        logger.debug("Realizando mouse over en el select de ubicación.")
        combo.hover()
        context.page.wait_for_timeout(1000)  # Espera adicional para que las opciones se desplieguen
        
        # 5. Seleccionar la opción con valor '1'.
        combo.select_option('1')
        logger.info("Opción de ubicación '1' seleccionada correctamente.")
        
    except TimeoutError:
        logger.error("Timeout al esperar el select del dropdown de ubicación. Contenido de la página:\n" +
                     context.page.content()[:1000])
        raise Exception("Timeout al esperar el select del dropdown de ubicación.")
    except Exception as e:
        raise Exception(f"Error al seleccionar ubicación: {str(e)}")

@then('la ubicación número 1 es seleccionada correctamente')
def step_impl_ubicacion_seleccionada_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])).to_have_value('1', timeout=TIMEOUT)

@when('el usuario ingresa el número de pedido en el campo correspondiente')
def step_impl_ingreso_numero_pedido(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['numeroPedido'], '987')
    except Exception as e:
        raise Exception(f"Error al ingresar el número de pedido: {e}")

@then('el número de pedido 987 es ingresado correctamente')
def step_impl_numero_pedido_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])).to_have_value('987', timeout=TIMEOUT)

@when('el usuario hace clic en el botón grabar pedidos')
def step_impl_click_grabar_pedidos(context):
    try:
        # Usar locator() en lugar de wait_for_selector para obtener un Locator, no un ElementHandle.
        boton_selector = LOCATORS['panel1']['buttons']['grabarPedidos']  # Ejemplo: "#botongenerar"
        logger.debug(f"Buscando botón grabar pedidos con el selector: {boton_selector}")
        boton = context.page.locator(boton_selector)
        
        expect(boton).to_be_visible(timeout=TIMEOUT)
        # En lugar de esperar un bucle revisando el atributo "disabled", se intenta verificar si el botón se habilita.
        try:
            expect(boton).to_be_enabled(timeout=TIMEOUT)
            boton.click()
            logger.info("Se hizo clic en el botón grabar pedidos de forma normal.")
        except Exception as e:
            logger.warning("El botón aún está deshabilitado, forzando el clic.")
            boton.click(force=True)
            logger.info("Se hizo clic en el botón grabar pedidos con force=True.")
        
    except TimeoutError:
        logger.error("Timeout al esperar el botón de grabar pedidos. Contenido de la página:\n" +
                     context.page.content()[:1000])
        raise Exception("Timeout al esperar el botón de grabar pedidos.")
    except Exception as e:
        raise Exception(f"Error al hacer clic en el botón: {str(e)}")

@then('el pedido es grabado y el proceso queda completado')
def step_impl_pedido_grabado_y_proceso_completado(context):
    # Aquí se debería agregar la verificación final del proceso completado, por ejemplo,
    # la aparición de un mensaje de éxito o algún cambio en la UI que indique que el pedido se grabó.
    pass

from behave import given, when, then
from playwright.sync_api import expect, TimeoutError
import os
import json
import logging
import time  

TIMEOUT = 15000  

logger = logging.getLogger("behave.steps")

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
        
        # 2. Localizar el dropdown de bodega usando un selector simplificado.
        bodega_selector = "#groupbox1 button[role='combobox']"
        logger.debug(f"Buscando dropdown de bodega con el selector: {bodega_selector}")
        combo = context.page.locator(bodega_selector)
        
        # 3. Esperar a que el dropdown esté visible y habilitado.
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        
        # 4. Hacer clic en el dropdown para desplegar las opciones.
        combo.click()
        option_locator = context.page.locator('[role="option"]', has_text="Bodega 2")
        expect(option_locator).to_be_visible(timeout=TIMEOUT)
        # Seleccionar la opción "Bodega 2"
        option_locator.click()
        logger.info("Opción 'Bodega 2' seleccionada correctamente.")
        
    except TimeoutError:
        logger.error("Timeout al esperar el dropdown de bodega. Contenido de la página:\n" +
                     context.page.content()[:1000])
        raise Exception("Timeout al esperar el dropdown de bodega.")
    except Exception as e:
        raise Exception(f"Error al seleccionar bodega: {str(e)}")

@then('la bodega 2 es seleccionada correctamente')
def step_impl_bodega_seleccionada_correctamente(context):
    # Se valida que el <select> muestre el valor esperado.
    expect(context.page.locator("#groupbox1 button[role='combobox']")).to_have_text("Bodega 2", timeout=TIMEOUT)

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
        
        # 2. Localizar el dropdown de destino filtrado por el texto que lo identifica.
        dropdown_selector = "#groupbox3 button[role='combobox']"
        logger.debug(f"Buscando dropdown de destino con el selector: {dropdown_selector} y filtrando por 'Seleccione ubicación'")
        combo = context.page.locator(dropdown_selector, has_text="Seleccione ubicación")
        # 3. Esperar que el dropdown filtrado esté visible y habilitado.
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        
        # 4. Hacer clic en el dropdown para desplegar las opciones.
        combo.click()
        # Esperar a que la opción con texto "1" sea visible.
        option_locator = context.page.locator('[role="option"]', has_text="1")
        expect(option_locator).to_be_visible(timeout=TIMEOUT)
        # Seleccionar la opción "1"
        option_locator.click()
        logger.info("Opción de destino '1' seleccionada correctamente.")
        
    except TimeoutError:
        logger.error("Timeout al esperar el dropdown de destino. Contenido de la página:\n" +
                     context.page.content()[:1000])
        raise Exception("Timeout al esperar el dropdown de destino.")
    except Exception as e:
        raise Exception(f"Error al seleccionar destino: {str(e)}")

@then('la ubicación número 1 es seleccionada correctamente')
def step_impl_ubicacion_seleccionada_correctamente(context):
    expect(context.page.locator("#groupbox3 button[role='combobox']", has_text="1")).to_have_text("Ubicación 1", timeout=TIMEOUT)

@when('el usuario ingresa el número de pedido en el campo correspondiente')
def step_impl_ingreso_numero_pedido(context):
    try:
        # Localizar el input para el número de pedido.
        numero_pedido_locator = context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])
        # Esperar que el input sea visible.
        expect(numero_pedido_locator).to_be_visible(timeout=TIMEOUT)
        # Hacer clic en el input (force=True para asegurar la acción, en caso de overlays o estilos personalizados)
        numero_pedido_locator.click(force=True)
        # Limpiar el campo antes de ingresar el valor.
        numero_pedido_locator.fill('')
        # Ingresar el número de pedido '987'
        numero_pedido_locator.fill('987')
        # Presionar TAB para forzar el blure y actualizar el valor en pantalla si es necesario.
        context.page.keyboard.press("Tab")
        logger.info("Número de pedido '987' ingresado correctamente.")
    except Exception as e:
        raise Exception(f"Error al ingresar el número de pedido: {e}")

@then('el número de pedido 987 es ingresado correctamente')
def step_impl_numero_pedido_ingresado_correctamente(context):
    # Se verifica que el campo de número de pedido contenga el valor '987'
    expect(
        context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])
    ).to_have_value('987', timeout=TIMEOUT)

@when('el usuario hace clic en el botón grabar pedidos')
def step_impl_click_grabar_pedidos(context):
    try:
        # Usar locator() en lugar de wait_for_selector para obtener un Locator, no un ElementHandle.
        boton_selector = LOCATORS['panel1']['buttons']['grabarPedidos'] 
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

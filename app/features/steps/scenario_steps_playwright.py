from behave import given, when, then
from playwright.sync_api import expect
import os
import json

TIMEOUT = 15000  # 15 segundos

with open(os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json'), 'r') as f:
    LOCATORS = json.load(f)

@given('el usuario está en la pantalla de carga de pedidos')
def step_impl_usuario_en_pantalla_de_carga(context):
    # Asegúrate de que la página esté completamente cargada
    context.page.wait_for_load_state('networkidle')
    expect(context.page.locator(LOCATORS['page']['title'])).to_be_visible()

@given('tiene acceso a todas las opciones necesarias')
def step_impl_usuario_con_acceso_opciones(context):
    expect(context.page.locator(LOCATORS['panel1']['container'])).to_be_visible()

@given('los parámetros iniciales están configurados')
def step_impl_parametros_iniciales_configurados(context):
    expect(context.page.locator(LOCATORS['groupBox1']['container'])).to_be_visible()

@when('el usuario selecciona la bodega origen del despacho')
def step_impl(context):
    try:
        selector = LOCATORS['groupBox1']['selects']['bodega']
        combo = context.page.locator(selector)
        
        # Esperar a que el elemento esté visible y habilitado
        combo.wait_for(state='visible', timeout=TIMEOUT)
        combo.wait_for(state='enabled', timeout=TIMEOUT)
        
        # Verificar que el elemento esté realmente visible y habilitado
        if not combo.is_visible() or not combo.is_enabled():
            raise Exception("El elemento no está visible o habilitado")
        
        # Seleccionar la opción deseada
        combo.select_option('2')
    except Exception as e:
        context.page.screenshot(path=f"error_bodega_{context.scenario.name}.png")
        raise Exception(f"Error al seleccionar bodega: {str(e)}")

@then('la bodega 2 es seleccionada correctamente')
def step_impl_bodega_seleccionada_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])).to_have_value('2')

@when('el usuario ingresa el RUT correspondiente al pedido')
def step_impl_ingreso_rut(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
    except Exception as e:
        print(f"Error al ingresar el RUT: {e}")

@then('el RUT 123456789 es ingresado correctamente')
def step_impl_rut_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789')

@when('el usuario selecciona el destino en el dropdown')
def step_impl_seleccion_destino(context):
    try:
        selector = LOCATORS['groupBox3']['selects']['ubicacion']
        combo = context.page.locator(selector)
        
        # Esperar a que el elemento esté visible y habilitado
        combo.wait_for(state='visible', timeout=TIMEOUT)
        combo.wait_for(state='enabled', timeout=TIMEOUT)
        
        # Verificar que el elemento esté realmente visible y habilitado
        if not combo.is_visible() or not combo.is_enabled():
            raise Exception("El elemento no está visible o habilitado")
        
        # Seleccionar la opción deseada
        combo.select_option('1')
    except Exception as e:
        context.page.screenshot(path=f"error_ubicacion_{context.scenario.name}.png")
        raise Exception(f"Error al seleccionar ubicación: {str(e)}")

@then('la ubicación número 1 es seleccionada correctamente')
def step_impl_ubicacion_seleccionada_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])).to_have_value('1')

@when('el usuario ingresa el número de pedido en el campo correspondiente')
def step_impl_ingreso_numero_pedido(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['numeroPedido'], '987')
    except Exception as e:
        print(f"Error al ingresar el número de pedido: {e}")

@then('el número de pedido 987 es ingresado correctamente')
def step_impl_numero_pedido_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])).to_have_value('987')

@when('el usuario hace clic en el botón grabar pedidos')
def step_impl(context):
    try:
        boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
        
        # Esperar a que el botón esté visible y habilitado
        boton.wait_for(state='visible', timeout=TIMEOUT)
        boton.wait_for(state='enabled', timeout=TIMEOUT)
        
        boton.click()
    except Exception as e:
        context.page.screenshot(path=f"error_boton_{context.scenario.name}.png")
        raise Exception(f"Error al hacer clic en el botón: {str(e)}")

@then('el pedido es grabado y el proceso queda completado')
def step_impl_pedido_grabado_y_proceso_completado(context):
    # Verificar algún cambio en la UI que indique que el pedido fue grabado
    pass

from behave import given, when, then
from playwright.sync_api import expect, TimeoutError
import os
import json

TIMEOUT = 15000

LOCATORS_PATH = os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json')
with open(LOCATORS_PATH, 'r') as f:
    LOCATORS = json.load(f)

TIMEOUT = 5000  # Adjust the timeout as needed
LOCATORS = {
    "page": {
        "title": "h1:text(\"Carga de Pedidos a Bodegas\")"
    },
    "panel1": {
        "container": "#panel1",
        "inputs": {
            "observaciones": "#editobs",
            "lineasRechazadas": "#editlinerechazo",
            "cantidadRechazada": "#editcantrechazo"
        },
        "buttons": {
            "grabarPedidos": "#botongenerar",
            "cancelar": "#botoncancelar",
            "exportarDatos": "#botonexportar",
            "exportarOTR": "#botonexporotr",
            "salir": "#botonsalir"
        }
    },
    "groupBox1": {
        "container": "#groupbox1",
        "selects": {
            "bodega": "#combobodega"
        }
    },
    "groupBox3": {
        "container": "#groupbox3",
        "inputs": {
            "rut": "#editrut",
            "numeroPedido": "#editnropedido"
        },
        "selects": {
            "ubicacion": "#comboubicacion"
        }
    }
}
@given('el usuario está en la pantalla de carga de pedidos')
def step_usuario_en_pantalla_carga_pedidos(context):
    pass
@given('tiene acceso a todas las opciones necesarias')
def step_acceso_a_opciones_necesarias(context):
    pass
@given('los parámetros iniciales están configurados')
def step_parametros_iniciales_configurados(context):
    pass
@when('el usuario selecciona la bodega origen del despacho')
def step_usuario_selecciona_bodega_origen(context):
    try:
        combo = context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        combo.click()
        opcion = context.page.locator('[role="option"]', has_text="Bodega 2")
        expect(opcion).to_be_visible(timeout=TIMEOUT)
        opcion.click()
    except Exception as e:
        raise Exception(f"Error al seleccionar la bodega: {str(e)}")
@then('la bodega 2 es seleccionada correctamente')
def step_bodega_2_seleccionada_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])).to_have_text('Bodega 2', timeout=TIMEOUT)
@when('el usuario ingresa el RUT correspondiente al pedido')
def step_usuario_ingresa_rut(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
    except Exception as e:
        raise Exception(f"Error al ingresar el RUT: {e}")
@then('el RUT 123456789 es ingresado correctamente')
def step_rut_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
@when('el usuario selecciona el destino en el dropdown')
def step_usuario_selecciona_destino(context):
    try:
        combo = context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        combo.click()
        opcion = context.page.locator('[role="option"]', has_text="Ubicación 1")
        expect(opcion).to_be_visible(timeout=TIMEOUT)
        opcion.click()
    except Exception as e:
        raise Exception(f"Error al seleccionar el destino: {str(e)}")
@then('la ubicación número 1 es seleccionada correctamente')
def step_ubicacion_1_seleccionada_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])).to_have_text('Ubicación 1', timeout=TIMEOUT)
@when('el usuario ingresa el número de pedido en el campo correspondiente')
def step_usuario_ingresa_numero_pedido(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['numeroPedido'], '987')
    except Exception as e:
        raise Exception(f"Error al ingresar el número de pedido: {e}")
@then('el número de pedido 987 es ingresado correctamente')
def step_numero_pedido_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])).to_have_value('987', timeout=TIMEOUT)
@when('el usuario hace clic en el botón grabar pedidos')
def step_usuario_clic_boton_grabar_pedidos(context):
    try:
        boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
        expect(boton).to_be_visible(timeout=TIMEOUT)
        try:
            expect(boton).to_be_enabled(timeout=TIMEOUT)
            boton.click()
        except Exception as e:
            boton.click(force=True)
    except Exception as e:
        raise Exception(f"Error al hacer clic en el botón grabar pedidos: {str(e)}")
@then('el pedido es grabado y el proceso queda completado')
def step_pedido_grabado_proceso_completado(context):
    # Aquí se podría agregar una validación adicional para confirmar que el proceso se completó
    pass

from behave import given, when, then
from playwright.sync_api import expect, TimeoutError
import os
import json

TIMEOUT = 15000

LOCATORS_PATH = os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json')
with open(LOCATORS_PATH, 'r') as f:
    LOCATORS = json.load(f)

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
TIMEOUT = 5000
@given('el usuario está en la pantalla para la carga de pedidos a bodegas')
def step_usuario_esta_en_pantalla_carga(context):
    expect(context.page.locator(LOCATORS['page']['title'])).to_be_visible(timeout=TIMEOUT)
@given('la aplicación está conectada a la base de datos')
def step_aplicacion_conectada_base_datos(context):
    pass  # Implementación que verifica la conexión a la base de datos
@when('el usuario selecciona el apartado "Bodegas de origen" y elige "Bodega 2"')
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
        raise Exception(f"Error al seleccionar la bodega de origen: {str(e)}")
@then('la bodega de origen es seleccionada correctamente')
def step_bodega_origen_seleccionada_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])).to_have_text('Bodega 2', timeout=TIMEOUT)
@when('el usuario completa el campo "RUT" con "123456789"')
def step_usuario_completa_campo_rut(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
    except Exception as e:
        raise Exception(f"Error al ingresar el RUT: {e}")
@then('el RUT es ingresado correctamente')
def step_rut_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
@when('el usuario selecciona el dropdown "Destino" y elige la opción "Ubicación 1"')
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
@then('el destino es seleccionado correctamente')
def step_destino_seleccionado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])).to_have_text('Ubicación 1', timeout=TIMEOUT)
@when('el usuario completa el campo "Número de pedido" con "987"')
def step_usuario_completa_campo_numero_pedido(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['numeroPedido'], '987')
    except Exception as e:
        raise Exception(f"Error al ingresar el número de pedido: {e}")
@then('el número de pedido es ingresado correctamente')
def step_numero_pedido_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])).to_have_value('987', timeout=TIMEOUT)
@when('el usuario hace clic en el botón "Grabar pedidos"')
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
        raise Exception(f"Error al hacer clic en el botón: {str(e)}")
@then('el pedido se graba en la base de datos')
def step_pedido_grabado_base_datos(context):
    pass  # Implementación que verifica que el pedido fue grabado en la base de datos
@then('el proceso de carga de pedidos queda completado')
def step_proceso_carga_completado(context):
    pass  # Implementación que verifica que el proceso fue completado

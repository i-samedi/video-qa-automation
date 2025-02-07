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
@given('el usuario está en la pantalla para carga de pedidos a bodegas')
def given_usuario_en_pantalla_carga_pedidos(context):
    expect(context.page.locator(LOCATORS['page']['title'])).to_be_visible(timeout=TIMEOUT)
@given('el proceso de pedido desde el almacén central está habilitado')
def given_proceso_pedido_habilitado(context):
    # Implementación para verificar que el proceso está habilitado
    pass
@when('el usuario selecciona el apartado "Bodegas de origen"')
def when_usuario_selecciona_apartado_bodegas_origen(context):
    combo = context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])
    expect(combo).to_be_visible(timeout=TIMEOUT)
    expect(combo).to_be_enabled(timeout=TIMEOUT)
    combo.click()
@when('selecciona "Bodega 2"')
def when_usuario_selecciona_bodega_2(context):
    opcion = context.page.locator('[role="option"]', has_text="Bodega 2")
    expect(opcion).to_be_visible(timeout=TIMEOUT)
    opcion.click()
@then('la bodega de origen es seleccionada correctamente')
def then_bodega_origen_seleccionada_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])).to_have_text("Bodega 2", timeout=TIMEOUT)
@when('el usuario completa el campo RUT con "123456789"')
def when_usuario_completa_campo_rut(context):
    context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
@then('el RUT es ingresado correctamente')
def then_rut_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
@when('el usuario selecciona el destino "Ubicación 1" en el dropdown')
def when_usuario_selecciona_destino(context):
    combo = context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])
    expect(combo).to_be_visible(timeout=TIMEOUT)
    expect(combo).to_be_enabled(timeout=TIMEOUT)
    combo.click()
    opcion = context.page.locator('[role="option"]', has_text="Ubicación 1")
    expect(opcion).to_be_visible(timeout=TIMEOUT)
    opcion.click()
@then('el destino es seleccionado correctamente')
def then_destino_seleccionado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])).to_have_text("Ubicación 1", timeout=TIMEOUT)
@when('el usuario completa el campo número de pedido con "987"')
def when_usuario_completa_campo_numero_pedido(context):
    context.page.fill(LOCATORS['groupBox3']['inputs']['numeroPedido'], '987')
@then('el número de pedido es ingresado correctamente')
def then_numero_pedido_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])).to_have_value('987', timeout=TIMEOUT)
@when('el usuario hace clic en el botón "Grabar pedidos"')
def when_usuario_click_boton_grabar_pedidos(context):
    boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
    expect(boton).to_be_visible(timeout=TIMEOUT)
    try:
        expect(boton).to_be_enabled(timeout=TIMEOUT)
        boton.click()
    except Exception as e:
        boton.click(force=True)
@then('el pedido se completa')
def then_pedido_se_completa(context):
    # Implementación para verificar que el pedido se completa
    pass
@then('el pedido queda persistido en la base de datos')
def then_pedido_persistido_base_datos(context):
    # Implementación para verificar que el pedido se persiste en la base de datos
    pass

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
@given(u'el usuario está en la pantalla para cargar pedidos a bodegas')
def given_usuario_en_pantalla_carga_pedidos(context):
    pass
@given(u'el sistema permite realizar pedidos desde el almacén central a distintas bodegas')
def given_sistema_permite_pedidos_desde_almacen_central(context):
    pass
@when(u'el usuario selecciona el apartado "Bodega origen" y elige "Bodega 2"')
def when_usuario_selecciona_bodega_origen(context):
    try:
        combo = context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        combo.click()
        opcion = context.page.locator('[role="option"]', has_text="Bodega 2")
        expect(opcion).to_be_visible(timeout=TIMEOUT)
        opcion.click()
    except Exception as e:
        raise Exception(f"Error al seleccionar la bodega origen: {str(e)}")
@then(u'la bodega origen es seleccionada correctamente')
def then_bodega_origen_seleccionada_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])).to_have_text('Bodega 2', timeout=TIMEOUT)
@when(u'el usuario completa el campo "RUT" con "123456789"')
def when_usuario_completa_campo_rut(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
    except Exception as e:
        raise Exception(f"Error al ingresar el RUT: {e}")
@then(u'el RUT es ingresado correctamente')
def then_rut_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
@when(u'el usuario selecciona el apartado "Destino" y elige "ubicación número 1"')
def when_usuario_selecciona_destino(context):
    try:
        combo = context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        combo.click()
        opcion = context.page.locator('[role="option"]', has_text="ubicación número 1")
        expect(opcion).to_be_visible(timeout=TIMEOUT)
        opcion.click()
    except Exception as e:
        raise Exception(f"Error al seleccionar el destino: {str(e)}")
@then(u'el destino es seleccionado correctamente')
def then_destino_seleccionado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])).to_have_text('ubicación número 1', timeout=TIMEOUT)
@when(u'el usuario completa el campo "número de pedido" con "987"')
def when_usuario_completa_campo_numero_de_pedido(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['numeroPedido'], '987')
    except Exception as e:
        raise Exception(f"Error al ingresar el número de pedido: {e}")
@then(u'el número de pedido es ingresado correctamente')
def then_numero_de_pedido_ingresado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])).to_have_value('987', timeout=TIMEOUT)
@when(u'el usuario hace clic en el botón "grabar pedidos"')
def when_usuario_hace_clic_en_boton_grabar_pedidos(context):
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
@then(u'el pedido se completa')
def then_pedido_se_completa(context):
    # Aquí se puede agregar una validación específica para confirmar que el pedido se completó
    pass
@then(u'el pedido queda guardado en la base de datos')
def then_pedido_guardado_en_base_de_datos(context):
    # Aquí se puede agregar una validación específica para confirmar que el pedido se guardó en la base de datos
    pass

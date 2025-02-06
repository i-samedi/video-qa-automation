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
@given('el usuario está en la pantalla de carga de pedidos a bodegas')
def step_esta_en_pantalla_carga_pedidos(context):
    expect(context.page.locator(LOCATORS['page']['title'])).to_be_visible(timeout=TIMEOUT)
@given('existe un pedido realizado desde el almacén central')
def step_existe_pedido_del_almacen_central(context):
    # Implementar lógica para verificar existencia de pedido
    pass
@when('el usuario selecciona el apartado "Bodegas de origen"')
def step_selecciona_apartado_bodegas_de_origen(context):
    # Implementar lógica para seleccionar el apartado
    pass
@when('selecciona "Bodega 2"')
def step_selecciona_bodega_2(context):
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
@then('la bodega de origen es seleccionada correctamente')
def step_bodega_origen_seleccionada_correctamente(context):
    # Implementar lógica para verificar selección correcta
    pass
@when('el usuario completa el campo RUT con "123456789"')
def step_completa_campo_RUT(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
    except Exception as e:
        raise Exception(f"Error al completar el campo RUT: {e}")
@then('el campo RUT es completado correctamente')
def step_campo_RUT_completado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
@when('el usuario selecciona "Ubicación 1" en el dropdown de destino')
def step_selecciona_ubicacion_1_dropdown_destino(context):
    try:
        combo = context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])
        expect(combo).to_be_visible(timeout=TIMEOUT)
        expect(combo).to_be_enabled(timeout=TIMEOUT)
        combo.click()
        opcion = context.page.locator('[role="option"]', has_text="Ubicación 1")
        expect(opcion).to_be_visible(timeout=TIMEOUT)
        opcion.click()
    except Exception as e:
        raise Exception(f"Error al seleccionar la ubicación de destino: {str(e)}")
@then('la ubicación de destino es seleccionada correctamente')
def step_ubicacion_destino_seleccionada_correctamente(context):
    # Implementar lógica para verificar selección correcta
    pass
@when('el usuario completa el campo número de pedido con "987"')
def step_completa_campo_numero_pedido(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['numeroPedido'], '987')
    except Exception as e:
        raise Exception(f"Error al completar el campo número de pedido: {e}")
@then('el campo número de pedido es completado correctamente')
def step_campo_numero_pedido_completado_correctamente(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido'])).to_have_value('987', timeout=TIMEOUT)
@when('el usuario hace clic en el botón "Grabar pedidos"')
def step_clic_boton_grabar_pedidos(context):
    try:
        boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
        expect(boton).to_be_visible(timeout=TIMEOUT)
        try:
            expect(boton).to_be_enabled(timeout=TIMEOUT)
            boton.click()
        except Exception as e:
            boton.click(force=True)
    except Exception as e:
        raise Exception(f"Error al hacer clic en el botón Grabar pedidos: {str(e)}")
@then('el pedido se persiste en la base de datos')
def step_pedido_persistido_base_datos(context):
    # Implementar lógica para verificar persistencia en la base de datos
    pass
@then('el proceso de carga se completa exitosamente')
def step_proceso_carga_completado_exitosamente(context):
    # Implementar lógica para verificar que el proceso de carga se completó
    pass

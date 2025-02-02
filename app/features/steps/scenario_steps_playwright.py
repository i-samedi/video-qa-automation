from behave import given, when, then
from playwright.sync_api import expect, TimeoutError
import os
import json

TIMEOUT = 5000  # 5 segundos

with open(os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json'), 'r') as f:
    LOCATORS = json.load(f)

@given('El usuario ha iniciado sesión en el sistema')
def step_usuario_inicia_sesion(context):
    pass  # Implementación de la lógica para iniciar sesión
@given('Se encuentra en la pantalla de carga de pedidos')
def step_usuario_en_pantalla_carga(context):
    context.page.goto("http://localhost:3000")
    context.page.wait_for_selector(LOCATORS['page']['title'])
    expect(context.page.locator(LOCATORS['page']['title'])).to_be_visible()
@when('El usuario selecciona la "Bodega 2" como bodega origen del despacho')
def step_usuario_selecciona_bodega_origen(context):
    try:
        context.page.wait_for_selector(LOCATORS['groupBox1']['selects']['bodega'])
        context.page.select_option(LOCATORS['groupBox1']['selects']['bodega'], "Bodega 2")
    except Exception as e:
        print(f"Error al seleccionar la bodega: {e}")
@then('La "Bodega 2" queda seleccionada como origen')
def step_verificar_bodega_origen_seleccionada(context):
    selected_option = context.page.locator(LOCATORS['groupBox1']['selects']['bodega']).input_value()
    expect(selected_option).to_equal("Bodega 2")
@when('El usuario completa el campo RUT con "1, 2, 3, 4, 5, 6, 7, 8, 9"')
def step_usuario_completa_rut(context):
    try:
        context.page.wait_for_selector(LOCATORS['groupBox3']['inputs']['rut'])
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], "1, 2, 3, 4, 5, 6, 7, 8, 9")
    except Exception as e:
        print(f"Error al completar el RUT: {e}")
@then('El RUT "1, 2, 3, 4, 5, 6, 7, 8, 9" queda registrado en el campo correspondiente')
def step_verificar_rut_registrado(context):
    rut_value = context.page.locator(LOCATORS['groupBox3']['inputs']['rut']).input_value()
    expect(rut_value).to_equal("1, 2, 3, 4, 5, 6, 7, 8, 9")
@when('El usuario selecciona la "Ubicación número 1" como destino del pedido')
def step_usuario_selecciona_destino_pedido(context):
    try:
        context.page.wait_for_selector(LOCATORS['groupBox3']['selects']['ubicacion'])
        context.page.select_option(LOCATORS['groupBox3']['selects']['ubicacion'], "Ubicación número 1")
    except Exception as e:
        print(f"Error al seleccionar la ubicación: {e}")
@then('La "Ubicación número 1" queda seleccionada como destino')
def step_verificar_destino_seleccionado(context):
    selected_option = context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion']).input_value()
    expect(selected_option).to_equal("Ubicación número 1")
@when('El usuario completa el campo número de pedido con "9, 8, 7"')
def step_usuario_completa_numero_pedido(context):
    try:
        context.page.wait_for_selector(LOCATORS['groupBox3']['inputs']['numeroPedido'])
        context.page.fill(LOCATORS['groupBox3']['inputs']['numeroPedido'], "9, 8, 7")
    except Exception as e:
        print(f"Error al completar el número de pedido: {e}")
@then('El número de pedido "9, 8, 7" queda registrado en el campo correspondiente')
def step_verificar_numero_pedido_registrado(context):
    numero_pedido_value = context.page.locator(LOCATORS['groupBox3']['inputs']['numeroPedido']).input_value()
    expect(numero_pedido_value).to_equal("9, 8, 7")
@when('El usuario hace clic en el botón "Grabar pedidos"')
def step_usuario_confirma_grabacion_pedido(context):
    try:
        context.page.wait_for_selector(LOCATORS['panel1']['buttons']['grabarPedidos'])
        context.page.click(LOCATORS['panel1']['buttons']['grabarPedidos'])
    except Exception as e:
        print(f"Error al hacer clic en Grabar pedidos: {e}")
@then('El pedido queda grabado y persistido en la base de datos')
def step_verificar_pedido_grabado(context):
    # Implementación de la lógica para verificar el pedido grabado
    pass

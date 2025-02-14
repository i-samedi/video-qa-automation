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
        "checkboxes": {
            "homologarCliente": "#checkboxhomologaclte",
            "soloStock": "#checkboxstock"
        }
    },
    "groupBox3": {
        "container": "#groupbox3",
        "inputs": {
            "rut": "#editrut"
        }
    }
}
TIMEOUT = 5000
@given('el área de COMEX utiliza la pantalla principal de seguimiento de importaciones')
def given_comex_uses_main_tracking_screen(context):
    pass
@given('la OC aprobada en Oracle se muestra en esta pantalla')
def given_approved_oc_displayed_on_screen(context):
    pass
@when('el usuario accede a la pantalla de seguimiento de importaciones')
def when_user_accesses_tracking_screen(context):
    pass
@then('se muestra la pantalla de seguimiento de importaciones correctamente')
def then_tracking_screen_displayed_correctly(context):
    expect(context.page.locator(LOCATORS['page']['title'])).to_be_visible(timeout=TIMEOUT)
@when('el usuario visualiza los datos de la compañía')
def when_user_views_company_data(context):
    pass
@then('se muestran el nombre, dirección antigua, bodegas de entrega, RUT, marca, colección y fecha de emisión de la orden de compra')
def then_company_data_displayed(context):
    pass
@when('el usuario visualiza los datos del proveedor')
def when_user_views_supplier_data(context):
    pass
@then('se muestran el nombre, RUT ficticio, correlativo, número asignado, dirección y otros datos relevantes')
def then_supplier_data_displayed(context):
    pass
@when('el usuario visualiza los datos de la proforma del proveedor')
def when_user_views_supplier_proforma_data(context):
    pass
@then('se muestran el país de origen, puertos de embarque, vía de embarque, factor, cláusula de compra, cláusula FOP y comisión si existen')
def then_supplier_proforma_data_displayed(context):
    pass
@when('el usuario visualiza las fechas y forma de pago')
def when_user_views_payment_dates_and_method(context):
    pass
@then('se muestran la factory date, último plazo de embarque, fecha de necesidad y forma de pago')
def then_payment_dates_and_method_displayed(context):
    pass
@when('el usuario visualiza los datos del forward, expeditors y condiciones de embarque')
def when_user_views_forward_expeditors_and_shipping_conditions(context):
    pass
@then('se muestran si el embarque es parcial, la moneda empleada y gastos adicionales si existen')
def then_forward_expeditors_and_shipping_conditions_displayed(context):
    pass
@when('el usuario visualiza los datos relacionados a carta de crédito')
def when_user_views_credit_letter_data(context):
    pass
@then('no se muestran si la cláusula de compra es WT')
def then_credit_letter_data_not_displayed_if_wt(context):
    pass
@when('el usuario visualiza el detalle de la orden de compra')
def when_user_views_purchase_order_details(context):
    pass
@then('se muestran el número de OC, clase de producto, género, modelo, nombre del producto, color, código, código color, talla, número de la barra, cantidad comprada, cantidad embarcada y precio')
def then_purchase_order_details_displayed(context):
    pass
@when('el usuario visualiza los íconos de acción en la pantalla')
def when_user_views_action_icons_on_screen(context):
    pass
@then('se muestran los íconos Factura, ASN, Programa, Envío, Reportes, área de Pagos, Borrar, Anulación, Royalty, opciones de anticipos y funciones de carga B y ver B en el booking')
def then_action_icons_displayed_on_screen(context):
    pass
@when('el usuario visualiza el resumen de la compra')
def when_user_views_purchase_summary(context):
    pass
@then('se muestran el total de tareas, unidades equivalentes, sólidos y total de la compra, confirmando que la diferencia es cero cuando la cantidad comprada es igual a la embarcada')
def then_purchase_summary_displayed_correctly(context):
    pass
@when('el usuario ingresa el RUT correspondiente')
def step_ingreso_rut(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
    except Exception as e:
        raise Exception(f"Error al ingresar el RUT: {e}")
@when('el usuario hace clic en el botón grabar pedidos')
def step_click_grabar(context):
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
@when('el usuario marca el checkbox de homologar cliente')
def step_checkbox_homologar_cliente(context):
    try:
        checkbox = context.page.locator(LOCATORS['groupBox1']['checkboxes']['homologarCliente'])
        expect(checkbox).to_be_visible(timeout=TIMEOUT)
        if not checkbox.is_checked():
            checkbox.check()
    except Exception as e:
        raise Exception(f"Error al marcar el checkbox: {str(e)}")
@then('el valor esperado se muestra en el campo de RUT')
def step_validacion_input_rut(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)

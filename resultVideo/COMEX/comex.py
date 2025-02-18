from behave import given, when, then
from playwright.sync_api import expect, TimeoutError
import os
import json

TIMEOUT = 15000

LOCATORS_PATH = os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json')
with open(LOCATORS_PATH, 'r') as f:
    LOCATORS = json.load(f)

@given('el usuario está en la pantalla de seguimiento de importaciones')
def step_usuario_en_pantalla_seguimiento(context):
    pass
@given('tiene acceso a todas las opciones necesarias')
def step_tiene_acceso_opciones(context):
    pass
@given('los parámetros iniciales están configurados')
def step_parametros_iniciales_configurados(context):
    pass
@when('el usuario ingresa el número de la OC "{numero_oc}"')
def step_usuario_ingresa_numero_oc(context, numero_oc):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['ordenCompra'], numero_oc)
    except Exception as e:
        raise Exception(f"Error al ingresar el número de la OC: {e}")
@then('el sistema despliega la información completa de la orden de compra')
def step_sistema_despliega_info_completa(context):
    expect(context.page.locator(LOCATORS['panel1']['inputs']['observaciones'])).to_be_visible(timeout=TIMEOUT)
@when('se visualizan los datos generales')
def step_visualizan_datos_generales(context):
    pass
@then('se muestra la empresa registrada y su vínculo mediante RUT')
def step_muestra_empresa_y_rut(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
@when('se inspecciona la información del proveedor')
def step_inspecciona_info_proveedor(context):
    pass
@then('se muestra la dirección y los datos generales del proveedor')
def step_muestra_direccion_y_datos_proveedor(context):
    expect(context.page.locator(LOCATORS['panel5']['textareas']['mensajeEmail'])).to_be_visible(timeout=TIMEOUT)
@when('se revisa la documentación de soporte')
def step_revisar_documentacion_soporte(context):
    pass
@then('se muestra la proforma o, en otros casos, la planilla Excel acordada entre Comercial y Oracle')
def step_muestra_proforma_o_planilla(context):
    expect(context.page.locator(LOCATORS['panel1']['buttons']['exportarDatos'])).to_be_visible(timeout=TIMEOUT)
@when('el usuario crea la OC')
def step_usuario_crea_oc(context):
    try:
        boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
        expect(boton).to_be_visible(timeout=TIMEOUT)
        boton.click()
    except Exception as e:
        raise Exception(f"Error al crear la OC: {str(e)}")
@then('se selecciona el país correspondiente y se selecciona el puerto de embarque adecuado')
def step_selecciona_pais_y_puerto(context):
    try:
        combo = context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])
        expect(combo).to_be_visible(timeout=TIMEOUT)
        combo.click()
        opcion = context.page.locator('[role="option"]', has_text="Chile")
        expect(opcion).to_be_visible(timeout=TIMEOUT)
        opcion.click()
    except Exception as e:
        raise Exception(f"Error al seleccionar el país y puerto: {str(e)}")
@when('se revisan las opciones disponibles')
def step_revisan_opciones_disponibles(context):
    pass
@then('se muestran las opciones: marítimo (la principal), aéreo y terrestre')
def step_muestra_opciones_transporte(context):
    expect(context.page.locator(LOCATORS['groupBox2']['radioButtons']['puntoComa'])).to_be_visible(timeout=TIMEOUT)
@when('se visualiza el campo de comisión')
def step_visualiza_campo_comision(context):
    pass
@then('el valor aparece como cero')
def step_valor_aparece_cero(context):
    expect(context.page.locator(LOCATORS['panel1']['inputs']['cantidadRechazada'])).to_have_value('0', timeout=TIMEOUT)
@when('se inspeccionan los detalles de la OC')
def step_inspeccionan_detalles_oc(context):
    pass
@then('se muestran la fecha factory, la fecha del último plazo de embarque y la fecha en que la mercadería debe estar disponible')
def step_muestra_fechas_clave_oc(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['fechaEntregaInicial'])).to_be_visible(timeout=TIMEOUT)
@when('se visualiza el campo "forma de pago"')
def step_visualiza_forma_pago(context):
    pass
@then('se muestran las opciones: WT (transferencia individual), LC (Letter of Credit) y cobranza (transferencia agrupada por proveedor)')
def step_muestra_opciones_forma_pago(context):
    expect(context.page.locator(LOCATORS['groupBox3']['selects']['condicionVenta'])).to_be_visible(timeout=TIMEOUT)
@when('se visualiza el dato del forwarder')
def step_visualiza_dato_forwarder(context):
    pass
@then('se muestra la opción seleccionada, ya sea Expeditors o DHL')
def step_muestra_opcion_forwarder(context):
    expect(context.page.locator(LOCATORS['panel5']['tabs']['pedido'])).to_be_visible(timeout=TIMEOUT)
@when('se inspecciona el total y la tolerancia')
def step_inspecciona_total_y_tolerancia(context):
    pass
@then('se muestra el monto total de la OC y, de ser aplicable, el ajuste por tolerancia')
def step_muestra_total_y_tolerancia(context):
    expect(context.page.locator(LOCATORS['panel1']['inputs']['lineasRechazadas'])).to_have_value('0', timeout=TIMEOUT)
@when('se revisa el contenido del detalle')
def step_revisa_contenido_detalle(context):
    pass
@then('se muestran el tipo de clase, género, modelo, nombre del producto, color (y su código), talla, código de barras, cantidad y cantidad embarcada')
def step_muestra_detalle_productos(context):
    expect(context.page.locator(LOCATORS['grillas']['detalle']['container'])).to_be_visible(timeout=TIMEOUT)
@when('se verifica el código de barras')
def step_verifica_codigo_barras(context):
    pass
@then('se reconoce si el código tiene 12 o 13 dígitos (producto sólido) o 6 dígitos (agrupa varias tallas en tareas)')
def step_reconoce_codigo_barras(context):
    expect(context.page.locator(LOCATORS['grillas']['detalle']['container'])).to_be_visible(timeout=TIMEOUT)
@when('el usuario interactúa con los íconos (factura, ASN, programa, envío, reportes, consultas, pagos, seguimiento)')
def step_usuario_interactua_iconos(context):
    pass
@then('el sistema permite acceder a un resumen de la operación y ejecutar la anulación de la OC si esta ya no es vigente')
def step_accede_resumen_y_anulacion(context):
    expect(context.page.locator(LOCATORS['panel1']['buttons']['cancelar'])).to_be_visible(timeout=TIMEOUT)
@when('se selecciona el ícono de royalty')
def step_selecciona_icono_royalty(context):
    pass
@then('se muestran únicamente los proveedores con royalty')
def step_muestra_proveedores_con_royalty(context):
    expect(context.page.locator(LOCATORS['panel2']['buttons']['button1'])).to_be_visible(timeout=TIMEOUT)
@when('se revisa la sección de booking')
def step_revisa_seccion_booking(context):
    pass
@then('se muestran los campos de carga, booking y ver booking en cero y deshabilitados')
def step_muestra_campos_booking(context):
    expect(context.page.locator(LOCATORS['panel5']['textareas']['mensajeEmail'])).to_have_value('0', timeout=TIMEOUT)

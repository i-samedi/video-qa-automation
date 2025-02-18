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
    "groupBox3": {
        "container": "#groupbox3",
        "inputs": {
            "ordenCompra": "#editoc"
        }
    }
}
TIMEOUT = 5000
@given('el usuario está en la pantalla de seguimiento de importaciones')
def given_usuario_en_pantalla_seguimiento(context):
    pass
@given('tiene acceso a todas las opciones necesarias')
def given_usuario_tiene_acceso_opciones(context):
    pass
@given('los parámetros iniciales están configurados')
def given_parametros_iniciales_configurados(context):
    pass
@when('el usuario ingresa una orden de compra con número "425376"')
def when_ingresar_orden_de_compra(context):
    try:
        context.page.fill(LOCATORS['groupBox3']['inputs']['ordenCompra'], '425376')
    except Exception as e:
        raise Exception(f"Error al ingresar la orden de compra: {e}")
@then('se despliega toda la información asociada a la OC')
def then_desplegar_informacion_oc(context):
    # Aquí se debería implementar la lógica para validar que la información se despliega correctamente
    pass
@when('el usuario observa los datos de empresa, destinos, proveedores y proforma o planilla Excel')
def when_observar_datos_empresa(context):
    # Aquí se debería implementar la lógica para observar los datos
    pass
@then('se muestran los detalles completos para respaldar la compra')
def then_mostrar_detalles_respaldo(context):
    # Aquí se debería implementar la lógica para validar que los detalles se muestran correctamente
    pass
@when('el usuario selecciona el país de origen, el puerto de embarque y la vía (por ejemplo, marítimo)')
def when_seleccionar_datos_embarque(context):
    # Aquí se debería implementar la lógica para seleccionar los datos de embarque
    pass
@then('se calcula un factor sobre el precio para estimar el costo de poner la mercadería en destino')
def then_calcular_costo_destino(context):
    # Aquí se debería implementar la lógica para calcular el costo
    pass
@when('se muestra la sección con WP, LC (Letter of Credit), cobranza y WT')
def when_mostrar_seccion_pagos(context):
    # Aquí se debería implementar la lógica para mostrar la sección de pagos
    pass
@then('se visualizan las opciones de pago y el forwarder (por ejemplo, Expeditors o THL)')
def then_visualizar_opciones_pago(context):
    # Aquí se debería implementar la lógica para visualizar las opciones de pago
    pass
@when('el usuario observa la clase, género, modelo, color, talla, código de barra, cantidad y precio')
def when_observar_detalles_productos(context):
    # Aquí se debería implementar la lógica para observar los detalles de los productos
    pass
@then('se distinguen los productos comprados por “sólido” (una talla por SKU) o “tarea” (agrupación de tallas)')
def then_distinguir_productos_comprados(context):
    # Aquí se debería implementar la lógica para distinguir los productos
    pass
@when('el usuario accede al icono ASN desde la OC')
def when_acceder_icono_asn(context):
    # Aquí se debería implementar la lógica para acceder al icono ASN
    pass
@then('se muestra un resumen de los productos embarcados y el total de cantidades')
def then_mostrar_resumen_productos_embarcados(context):
    # Aquí se debería implementar la lógica para mostrar el resumen de productos
    pass
@when('el usuario presiona Enter sobre el VL')
def when_presionar_enter_vl(context):
    # Aquí se debería implementar la lógica para presionar Enter sobre el VL
    pass
@then('se despliegan las facturas emitidas por el proveedor')
def then_desplegar_facturas_proveedor(context):
    # Aquí se debería implementar la lógica para desplegar las facturas
    pass
@then('se muestran los montos facturados y las diferencias comparados con la OC')
def then_mostrar_montos_y_diferencias(context):
    # Aquí se debería implementar la lógica para mostrar los montos y diferencias
    pass
@when('el usuario ingresa el número de contenedor o VL')
def when_ingresar_numero_contenedor(context):
    # Aquí se debería implementar la lógica para ingresar el número de contenedor o VL
    pass
@then('se muestra la información de programación (incluyendo fechas estimadas y confirmadas)')
def then_mostrar_informacion_programacion(context):
    # Aquí se debería implementar la lógica para mostrar la información de programación
    pass
@then('se visualizan datos del centro de distribución, cantidades, estatus y modalidad de retiro')
def then_visualizar_datos_distribucion(context):
    # Aquí se debería implementar la lógica para visualizar los datos de distribución
    pass
@when('el usuario filtra por contenedor, VL, marca, clase, o define un rango de fechas')
def when_filtrar_informacion_oc(context):
    # Aquí se debería implementar la lógica para filtrar la información
    pass
@then('se genera un reporte resumido o detallado de la OC')
def then_generar_reporte_oc(context):
    # Aquí se debería implementar la lógica para generar el reporte
    pass
@then('se permite descargar el reporte en formato Excel')
def then_permitir_descargar_reporte_excel(context):
    # Aquí se debería implementar la lógica para permitir la descarga del reporte
    pass
@when('el usuario modifica las fechas u otros datos y graba los cambios')
def when_modificar_y_grabar_cambios_oc(context):
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
@then('se actualiza la información de la OC en pantalla')
def then_actualizar_informacion_oc(context):
    # Aquí se debería implementar la lógica para actualizar la información
    pass
@when('el usuario selecciona eliminar una invoice o anular una OC utilizando la clave de validación')
def when_eliminar_o_anular_informacion(context):
    # Aquí se debería implementar la lógica para eliminar o anular la información
    pass
@then('se elimina o anula la información de forma parcial o completa')
def then_eliminar_o_anular_informacion(context):
    # Aquí se debería implementar la lógica para eliminar o anular la información
    pass
@when('el usuario ingresa el valor a pagar y se aplica la retención correspondiente')
def when_ingresar_valor_y_aplicar_retencion(context):
    # Aquí se debería implementar la lógica para ingresar el valor y aplicar la retención
    pass
@then('se muestra el detalle de los pagos y se genera un reporte para Royalty')
def then_mostrar_detalle_pagos_y_reporte(context):
    # Aquí se debería implementar la lógica para mostrar el detalle de pagos y generar el reporte
    pass

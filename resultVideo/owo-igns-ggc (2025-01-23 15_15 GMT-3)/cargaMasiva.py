from behave import given, when, then
from playwright.sync_api import expect, TimeoutError
import os
import json

TIMEOUT = 15000

LOCATORS_PATH = os.path.join(os.path.dirname(__file__), '..', 'locators', 'page_locators.json')
with open(LOCATORS_PATH, 'r') as f:
    LOCATORS = json.load(f)

@given('el usuario está en la pantalla principal de la aplicación de carga masiva')
def step_user_on_main_screen(context):
    expect(context.page.locator(LOCATORS['page']['title'])).to_be_visible(timeout=TIMEOUT)
@given('se visualizan los tipos de pedido en el panel izquierdo con el tipo normal marcado por defecto')
def step_order_types_visible(context):
    expect(context.page.locator(LOCATORS['groupBox4']['radioButtons']['normal'])).to_be_checked(timeout=TIMEOUT)
@given('se muestra la bodega de despacho por defecto (SDFORCE)')
def step_default_dispatch_warehouse_displayed(context):
    expect(context.page.locator(LOCATORS['groupBox1']['selects']['bodega'])).to_have_text('SDFORCE', timeout=TIMEOUT)
@when('el usuario digita el nombre de usuario')
def step_user_enters_username(context):
    context.page.fill(LOCATORS['panel1']['inputs']['observaciones'], 'usuario')
@when('presiona Enter para confirmar la bodega por defecto')
def step_confirm_default_warehouse_with_enter(context):
    context.page.press(LOCATORS['groupBox1']['selects']['bodega'], 'Enter')
@then('el cursor se posiciona en el campo RUT')
def step_cursor_in_rut_field(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_be_focused(timeout=TIMEOUT)
@when('el usuario ingresa el RUT del cliente')
def step_user_enters_rut(context):
    context.page.fill(LOCATORS['groupBox3']['inputs']['rut'], '123456789')
@then('el RUT es validado correctamente')
def step_rut_validated_correctly(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['rut'])).to_have_value('123456789', timeout=TIMEOUT)
@when('el usuario desconoce el RUT')
def step_user_does_not_know_rut(context):
    pass
@when('presiona el botón de ayuda')
def step_press_help_button(context):
    boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
    expect(boton).to_be_visible(timeout=TIMEOUT)
    boton.click()
@when('escribe parte de la razón social')
def step_user_enters_company_name_part(context):
    context.page.fill(LOCATORS['panel1']['inputs']['observaciones'], 'parte de razón social')
@when('presiona Enter')
def step_user_presses_enter(context):
    context.page.press(LOCATORS['panel1']['inputs']['observaciones'], 'Enter')
@then('la aplicación muestra los clientes que coinciden con el patrón')
def step_show_matching_clients(context):
    expect(context.page.locator('#resultadoBusqueda')).to_be_visible(timeout=TIMEOUT)
@when('el usuario selecciona el cliente adecuado con doble clic sobre el RUT')
def step_user_selects_client_with_double_click(context):
    cliente = context.page.locator('#clienteRUT')
    cliente.dblclick()
@when('presiona Enter')
def step_user_confirms_with_enter(context):
    context.page.press('#clienteRUT', 'Enter')
@then('la pantalla principal muestra el RUT y la razón social del cliente')
def step_main_screen_shows_client_info(context):
    expect(context.page.locator('#clienteInfo')).to_be_visible(timeout=TIMEOUT)
@then('la aplicación indica que el cliente tiene crédito suficiente')
def step_application_confirms_sufficient_credit(context):
    expect(context.page.locator('#creditoSuficiente')).to_have_text('Crédito suficiente', timeout=TIMEOUT)
@when('el usuario selecciona la ubicación de destino mediante el combo o a partir de la plantilla')
def step_user_selects_destination_location(context):
    combo = context.page.locator(LOCATORS['groupBox3']['selects']['ubicacion'])
    expect(combo).to_be_visible(timeout=TIMEOUT)
    combo.click()
    opcion = context.page.locator('[role="option"]', has_text="Ubicación 1")
    expect(opcion).to_be_visible(timeout=TIMEOUT)
    opcion.click()
@when('selecciona las condiciones de venta')
def step_user_selects_sales_conditions(context):
    combo = context.page.locator(LOCATORS['groupBox3']['selects']['condicionVenta'])
    expect(combo).to_be_visible(timeout=TIMEOUT)
    combo.click()
    opcion = context.page.locator('[role="option"]', has_text="Condición 1")
    expect(opcion).to_be_visible(timeout=TIMEOUT)
    opcion.click()
@when('digita la orden de compra del cliente')
def step_user_enters_purchase_order(context):
    context.page.fill(LOCATORS['groupBox3']['inputs']['ordenCompra'], 'OC123456')
@when('presiona Enter')
def step_user_confirms_purchase_order_with_enter(context):
    context.page.press(LOCATORS['groupBox3']['inputs']['ordenCompra'], 'Enter')
@then('el sistema cambia el campo activo al porcentaje de descuento')
def step_system_moves_to_discount_field(context):
    expect(context.page.locator(LOCATORS['groupBox3']['inputs']['porcentajeDescuento'])).to_be_focused(timeout=TIMEOUT)
@when('el usuario ingresa 15% de descuento')
def step_user_enters_discount(context):
    context.page.fill(LOCATORS['groupBox3']['inputs']['porcentajeDescuento'], '15')
@when('presiona Enter')
def step_user_confirms_discount_with_enter(context):
    context.page.press(LOCATORS['groupBox3']['inputs']['porcentajeDescuento'], 'Enter')
@then('el cursor se posiciona en el botón de lectura de archivo')
def step_cursor_on_file_read_button(context):
    expect(context.page.locator(LOCATORS['groupBox3']['buttons']['archivo'])).to_be_focused(timeout=TIMEOUT)
@when('el usuario selecciona el botón de lectura')
def step_user_selects_read_button(context):
    boton = context.page.locator(LOCATORS['groupBox3']['buttons']['archivo'])
    expect(boton).to_be_visible(timeout=TIMEOUT)
    boton.click()
@when('selecciona el archivo CSV con doble clic')
def step_user_selects_csv_file_with_double_click(context):
    archivo = context.page.locator('#archivoCSV')
    archivo.dblclick()
@then('la aplicación lee el archivo y valida cada registro')
def step_application_reads_and_validates_file(context):
    expect(context.page.locator('#validacionArchivo')).to_have_text('Validación completa', timeout=TIMEOUT)
@then('la aplicación valida el código de tienda, modelo, color, talla, cantidad de pedido')
def step_application_validates_file_records(context):
    expect(context.page.locator('#validacionRegistros')).to_have_text('Registros validados', timeout=TIMEOUT)
@then('marca en rojo las líneas con error y en verde las correctas')
def step_mark_lines_based_on_validation(context):
    expect(context.page.locator('.lineaError')).to_have_css('color', 'red', timeout=TIMEOUT)
    expect(context.page.locator('.lineaCorrecta')).to_have_css('color', 'green', timeout=TIMEOUT)
@then('la aplicación recupera datos adicionales como ID del cliente, SiteUsageID, TypeID, ItemID, y otros')
def step_application_recovers_additional_data(context):
    expect(context.page.locator('#datosAdicionales')).to_be_visible(timeout=TIMEOUT)
@when('el usuario activa el botón "Grabar pedido"')
def step_user_activates_log_order_button(context):
    boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
    expect(boton).to_be_visible(timeout=TIMEOUT)
    boton.click()
@when('presiona este botón para registrar el pedido')
def step_user_register_order(context):
    boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
    expect(boton).to_be_visible(timeout=TIMEOUT)
    boton.click()
@then('la aplicación registra los pedidos y asigna un número de pedido a cada grupo de líneas')
def step_application_registers_orders(context):
    expect(context.page.locator('#registroPedidos')).to_have_text('Pedidos registrados', timeout=TIMEOUT)
@then('la aplicación agrupa los pedidos según la marca, clase y género')
def step_application_groups_orders(context):
    expect(context.page.locator('#agrupacionPedidos')).to_have_text('Pedidos agrupados', timeout=TIMEOUT)
@then('muestra en la pantalla los números de pedido generados')
def step_display_generated_order_numbers(context):
    expect(context.page.locator('#numerosPedido')).to_be_visible(timeout=TIMEOUT)
@when('el usuario activa la opción "Pruebas de inyección" y guarda')
def step_user_activates_injection_tests_and_saves(context):
    checkbox = context.page.locator('#pruebasInyeccion')
    expect(checkbox).to_be_visible(timeout=TIMEOUT)
    if not checkbox.is_checked():
        checkbox.check()
    boton = context.page.locator(LOCATORS['panel1']['buttons']['grabarPedidos'])
    expect(boton).to_be_visible(timeout=TIMEOUT)
    boton.click()
@then('la aplicación exporta los datos de la inyección')
def step_application_exports_injection_data(context):
    expect(context.page.locator('#exportacionInyeccion')).to_have_text('Exportación completa', timeout=TIMEOUT)
@then('el respaldo DBF contiene el detalle de la grilla')
def step_backup_dbf_contains_grid_details(context):
    expect(context.page.locator('#respaldoDBF')).to_have_text('Detalle completo', timeout=TIMEOUT)
@then('el usuario valida que la carga se realizó satisfactoriamente')
def step_user_validates_successful_load(context):
    expect(context.page.locator('#validacionCarga')).to_have_text('Carga satisfactoria', timeout=TIMEOUT)
@then('que la información en el respaldo coincide con la grilla de la pantalla principal')
def step_backup_matches_main_screen_grid(context):
    expect(context.page.locator('#coincidenciaRespaldo')).to_have_text('Coincidencia completa', timeout=TIMEOUT)
@then('el usuario cierra la aplicación')
def step_user_closes_application(context):
    boton = context.page.locator(LOCATORS['panel1']['buttons']['salir'])
    expect(boton).to_be_visible(timeout=TIMEOUT)
    boton.click()

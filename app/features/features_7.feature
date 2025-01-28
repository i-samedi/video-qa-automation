Scenario: Validación de cliente y registro de pedidos en el sistema RPI
   Given que la aplicación está abierta en la pantalla de validación de clientes
   And el cliente "SOCiedad Comercial Valcao" está registrado en el maestro de clientes del RPI
   When el usuario revisa los detalles del cliente
   And verifica la información como SiteUsageID para la dirección de envío y facturación
   Then el sistema debe mostrar correctamente el TypeID, ItemID y la unidad de medida "UND"
   And debe permitir al usuario grabar o cancelar el pedido según la configuración establecida
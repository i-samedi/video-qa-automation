'use client'

import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

export default function GroupBox4() {
  return (
    <div className="rounded-lg border p-4" id="groupbox4">
      <h3 className="mb-4 text-lg font-medium">Tipo Pedido</h3>
      <RadioGroup defaultValue="normal" className="space-y-2">
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="normal" id="rbnormal" />
          <label htmlFor="rbnormal" className="font-bold">
            Normal
          </label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="apertura" id="rbapertura" />
          <label htmlFor="rbapertura">Apertura Tienda</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="llenado" id="rbllenado" />
          <label htmlFor="rbllenado">Llenado Canal</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="cross" id="rbcross" />
          <label htmlFor="rbcross">Cross Docking</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="nocol" id="rbnocol" />
          <label htmlFor="rbnocol">No Colección</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="acc" id="rbacc" />
          <label htmlFor="rbacc">Accesorios</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="rt" id="rbrt" />
          <label htmlFor="rbrt">Colegio</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="foto" id="rbfoto" />
          <label htmlFor="rbfoto">Fotografia</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="vtaec" id="rbvtaec" />
          <label htmlFor="rbvtaec">Venta Ecommerce</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="campana" id="rbcampana" />
          <label htmlFor="rbcampana">Campaña</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="reserva" id="rbreserva" />
          <label htmlFor="rbreserva">Reservar STOCK</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem
            value="stockreservado"
            id="rbstockreservado"
            disabled
          />
          <label htmlFor="rbstockreservado">STOCK Reservado</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="traspasowhs" id="rbtraspasowhs" />
          <label htmlFor="rbtraspasowhs">Tra. ForusBee WH</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="desarme" id="rbdesarme" disabled />
          <label htmlFor="rbdesarme">Desarme Tareas</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="regula" id="rbregula" disabled />
          <label htmlFor="rbregula">Regularización</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="consigna" id="rbconsigna" />
          <label htmlFor="rbconsigna">Consignación</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="repoas" id="rbrepoas" />
          <label htmlFor="rbrepoas">Reposicion AS</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="llenadoas" id="rbllenadoas" />
          <label htmlFor="rbllenadoas">Lllenado Canal AS</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="carrito" id="rbcarrito" />
          <label htmlFor="rbcarrito">Carrito AS</label>
        </div>
      </RadioGroup>
    </div>
  )
}

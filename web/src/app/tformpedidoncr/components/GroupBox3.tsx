'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import GroupBox2 from './GroupBox2'

export default function GroupBox3() {
  return (
    <div className="space-y-4 rounded-lg border p-4" id="groupbox3">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="editrut">RUT</label>
          <Input id="editrut" />
        </div>
        <div>
          <label htmlFor="editcliente">Razón Social</label>
          <Input id="editcliente" readOnly />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <label htmlFor="comboubicacion">Ubicación Destino</label>
          <Select id="comboubicacion">
            <SelectTrigger>
              <SelectValue placeholder="Seleccione ubicación" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1">Ubicación 1</SelectItem>
              <SelectItem value="2">Ubicación 2</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div>
          <label htmlFor="combocondicionventa">Condiciones Venta</label>
          <Select id="combocondicionventa">
            <SelectTrigger>
              <SelectValue placeholder="Seleccione condición" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1">Condición 1</SelectItem>
              <SelectItem value="2">Condición 2</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="grid grid-cols-3 gap-2">
          <div>
            <label htmlFor="editoc">O.C.</label>
            <Input id="editoc" />
          </div>
          <div>
            <label htmlFor="editpordcto">% Dcto.</label>
            <Input id="editpordcto" disabled />
          </div>
          <div>
            <label htmlFor="editnropedido">Nro Pedido</label>
            <Input id="editnropedido" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <Input type="date" id="fechaentinicial" />
        <Input type="date" id="fechaentfinal" />
        <Input type="date" id="fechaexpiracion" />
      </div>

      <GroupBox2 />

      <Button id="botonarchivo" variant="outline" disabled>
        Archivos (DBF, CSV)
      </Button>
    </div>
  )
}

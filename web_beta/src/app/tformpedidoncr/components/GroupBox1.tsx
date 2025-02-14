'use client'

import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export default function GroupBox1() {
  return (
    <div className="rounded-lg border p-4" id="groupbox1">
      <h3 className="mb-4 text-lg font-medium">Origen Despacho</h3>
      <div className="space-y-4">
        <Select id="combobodega">
          <SelectTrigger className="w-[280px]">
            <SelectValue placeholder="Seleccione bodega" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="1">Bodega 1</SelectItem>
            <SelectItem value="2">Bodega 2</SelectItem>
          </SelectContent>
        </Select>

        <div className="flex items-center space-x-4">
          <Checkbox id="checkboxhomologaclte" />
          <label htmlFor="checkboxhomologaclte">
            Homologar Ubicacion Cliente
          </label>
        </div>

        <div className="flex items-center space-x-4">
          <Checkbox id="checkboxstock" defaultChecked />
          <label htmlFor="checkboxstock">Solo C/Stock</label>
        </div>

        <Button id="botonstock" variant="outline" disabled>
          Asignar STOCK
        </Button>
      </div>
    </div>
  )
}

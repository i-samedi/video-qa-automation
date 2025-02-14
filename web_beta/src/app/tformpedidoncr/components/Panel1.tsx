'use client'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import GroupBox1 from './GroupBox1'
import GroupBox3 from './GroupBox3'
import GroupBox4 from './GroupBox4'

export default function Panel1() {
  return (
    <div className="border-b p-4" id="panel1">
      <div className="flex gap-4">
        <GroupBox4 />
        <div className="flex-1 space-y-4">
          <GroupBox1 />
          <GroupBox3 />
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <label>OBS.:</label>
              <Input id="editobs" className="flex-1" />
            </div>
            <div className="flex items-center gap-2">
              <label>Lineas/Und Rechazadas:</label>
              <Input id="editlinerechazo" className="w-24" readOnly />
              <Input id="editcantrechazo" className="w-24" readOnly />
            </div>
            <div className="flex justify-end gap-2">
              <Button id="botongenerar" disabled>
                Grabar Pedidos
              </Button>
              <Button id="botoncancelar" variant="outline">
                Cancelar
              </Button>
              <Button id="botonexportar" disabled>
                Exportar Datos
              </Button>
              <Button id="botonexporotr" disabled>
                Exportar OTR rechazo
              </Button>
              <Button id="botonsalir">Salir</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

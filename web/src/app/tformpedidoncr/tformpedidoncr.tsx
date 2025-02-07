'use client'

import Panel1 from './components/Panel1'
import Panel2 from './components/Panel2'
import Panel5 from './components/Panel5'

export default function FormPedidoNCR() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-4">
        <h1 className="mb-4 text-2xl font-bold">Carga de Pedidos a Bodegas</h1>
        <div className="flex flex-col gap-4">
          <Panel1 />
          <Panel5 />
          <Panel2 />
        </div>
      </div>
    </div>
  )
}

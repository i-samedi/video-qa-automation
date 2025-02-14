'use client'

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import GrillaDeliveryId from './GrillaDeliveryId'
import GrillaDetalle from './GrillaDetalle'
import GrillaInvId from './GrillaInvId'
import GrillaStock from './GrillaStock'
import GrillaOtr from './GrillaOtr'

export default function Panel5() {
  return (
    <div className="p-4" id="panel5">
      <Tabs defaultValue="pedido">
        <TabsList>
          <TabsTrigger value="pedido">Pedido</TabsTrigger>
          <TabsTrigger value="stock">Stock</TabsTrigger>
          <TabsTrigger value="otr">OTR</TabsTrigger>
        </TabsList>
        <TabsContent value="pedido">
          <div className="space-y-4">
            <GrillaDetalle />
            <div className="hidden">
              <GrillaDeliveryId />
              <GrillaInvId />
              <textarea id="mensajeemail" className="h-32 w-full" />
            </div>
          </div>
        </TabsContent>
        <TabsContent value="stock">
          <GrillaStock />
        </TabsContent>
        <TabsContent value="otr">
          <GrillaOtr />
        </TabsContent>
      </Tabs>
    </div>
  )
}

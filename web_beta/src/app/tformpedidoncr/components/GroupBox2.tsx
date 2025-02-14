'use client'

import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

export default function GroupBox2() {
  return (
    <div className="rounded-lg border p-4" id="groupbox2">
      <h3 className="mb-4 text-lg font-medium">CSV Separado Por</h3>
      <RadioGroup defaultValue="puntocoma">
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="puntocoma" id="rbpuntocoma" />
          <label htmlFor="rbpuntocoma">Punto y Coma (;)</label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="coma" id="rbcoma" />
          <label htmlFor="rbcoma">Coma (,)</label>
        </div>
      </RadioGroup>
    </div>
  )
}

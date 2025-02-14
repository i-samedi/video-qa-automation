'use client'

import { Button } from '@/components/ui/button'

export default function Panel2() {
  return (
    <div className="border-t p-4" id="panel2">
      <Button id="button1" className="hidden">
        Button1
      </Button>
      <Button id="button2" className="hidden">
        Button2
      </Button>
    </div>
  )
}

'use client'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

export default function GrillaInvId() {
  return (
    <Table id="grillainvid">
      <TableHeader>
        <TableRow>
          <TableHead>InvID</TableHead>
          <TableHead>Qty</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          <TableCell></TableCell>
          <TableCell></TableCell>
        </TableRow>
      </TableBody>
    </Table>
  )
}

'use client'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

export default function GrillaStock() {
  return (
    <Table id="grillastock">
      <TableHeader>
        <TableRow>
          <TableHead>C/Modelo</TableHead>
          <TableHead>C/Color</TableHead>
          <TableHead>Nº</TableHead>
          <TableHead>SKU</TableHead>
          <TableHead>Stock</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          <TableCell></TableCell>
          <TableCell></TableCell>
          <TableCell></TableCell>
          <TableCell></TableCell>
          <TableCell></TableCell>
        </TableRow>
      </TableBody>
    </Table>
  )
}

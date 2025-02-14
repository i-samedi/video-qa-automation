'use client'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

export default function GrillaOtr() {
  return (
    <Table id="grillaotr">
      <TableHeader>
        <TableRow>
          <TableHead>IDTienda</TableHead>
          <TableHead>Marca</TableHead>
          <TableHead>Clase</TableHead>
          <TableHead>Otr</TableHead>
          <TableHead>Digitado</TableHead>
          <TableHead>Carga</TableHead>
          <TableHead>Autorizado</TableHead>
          <TableHead>Excedente</TableHead>
          <TableHead>Archivo</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          <TableCell></TableCell>
          <TableCell></TableCell>
          <TableCell></TableCell>
          <TableCell></TableCell>
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

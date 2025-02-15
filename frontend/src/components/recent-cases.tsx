"use client"

import { ArrowUpRight } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const recentCases = [
  { id: "001", patient: "John Doe", priority: "High", status: "In Progress", time: "10 min ago" },
  { id: "002", patient: "Jane Smith", priority: "Medium", status: "Completed", time: "25 min ago" },
  { id: "003", patient: "Bob Johnson", priority: "Low", status: "Pending", time: "1 hour ago" },
  { id: "004", patient: "Alice Brown", priority: "High", status: "In Progress", time: "2 hours ago" },
  { id: "005", patient: "Charlie Davis", priority: "Medium", status: "Completed", time: "3 hours ago" },
]

export function RecentCases() {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Case ID</TableHead>
          <TableHead>Patient</TableHead>
          <TableHead>Priority</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Time</TableHead>
          <TableHead>Action</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {recentCases.map((caseItem) => (
          <TableRow key={caseItem.id}>
            <TableCell>{caseItem.id}</TableCell>
            <TableCell>{caseItem.patient}</TableCell>
            <TableCell>
              <Badge
                variant={
                  caseItem.priority === "High"
                    ? "destructive"
                    : caseItem.priority === "Medium"
                      ? "default"
                      : "secondary"
                }
              >
                {caseItem.priority}
              </Badge>
            </TableCell>
            <TableCell>{caseItem.status}</TableCell>
            <TableCell>{caseItem.time}</TableCell>
            <TableCell>
              <ArrowUpRight className="h-4 w-4 cursor-pointer" />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}


"use client"

import { ArrowUpDown, ChevronDown, MoreHorizontal } from "lucide-react"
import * as React from "react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const cases = [
  {
    id: "001",
    patient: "John Doe",
    priority: "High",
    status: "In Progress",
    assignedTo: "Dr. Smith",
    dateCreated: "2023-06-01",
    lastUpdated: "2023-06-02",
  },
  {
    id: "002",
    patient: "Jane Smith",
    priority: "Medium",
    status: "Completed",
    assignedTo: "Dr. Johnson",
    dateCreated: "2023-05-30",
    lastUpdated: "2023-06-01",
  },
  {
    id: "003",
    patient: "Bob Johnson",
    priority: "Low",
    status: "Pending",
    assignedTo: "Dr. Williams",
    dateCreated: "2023-06-02",
    lastUpdated: "2023-06-02",
  },
  {
    id: "004",
    patient: "Alice Brown",
    priority: "High",
    status: "In Progress",
    assignedTo: "Dr. Davis",
    dateCreated: "2023-05-29",
    lastUpdated: "2023-06-01",
  },
  {
    id: "005",
    patient: "Charlie Davis",
    priority: "Medium",
    status: "Completed",
    assignedTo: "Dr. Miller",
    dateCreated: "2023-05-28",
    lastUpdated: "2023-05-31",
  },
]

type CaseKey = keyof typeof cases[0]

export function CasesTable() {
  const [sorting, setSorting] = React.useState<CaseKey | null>(null)
  const [sortDirection, setSortDirection] = React.useState<"asc" | "desc">("asc")
  const [selectedCases, setSelectedCases] = React.useState<string[]>([])

  const sortedCases = React.useMemo(() => {
    if (!sorting) return cases

    return [...cases].sort((a, b) => {
      if (a[sorting] < b[sorting]) return sortDirection === "asc" ? -1 : 1
      if (a[sorting] > b[sorting]) return sortDirection === "asc" ? 1 : -1
      return 0
    })
  }, [sorting, sortDirection])

  const handleSort = (column: CaseKey) => {
    if (sorting === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc")
    } else {
      setSorting(column)
      setSortDirection("asc")
    }
  }

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedCases(cases.map((c) => c.id))
    } else {
      setSelectedCases([])
    }
  }

  const handleSelectCase = (caseId: string, checked: boolean | string) => {
    if (checked === true) {
      setSelectedCases([...selectedCases, caseId])
    } else {
      setSelectedCases(selectedCases.filter((id) => id !== caseId))
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between p-4">
        <div className="flex items-center space-x-2">
          <Input placeholder="Search cases..." className="max-w-sm" />
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">
                Columns <ChevronDown className="ml-2 h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Toggle columns</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuCheckboxItem checked>Case ID</DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem checked>Patient</DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem checked>Priority</DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem checked>Status</DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem checked>Assigned To</DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem checked>Date Created</DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem checked>Last Updated</DropdownMenuCheckboxItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <div className="flex items-center space-x-2">
          <Select>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Statuses</SelectItem>
              <SelectItem value="in-progress">In Progress</SelectItem>
              <SelectItem value="completed">Completed</SelectItem>
              <SelectItem value="pending">Pending</SelectItem>
            </SelectContent>
          </Select>
          <Button>Export</Button>
        </div>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[50px]">
              <Checkbox checked={selectedCases.length === cases.length} onCheckedChange={handleSelectAll} />
            </TableHead>
            <TableHead className="w-[100px]">
              <Button variant="ghost" onClick={() => handleSort("id")}>
                Case ID
                <ArrowUpDown className="ml-2 h-4 w-4" />
              </Button>
            </TableHead>
            <TableHead>
              <Button variant="ghost" onClick={() => handleSort("patient")}>
                Patient
                <ArrowUpDown className="ml-2 h-4 w-4" />
              </Button>
            </TableHead>
            <TableHead>Priority</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>
              <Button variant="ghost" onClick={() => handleSort("assignedTo")}>
                Assigned To
                <ArrowUpDown className="ml-2 h-4 w-4" />
              </Button>
            </TableHead>
            <TableHead>
              <Button variant="ghost" onClick={() => handleSort("dateCreated")}>
                Date Created
                <ArrowUpDown className="ml-2 h-4 w-4" />
              </Button>
            </TableHead>
            <TableHead>
              <Button variant="ghost" onClick={() => handleSort("lastUpdated")}>
                Last Updated
                <ArrowUpDown className="ml-2 h-4 w-4" />
              </Button>
            </TableHead>
            <TableHead className="w-[100px]">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedCases.map((caseItem) => (
            <TableRow key={caseItem.id}>
              <TableCell>
                <Checkbox
                  checked={selectedCases.includes(caseItem.id)}
                  onCheckedChange={(checked) => handleSelectCase(caseItem.id, checked)}
                />
              </TableCell>
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
              <TableCell>{caseItem.assignedTo}</TableCell>
              <TableCell>{caseItem.dateCreated}</TableCell>
              <TableCell>{caseItem.lastUpdated}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>View details</DropdownMenuItem>
                    <DropdownMenuItem>Update status</DropdownMenuItem>
                    <DropdownMenuItem>Reassign</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className="flex items-center justify-end space-x-2 py-4">
        <Button variant="outline" size="sm">
          Previous
        </Button>
        <Button variant="outline" size="sm">
          Next
        </Button>
      </div>
    </div>
  )
}
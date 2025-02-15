"use client"

import { BarChart2, FileText, Home, Settings, Users } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"

export function Sidebar() {
  return (
    <aside className="hidden sm:flex sm:flex-col w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
      <nav className="flex-1 px-2 py-4 space-y-2">
        <Button variant="ghost" className="w-full justify-start" asChild>
          <Link href="/">
            <Home className="mr-3 h-5 w-5" />
            Dashboard
          </Link>
        </Button>
        <Button variant="ghost" className="w-full justify-start" asChild>
          <Link href="/cases">
            <FileText className="mr-3 h-5 w-5" />
            Cases
          </Link>
        </Button>
        <Button variant="ghost" className="w-full justify-start" asChild>
          <Link href="/analytics">
            <BarChart2 className="mr-3 h-5 w-5" />
            Analytics
          </Link>
        </Button>
        <Button variant="ghost" className="w-full justify-start" asChild>
          <Link href="/users">
            <Users className="mr-3 h-5 w-5" />
            Users
          </Link>
        </Button>
        <Button variant="ghost" className="w-full justify-start" asChild>
          <Link href="/settings">
            <Settings className="mr-3 h-5 w-5" />
            Settings
          </Link>
        </Button>
      </nav>
    </aside>
  )
}
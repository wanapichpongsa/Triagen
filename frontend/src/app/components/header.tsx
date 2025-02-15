import { Bell, Search } from "lucide-react"
import Image from "next/image"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function Header() {
  return (
    <header className="bg-white dark:bg-gray-800 shadow">
      <div className="container mx-auto px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Link href="/" className="flex items-center">
              <Image src="/nhs-logo.svg" alt="NHS Logo" width={48} height={48} />
              <span className="ml-2 text-xl font-semibold text-gray-800 dark:text-white">NHS Triage Automation</span>
            </Link>
          </div>
          <div className="flex items-center">
            <div className="relative mr-4">
              <Input type="text" className="w-full pl-10 pr-4 py-2 rounded-lg" placeholder="Search..." />
              <div className="absolute top-3 left-3">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
            </div>
            <Button variant="ghost" size="icon">
              <Bell className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="ml-4">
              <Image src="/placeholder-user.jpg" alt="User Avatar" width={32} height={32} className="rounded-full" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
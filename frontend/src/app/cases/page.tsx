"use client"

import { UploadCloud } from 'lucide-react'

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

import { CasesTable } from "@/components/all-cases"
import { Header } from "@/components/header"
import { Sidebar } from "@/components/sidebar"

export default function CasesPage() {
  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 dark:bg-gray-900">
          <div className="container mx-auto px-6 py-8">
            <h1 className="text-3xl font-semibold text-gray-800 dark:text-white mb-6">Cases</h1>
            
            {/* File Upload Section */}
            <div className="mb-8 p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
              <h2 className="text-xl font-semibold mb-4">Upload New Cases</h2>
              <div className="flex items-center space-x-4">
                <div className="grid w-full max-w-sm items-center gap-1.5">
                  <Label htmlFor="caseFile">Case File</Label>
                  <Input id="caseFile" type="file" />
                </div>
                <Button className="mt-6">
                  <UploadCloud className="mr-2 h-4 w-4" /> Upload
                </Button>
              </div>
            </div>

            {/* Cases Table */}
            <div className="bg-white dark:bg-gray-800 shadow rounded-lg">
              <CasesTable />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

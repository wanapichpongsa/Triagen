"use client"

import { UploadCloud } from 'lucide-react'
import { useState } from "react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

import { CasesTable } from "@/components/all-cases"
import { Header } from "@/components/header"
import { Sidebar } from "@/components/sidebar"

import toast, { Toaster } from "react-hot-toast"

export default function CasesPage() {
  const [isUploading, setIsUploading] = useState(false) // used for upload button 'upload' => 'uploading...' state
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    setSelectedFile(file || null)
  }

  const handleUploadClick = async () => {
    if (!selectedFile) return
    setIsUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      })
      if (!response.ok) throw new Error('Upload failed')
      const fileInput = document.getElementById('caseFile') as HTMLInputElement
      if (fileInput) fileInput.value = ''
      toast.success('Upload successful')
    } catch (error) {
      console.error(error)
      toast.error('Upload failed')
    } finally {
      setIsUploading(false)
    }
  }

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
                  <Input 
                    id="caseFile" 
                    type="file"
                    onChange={handleFileSelect}
                    disabled={isUploading}
                    multiple={false}
                    key={selectedFile ? 'has-file' : 'no-file'}
                  /> {/* Set multiple to true when can handle multiple files */}
                </div>
                <Button className="mt-6" onClick={handleUploadClick} disabled={isUploading}>
                  <UploadCloud className="mr-2 h-4 w-4" />
                  {isUploading ? 'Uploading...' : 'Upload'}
                </Button>
                <Toaster />
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

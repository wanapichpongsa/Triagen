"use server"

import { NextResponse } from 'next/server'
import { writeFile } from 'fs/promises'
import path from 'path'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

export async function POST(request: Request) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File
    const bytes = await file.arrayBuffer()
    const buffer = Buffer.from(bytes)
    
    // Get the project root directory (where frontend and backend folders are)
    const projectRoot = path.join(process.cwd(), '../..')
    const backendPath = path.join(projectRoot, 'backend')
    
    // Save file
    const filePath = path.join(backendPath, 'data', file.name)
    await writeFile(filePath, buffer)

    // Execute Python script using absolute path
    const { stdout, stderr } = await execAsync(`python3 ${path.join(backendPath, 'main.py')}`)
    console.log('Python output:', stdout)
    if (stderr) console.error('Python error:', stderr)

    return NextResponse.json({ message: 'File uploaded and processed' })
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json({ error: 'Process failed' }, { status: 500 })
  }
}
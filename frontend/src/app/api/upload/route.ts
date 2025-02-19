"use server"

import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const formData = await request.formData()
    /*
    formData:
    ----boundary----
    Content-Disposition: form-data; name="fieldName"

    value
    ----boundary----
    Content-Disposition: form-data; name="file"; filename="example.jpg"
    Content-Type: image/jpeg

    [Binary file data]
    ----boundary----
    */
   console.log(formData)
    
    const destinationEndpoint = "http://127.0.0.1:8080/api/triagen-engine"
    const response = await fetch(destinationEndpoint, {
      headers: {
        // TODO: add id
        'Accept': 'application/json'
        // Browser automatically sets Content-type header with necessary boundary e.g., multipart/form-data; boundary=----WebKitFormBoundaryABC123...
      },
      method: 'POST',
      body: formData
    })
    return response
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json({ error: 'Process failed' }, { status: 500 })
  }
}
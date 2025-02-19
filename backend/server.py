from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/triagen-engine':
            content_length = int(self.headers.get('Content-Length', 0))
            print(content_length)
            # Parse the multipart form data
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'message': 'File processed successfully'}
            self.wfile.write(json.dumps(response).encode())
            """
            content_type = self.headers.get('Content-Type', '')
            if 'multipart/form-data' in content_type:
                boundary: str = content_type.split('=')[1].strip()
            
                # Get the file from form data
                if 'file' in form:
                    fileitem = form['file']
                    # Process the file
                    filename = fileitem.filename
                    file_data = fileitem.file.read()

                    with open(f'data/{filename}', 'wb') as f:
                        f.write(file_data)

                    # Send response
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {'message': f'File {filename} processed successfully'}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_error(400, "No file found in request")
            else:
                self.send_error(400, "Expected multipart/form-data")
            """   
        else:
            self.send_error(404, "Path not found")

def run_server():
    server = HTTPServer(('127.0.0.1', 8080), RequestHandler)
    print("Server running on http://127.0.0.1:8080")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
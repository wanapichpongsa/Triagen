from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class RequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/triagen-engine':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                content_type = self.headers.get('Content-Type', '')

                if 'multipart/form-data' not in content_type:
                    self.send_error(400, "Expected multipart/form-data")
                    return
                logging.info("<< PROCESSING FILE >>")
                post_data: bytes = self.rfile.read(content_length)
                boundary: str = content_type.split('=')[1].strip()
                boundary: bytes = boundary.encode()
                parts = post_data.split(boundary)
                """ Example HTTP File Form Structure
                ------WebKitFormBoundaryABC123
                Content-Disposition: form-data; name="file"; filename="example.pdf"
                Content-Type: application/pdf

                [actual file data here]
                ------WebKitFormBoundaryABC123--
                """
                for part in parts:
                    part = bytes(part)
                    if b'name="file"' in part and b'filename=' in part:
                        
                        filename = part.split(b'filename=')[1].split(b'\r\n')[0].strip(b'"').decode()
                        # Find start of file content (after double \r\n). \r is carriage return like on a typewriter.
                        file_content = part.split(b'\r\n\r\n')[1].rsplit(b'\r\n', 1)[0]
                        
                        # Save file
                        with open(f'data/{filename}', 'wb') as f:
                            f.write(file_content)
                            
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        response = {'message': f'File {filename} processed successfully'}
                        self.wfile.write(json.dumps(response).encode())
                        return
                    
                self.send_error(400, "No file found in request")
            except Exception as e:
                logging.error(f"Error: {e}")
                self.send_error(500, str(e))

        else:
            self.send_error(404, "Path not found")

def run_server():
    server = HTTPServer(('127.0.0.1', 8080), RequestHandler)
    print("Server running on http://127.0.0.1:8080")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
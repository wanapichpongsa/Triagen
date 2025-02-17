from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self): # requires do_prefix
        if self.path == '/api/triagen-engine':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': 'received'}
        else:
            self.send_response(404)
            self.end_headers()
            response = {'error': 'route not found'}
        self.wfile.write(json.dumps(response).encode())

def server():
    LOCAL_PORT: int = 8080
    LOCAL_SERVER_URL: str = "http://127.0.0.1:" + str(LOCAL_PORT)
    
    server = HTTPServer(("127.0.0.1", LOCAL_PORT), RequestHandler)
    print(f"Server running on {LOCAL_SERVER_URL}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Server closed")

if __name__ == "__main__":
    server()
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
print(f"Starting server on port {port}...")
httpd = HTTPServer(('localhost', port), CORSRequestHandler)
httpd.serve_forever() 
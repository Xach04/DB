from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(message).encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self._send_response({'message': 'Hello World!'})
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/users':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                # Попробуйте декодировать JSON
                user_data = json.loads(post_data)
                self._send_response({
                    'message': 'User created',
                    'user': user_data
                }, status_code=201)
            except json.JSONDecodeError:
                # Если JSON невалиден, отправьте ошибку
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Invalid JSON')
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Leer el cuerpo de la petición
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # 2. Obtener la key
            api_key = os.environ.get('OPENROUTER_API_KEY')
            
            # 3. Configurar la petición a OpenRouter
            url = "https://openrouter.ai/api/v1/chat/completions"
            req = urllib.request.Request(url, data=body, method='POST')
            req.add_header('Authorization', f"Bearer {api_key}")
            req.add_header('Content-Type', 'application/json')
            
            # 4. Ejecutar
            with urllib.request.urlopen(req) as response:
                data = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(data)
                
        except Exception as e:
            # Responder con el error exacto para que el frontend lo capture
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

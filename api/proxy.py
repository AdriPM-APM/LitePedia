import os
import json
import urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. Debug: Log the environment variable existence
            api_key = os.environ.get('OPENROUTER_API_KEY')
            if not api_key:
                print("ERROR: OPENROUTER_API_KEY is NULL. Check Vercel Settings.")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing API Key"}).encode())
                return

            # 2. Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                print("ERROR: Request body is empty.")
                self.send_response(400)
                self.end_headers()
                return
            
            body = self.rfile.read(content_length)
            
            # 3. Call OpenRouter
            url = "https://openrouter.ai/api/v1/chat/completions"
            req = urllib.request.Request(url, data=body, method='POST')
            req.add_header('Authorization', f"Bearer {api_key}")
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req) as response:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response.read())
                
        except Exception as e:
            print(f"CRITICAL PYTHON ERROR: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

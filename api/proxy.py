import os
import json
from http.server import BaseHTTPRequestHandler
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # DEBUG LOG
            api_key = os.environ.get('OPENROUTER_API_KEY')
            print(f"DEBUG: API Key present: {api_key is not None}") # This will appear in your Vercel Logs
            
            if not api_key:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "API Key is missing in Vercel Environment"}).encode())
                return

            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
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
            print(f"CRITICAL ERROR: {str(e)}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

from http.server import BaseHTTPRequestHandler
import os
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # This will show up in Vercel logs to confirm the variable status
        key_exists = "OPENROUTER_API_KEY" in os.environ
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "debug",
            "key_present": key_exists
        }
        self.wfile.write(json.dumps(response).encode())

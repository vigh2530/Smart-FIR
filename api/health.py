"""Health check endpoint for Vercel"""
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"status": "healthy", "timestamp": str(__import__('datetime').datetime.now())}
        self.wfile.write(json.dumps(response).encode('utf-8'))

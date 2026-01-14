#!/usr/bin/env python3
"""
Vercel Serverless Function for FIR Analysis API
This replaces Streamlit for serverless deployment
"""

from http.server import BaseHTTPRequestHandler
import json
import pickle
import os
import sys

# Add paths
sys.path.insert(0, os.path.dirname(__file__))

from utils.preprocessing import preprocess_fir
from utils.fir_quality import check_fir_quality
from utils.explainability import get_top_keywords
from ollama.ollama_client import call_ollama
from ollama.prompts import (
    severity_prompt,
    ipc_explanation_prompt,
    punishment_prompt,
    hinglish_prompt
)

# Load models once
try:
    model = pickle.load(open("models/ipc_model.pkl", "rb"))
    vectorizer = pickle.load(open("models/tfidf_vectorizer.pkl", "rb"))
except Exception as e:
    print(f"Error loading models: {e}")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests"""
        if self.path == "/api/analyze":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
                fir_input = data.get("fir_text", "").strip()
                
                if not fir_input:
                    self.send_error_response(400, "FIR text required")
                    return
                
                # Process FIR
                translated = call_ollama(hinglish_prompt(fir_input))
                processed = preprocess_fir(translated)
                
                vec = vectorizer.transform([processed])
                probs = model.predict_proba(vec)[0]
                classes = model.classes_
                
                top3 = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]
                primary_ipc = top3[0][0]
                
                quality = check_fir_quality(processed)
                keywords = get_top_keywords(model, vectorizer, processed)
                
                severity = call_ollama(severity_prompt(processed, primary_ipc))
                explanation = call_ollama(ipc_explanation_prompt(processed, primary_ipc))
                punishment = call_ollama(punishment_prompt(primary_ipc))
                
                # Prepare response
                response = {
                    "status": "success",
                    "ipc_predictions": [{"section": sec, "probability": float(prob)} for sec, prob in top3],
                    "quality_score": quality["quality_score"],
                    "warnings": quality["warnings"],
                    "keywords": keywords,
                    "severity": severity,
                    "explanation": explanation,
                    "punishment": punishment
                }
                
                self.send_success_response(response)
                
            except Exception as e:
                self.send_error_response(500, str(e))
        
        elif self.path == "/api/health":
            self.send_success_response({"status": "ok", "model": "mistral"})
        
        else:
            self.send_error_response(404, "Endpoint not found")
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/api/health":
            self.send_success_response({"status": "ok", "model": "mistral"})
        else:
            self.send_error_response(404, "Not found")
    
    def send_success_response(self, data):
        """Send JSON success response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, status_code, message):
        """Send JSON error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"status": "error", "message": message}
        self.wfile.write(json.dumps(response).encode('utf-8'))

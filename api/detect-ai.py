# api/detect-ai.py
from http.server import BaseHTTPRequestHandler
import json
import requests
from urllib.parse import parse_qs
import base64
import io

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Configurar CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        try:
            # Ler dados do request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse multipart form data (simplificado)
            # Em produção, use uma biblioteca como `python-multipart`
            
            # Para esta demo, vamos aceitar base64 image
            data = json.loads(post_data.decode('utf-8'))
            image_data = data.get('image_base64')
            
            if not image_data:
                raise ValueError("image_base64 is required")
            
            # Decodificar base64
            image_bytes = base64.b64decode(image_data.split(',')[1])
            
            # Chamar API Sightengine
            params = {
                'models': 'genai',
                'api_user': '977059260',
                'api_secret': 'hcZbaLerB8gq8k9v7NBPyPXnKDTLdogt'
            }
            
            files = {'media': ('image.jpg', io.BytesIO(image_bytes), 'image/jpeg')}
            
            response = requests.post(
                'https://api.sightengine.com/1.0/check.json',
                files=files,
                data=params,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"Sightengine API error: {response.status_code}")
            
            result = response.json()
            
            if result.get('status') != 'success':
                raise Exception(f"API returned error: {result}")
            
            ai_score = result['type']['ai_generated']
            
            # Resposta formatada
            response_data = {
                'success': True,
                'is_ai': ai_score > 0.5,
                'confidence': ai_score,
                'score_percentage': round(ai_score * 100, 1),
                'label': 'IA' if ai_score > 0.5 else 'Humana',
                'request_id': result.get('request', {}).get('id'),
                'operations_used': result.get('request', {}).get('operations', 1)
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                'success': False,
                'error': str(e),
                'message': 'Erro ao processar imagem'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight CORS request
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
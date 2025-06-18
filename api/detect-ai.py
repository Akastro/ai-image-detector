from http.server import BaseHTTPRequestHandler
import json
import requests
import base64
import io
import os

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
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            image_data = data.get('image_base64')
            
            if not image_data:
                raise ValueError("image_base64 is required")
            
            # Decodificar base64 (remover prefixo data:image/...)
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            
            # Credenciais da API (pode usar env vars para segurança)
            api_user = os.environ.get('SIGHTENGINE_API_USER', '977059260')
            api_secret = os.environ.get('SIGHTENGINE_API_SECRET', 'hcZbaLerB8gq8k9v7NBPyPXnKDTLdogt')
            
            # Chamar API Sightengine
            params = {
                'models': 'genai',
                'api_user': api_user,
                'api_secret': api_secret
            }
            
            files = {'media': ('image.jpg', io.BytesIO(image_bytes), 'image/jpeg')}
            
            response = requests.post(
                'https://api.sightengine.com/1.0/check.json',
                files=files,
                data=params,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"Sightengine API HTTP {response.status_code}: {response.text}")
            
            result = response.json()
            
            if result.get('status') != 'success':
                error_msg = result.get('error', {}).get('message', 'Unknown API error')
                raise Exception(f"API Error: {error_msg}")
            
            ai_score = result['type']['ai_generated']
            
            # Resposta formatada
            response_data = {
                'success': True,
                'is_ai': ai_score > 0.5,
                'confidence': ai_score,
                'score_percentage': round(ai_score * 100, 1),
                'label': 'IA Gerada' if ai_score > 0.5 else 'Humana',
                'request_id': result.get('request', {}).get('id'),
                'operations_used': result.get('request', {}).get('operations', 1),
                'timestamp': result.get('request', {}).get('timestamp'),
                'api_version': 'Sightengine v1.0',
                'detector_info': {
                    'accuracy': '98.3%',
                    'models_detected': ['Stable Diffusion', 'MidJourney', 'DALL-E', 'Adobe Firefly', 'Flux', 'GANs']
                }
            }
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            
        except json.JSONDecodeError:
            error_response = {
                'success': False,
                'error': 'Invalid JSON data',
                'message': 'Por favor, envie dados JSON válidos'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except ValueError as e:
            error_response = {
                'success': False,
                'error': str(e),
                'message': 'Dados de imagem inválidos'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except requests.RequestException as e:
            error_response = {
                'success': False,
                'error': f'Network error: {str(e)}',
                'message': 'Erro de conexão com a API Sightengine'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except Exception as e:
            error_response = {
                'success': False,
                'error': str(e),
                'message': 'Erro interno do servidor'
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight CORS request
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        # Health check endpoint
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        health_response = {
            'status': 'healthy',
            'service': 'AI Image Detector API',
            'version': '1.0.0',
            'endpoints': {
                'POST /api/detect-ai': 'Detectar imagens geradas por IA'
            }
        }
        
        self.wfile.write(json.dumps(health_response, ensure_ascii=False).encode('utf-8'))
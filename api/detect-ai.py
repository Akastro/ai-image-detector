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
            
            # Validar formato base64
            if not image_data.startswith('data:image'):
                raise ValueError("Formato de imagem inválido. Use data:image/...")
            
            # Decodificar base64 (remover prefixo data:image/...)
            if ',' in image_data:
                mime_type = image_data.split(',')[0]
                image_data_clean = image_data.split(',')[1]
            else:
                raise ValueError("Formato base64 inválido")
            
            # Validar base64
            try:
                image_bytes = base64.b64decode(image_data_clean)
            except Exception as e:
                raise ValueError(f"Erro ao decodificar base64: {str(e)}")
            
            # Verificar se não está vazio
            if len(image_bytes) == 0:
                raise ValueError("Dados de imagem vazios")
                
            # Verificar tamanho mínimo (pelo menos 100 bytes)
            if len(image_bytes) < 100:
                raise ValueError("Arquivo muito pequeno, pode estar corrompido")
            
            # Verificar tamanho máximo da imagem (limite Sightengine: 5MB)
            if len(image_bytes) > 5 * 1024 * 1024:
                raise ValueError("Imagem muito grande. Máximo: 5MB")
            
            # Detectar formato da imagem e validar
            if 'webp' in mime_type.lower():
                filename = 'image.webp'
                content_type = 'image/webp'
                # WebP pode ter problemas, vamos logar
                print(f"⚠️  WebP detected - may need conversion")
            elif 'png' in mime_type.lower():
                filename = 'image.png'
                content_type = 'image/png'
            elif 'jpeg' in mime_type.lower() or 'jpg' in mime_type.lower():
                filename = 'image.jpg'
                content_type = 'image/jpeg'
            else:
                # Fallback para JPEG
                filename = 'image.jpg'
                content_type = 'image/jpeg'
                print(f"⚠️  Unknown format {mime_type}, using JPEG fallback")
            
            # Credenciais da API
            api_user = os.environ.get('SIGHTENGINE_API_USER', '977059260')
            api_secret = os.environ.get('SIGHTENGINE_API_SECRET', 'hcZbaLerB8gq8k9v7NBPyPXnKDTLdogt')
            
            # Chamar API Sightengine
            params = {
                'models': 'genai',
                'api_user': api_user,
                'api_secret': api_secret
            }
            
            files = {'media': (filename, io.BytesIO(image_bytes), content_type)}
            
            print(f"Processing {filename} ({content_type}) - Size: {len(image_bytes)} bytes")
            print(f"Calling Sightengine API...")
            
            response = requests.post(
                'https://api.sightengine.com/1.0/check.json',
                files=files,
                data=params,
                timeout=30
            )
            
            print(f"API Response Status: {response.status_code}")
            print(f"API Response Headers: {response.headers}")
            print(f"API Response Text: {response.text[:500]}...")
            
            if response.status_code != 200:
                raise Exception(f"Sightengine API HTTP {response.status_code}: {response.text}")
            
            # Verificar se a resposta é JSON válido
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                raise Exception(f"API retornou resposta inválida (não JSON): {response.text[:200]}...")
            
            if result.get('status') != 'success':
                error_msg = result.get('error', {}).get('message', 'Unknown API error')
                error_code = result.get('error', {}).get('code', 'unknown')
                raise Exception(f"API Error [{error_code}]: {error_msg}")
            
            # Verificar se o resultado tem o campo esperado
            if 'type' not in result or 'ai_generated' not in result['type']:
                raise Exception(f"API response missing expected fields: {result}")
            
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
                },
                'debug_info': {
                    'image_size_bytes': len(image_bytes),
                    'api_status_code': response.status_code
                }
            }
            
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            
        except json.JSONDecodeError as e:
            error_response = {
                'success': False,
                'error': f'Invalid JSON in request: {str(e)}',
                'message': 'Por favor, envie dados JSON válidos'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except ValueError as e:
            error_response = {
                'success': False,
                'error': str(e),
                'message': 'Dados de imagem inválidos ou muito grandes'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except requests.exceptions.Timeout:
            error_response = {
                'success': False,
                'error': 'Request timeout',
                'message': 'Timeout ao conectar com a API Sightengine (30s)'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except requests.exceptions.ConnectionError:
            error_response = {
                'success': False,
                'error': 'Connection error',
                'message': 'Erro de conexão com a API Sightengine'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
        except requests.RequestException as e:
            error_response = {
                'success': False,
                'error': f'Network error: {str(e)}',
                'message': 'Erro de rede ao conectar com a API Sightengine'
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
# 🔍 AI Image Detector

Detector de imagens geradas por inteligência artificial usando a API Sightengine com deploy automático na Vercel.

## 🚀 Demo

- **Live Demo**: [https://ai-image-detector.vercel.app](https://ai-image-detector.vercel.app)
- **API Endpoint**: [https://ai-image-detector.vercel.app/api/detect-ai](https://ai-image-detector.vercel.app/api/detect-ai)

## ✨ Funcionalidades

- 🤖 **Detecção precisa**: 98.3% de precisão usando Sightengine API
- ⚡ **Serverless**: Python Functions na Vercel
- 🌐 **Frontend moderno**: Interface intuitiva e responsiva
- 🔄 **Deploy automático**: GitHub → Vercel integração
- 📊 **Análise detalhada**: Score, confiança e metadados
- 🎯 **Múltiplos modelos**: Detecta Stable Diffusion, MidJourney, DALL-E, etc.

## 🛠️ Tecnologias

- **Backend**: Python 3.9 (Serverless Functions)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API**: Sightengine AI Detection
- **Deploy**: Vercel
- **CI/CD**: GitHub Actions (automático)

## 📁 Estrutura do Projeto

```
ai-image-detector/
├── api/
│   └── detect-ai.py          # Serverless function Python
├── public/
│   └── index.html           # Frontend principal
├── requirements.txt          # Dependências Python
├── vercel.json              # Configuração Vercel
├── package.json             # Metadados do projeto
└── README.md                # Esta documentação
```

## 🚀 Deploy Rápido

### 1. Fork/Clone este repositório

```bash
git clone https://github.com/SEU_USUARIO/ai-image-detector.git
cd ai-image-detector
```

### 2. Deploy na Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FSEU_USUARIO%2Fai-image-detector)

**OU manualmente:**

1. Acesse [vercel.com](https://vercel.com)
2. Conecte com GitHub
3. Selecione este repositório
4. Deploy! 🚀

### 3. Configurar Variáveis de Ambiente (Opcional)

Na Vercel Dashboard → Settings → Environment Variables:

```
SIGHTENGINE_API_USER=977059260
SIGHTENGINE_API_SECRET=hcZbaLerB8gq8k9v7NBPyPXnKDTLdogt
```

## 📡 Uso da API

### Endpoint

```
POST https://ai-image-detector.vercel.app/api/detect-ai
```

### Request

```javascript
const response = await fetch('/api/detect-ai', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    image_base64: 'data:image/jpeg;base64,/9j/4AAQSkZJRgABA...'
  })
});

const result = await response.json();
```

### Response

```json
{
  "success": true,
  "is_ai": false,
  "confidence": 0.05,
  "score_percentage": 5.0,
  "label": "Humana",
  "request_id": "req_abc123",
  "operations_used": 1,
  "api_version": "Sightengine v1.0"
}
```

## 🔧 Desenvolvimento Local

### Pré-requisitos

- Node.js 14+
- Python 3.9+
- Vercel CLI

### Setup

```bash
# Instalar Vercel CLI
npm i -g vercel

# Instalar dependências
pip install -r requirements.txt

# Executar localmente
vercel dev
```

Acesse: `http://localhost:3000`

## 🎯 Casos de Uso

- **Plataformas de mídia**: Detectar e rotular conteúdo IA
- **Verificação de notícias**: Combater desinformação
- **E-commerce**: Validar autenticidade de produtos
- **Redes sociais**: Moderar conteúdo sintético
- **KYC/AML**: Detectar documentos falsos
- **Arte digital**: Verificar originalidade

## 📊 Modelos Detectados

- ✅ Stable Diffusion (todas versões)
- ✅ MidJourney (v3-v6)
- ✅ DALL-E (1, 2, 3)
- ✅ Adobe Firefly
- ✅ Flux
- ✅ GANs
- ✅ Bing Image Creator
- ✅ E mais...

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [Sightengine](https://sightengine.com) pela excelente API de detecção
- [Vercel](https://vercel.com) pela plataforma de deploy
- [GitHub](https://github.com) pela hospedagem do código

## 📞 Suporte

- 🐛 [Reportar bugs](https://github.com/SEU_USUARIO/ai-image-detector/issues)
- 💡 [Sugerir funcionalidades](https://github.com/SEU_USUARIO/ai-image-detector/issues)
- 📧 [Contato direto](mailto:seu@email.com)

---

**⭐ Se este projeto foi útil, deixe uma estrela no GitHub!**

# 🤖 AI DevOps Agent

Intelligent DevOps agent with log analysis and chat functionality, built on OpenAI GPT and Weaviate vector database.

![CI/CD](https://github.com/justrunme/ai-agent/workflows/CI%2FCD%20Pipeline/badge.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange.svg)
![Weaviate](https://img.shields.io/badge/Weaviate-Vector%20DB-purple.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red.svg)

## 🚀 Features

- **💬 Intelligent Chat Bot** - Russian language interaction
- **📊 Log Analysis** - Semantic search and analysis of container logs
- **🔍 Vector Search** - Using Weaviate for fast log search
- **🐳 Docker Integration** - Automatic log collection from containers
- **🤖 AI Analysis** - GPT-3.5 for log analysis and interpretation
- **⚡ Scalability** - Microservices architecture

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   Agent API     │    │   OpenAI API    │
│                 │◄──►│   (Flask)       │◄──►│   (GPT-3.5)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Weaviate DB   │
                       │   (Vector DB)   │
                       └─────────────────┘
                                ▲
                                │
                       ┌─────────────────┐
                       │  Log Ingestor   │
                       │  (Docker Logs)  │
                       └─────────────────┘
```

### System Components:

- **Agent Service** - Flask API for request processing
- **Log Ingestor** - Service for log collection and indexing
- **Weaviate** - Vector database for semantic search
- **OpenAI Integration** - For embedding generation and analysis

## 🛠️ Technology Stack

- **Backend**: Python 3.9, Flask
- **AI/ML**: OpenAI GPT-3.5, OpenAI Embeddings
- **Database**: Weaviate (Vector Database)
- **Containerization**: Docker, Docker Compose
- **Log Processing**: Docker API, OpenAI Embeddings
- **API**: RESTful API

## 📦 Installation and Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- OpenAI API key

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-devops-agent.git
   cd ai-devops-agent
   ```

2. **Create configuration file**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Start the system**
   ```bash
   docker compose up --build -d
   ```

4. **Verify functionality**
   ```bash
   python test_agent.py
   python test_logs.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following parameters:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Weaviate Configuration
WEAVIATE_URL=http://weaviate:8080

# Agent Configuration
AGENT_PORT=5000
```

## 📚 API Documentation

### Chat Endpoint

**POST** `/chat`

Sends a message to the chat bot and receives a response.

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, what is your name?"}'
```

**Response:**
```json
{
  "answer": "Hello! My name is Assistant. How can I help you?"
}
```

### Log Analysis Endpoint

**POST** `/logs`

Analyzes logs based on semantic search.

```bash
curl -X POST http://localhost:5000/logs \
  -H "Content-Type: application/json" \
  -d '{"question": "Why did the service crash?"}'
```

**Response:**
```json
{
  "analysis": "Log analysis shows that the service crashed due to..."
}
```

## 🧪 Testing

### Running Tests

```bash
# Chat functionality test
python test_agent.py

# Log analysis test
python test_logs.py
```

### Test Examples

```python
# Chat test
import requests

response = requests.post('http://localhost:5000/chat', 
                        json={'prompt': 'Hello, what is your name?'})
print(response.json()['answer'])

# Log analysis test
response = requests.post('http://localhost:5000/logs',
                        json={'question': 'Why did the service crash?'})
print(response.json()['analysis'])
```

## 🔍 Monitoring

### Service Status Check

```bash
# Container status
docker compose ps

# Agent logs
docker logs ai-agent-agent-1

# Log ingestor logs
docker logs ai-agent-log-ingestor-1

# Weaviate logs
docker logs ai-agent-weaviate-1
```

## 🚀 Production Deployment

### Docker Compose (Production)

```bash
# Run in background
docker compose -f docker-compose.prod.yml up -d

# Check logs
docker compose -f docker-compose.prod.yml logs -f
```

### Kubernetes (Optional)

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n ai-agent
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for providing the API
- [Weaviate](https://weaviate.io/) for the vector database
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📞 Contact

- **Author**: justrunme
- **Email**: [justrunme@egmail.com]
- **GitHub**: [@justrunme](https://github.com/justrunme)

---

⭐ If you liked this project, give it a star!
# 🚀 AI DevOps Agent Deployment Guide

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Production Deployment](#production-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Monitoring](#monitoring)
5. [Security](#security)
6. [Scaling](#scaling)

## 🏃‍♂️ Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-devops-agent.git
   cd ai-devops-agent
   ```

2. **Set up environment variables**
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
   # Tests
   python test_agent.py
   python test_logs.py
   
   # Web interface
   open http://localhost:8080
   
   # API
   curl http://localhost:5001/health
   ```

## 🏭 Production Deployment

### Docker Compose (Production)

1. **Use production configuration**
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```

2. **Set up production environment variables**
   ```bash
   # .env.prod
   OPENAI_API_KEY=sk-your-production-key
   WEAVIATE_URL=http://weaviate:8080
   GRAFANA_PASSWORD=secure-password
   ```

3. **Check service status**
   ```bash
   docker compose -f docker-compose.prod.yml ps
   docker compose -f docker-compose.prod.yml logs -f
   ```

### Production Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `WEAVIATE_URL` | Weaviate URL | `http://weaviate:8080` |
| `GRAFANA_PASSWORD` | Grafana password | `secure-password` |
| `LOG_INGESTOR_INTERVAL` | Log collection interval (seconds) | `300` |
| `LOG_INGESTOR_BATCH_SIZE` | Log batch size | `50` |

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.19+)
- Helm 3.0+
- kubectl configured

### Installation via Helm

1. **Create namespace**
   ```bash
   kubectl create namespace ai-agent
   ```

2. **Create Secret with API keys**
   ```bash
   kubectl create secret generic ai-agent-secrets \
     --from-literal=openai-api-key=sk-your-key \
     --from-literal=grafana-password=secure-password \
     -n ai-agent
   ```

3. **Install via Helm**
   ```bash
   helm install ai-agent ./helm/ai-agent \
     --namespace ai-agent \
     --set openai.apiKey=sk-your-key
   ```

### Verify Deployment

```bash
# Pod status
kubectl get pods -n ai-agent

# Service logs
kubectl logs -f deployment/ai-agent-agent -n ai-agent
kubectl logs -f deployment/ai-agent-log-ingestor -n ai-agent

# Access services
kubectl port-forward svc/ai-agent-web-ui 8080:80 -n ai-agent
kubectl port-forward svc/ai-agent-agent 5001:5000 -n ai-agent
```

## 📊 Monitoring

### Prometheus + Grafana

The system includes built-in monitoring:

- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000` (admin/admin)

### Metrics

The system collects the following metrics:

- API request count
- Response time
- Memory and CPU usage
- Service status
- Processed log count

### Alerts

Configure alerts in Grafana for:

- High resource usage
- API errors
- Service unavailability
- OpenAI rate limit exceeded

## 🔒 Security

### Security Recommendations

1. **API Keys**
   - Use different keys for dev/prod
   - Rotate keys regularly
   - Limit access permissions

2. **Network**
   - Use HTTPS in production
   - Configure firewall
   - Restrict port access

3. **Containers**
   - Use non-root users
   - Update images regularly
   - Scan for vulnerabilities

### HTTPS Configuration

1. **Get SSL certificate**
   ```bash
   # Let's Encrypt
   certbot certonly --standalone -d your-domain.com
   ```

2. **Configure nginx with SSL**
   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
       
       location / {
           proxy_pass http://agent:5000;
       }
   }
   ```

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale agent
kubectl scale deployment ai-agent-agent --replicas=3 -n ai-agent

# Scale log ingestor
kubectl scale deployment ai-agent-log-ingestor --replicas=2 -n ai-agent
```

### Vertical Scaling

```yaml
# resources.yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

### Auto-scaling

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-agent-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 🛠️ Troubleshooting

### Common Issues

1. **OpenAI API errors**
   ```bash
   # Check limits
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/usage
   ```

2. **Weaviate unavailable**
   ```bash
   # Check status
   curl http://localhost:8081/v1/.well-known/ready
   
   # Restart
   docker compose restart weaviate
   ```

3. **High memory usage**
   ```bash
   # Check logs
   docker stats
   docker logs ai-agent-agent-1
   ```

### Logs and Debugging

```bash
# All logs
docker compose logs -f

# Specific service
docker compose logs -f agent

# Last 100 lines
docker compose logs --tail=100 agent
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-devops-agent/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/ai-devops-agent/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-devops-agent/discussions)

---

⭐ If this project helped you, give it a star on GitHub! 
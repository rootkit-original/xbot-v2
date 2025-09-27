# 🚀 Deployment Guide - Guia de Implantação

Guia completo para deploy do XBot v2 em diferentes ambientes.

## 🎯 Opções de Deployment

### Cenários de Uso

| Cenário | Ambiente | Custo | Complexidade | Uptime |
|---------|----------|-------|-------------|---------|
| **Desenvolvimento** | Local | $0 | Baixa | Variável |
| **Teste/Staging** | VPS básico | $5-10/mês | Média | 99%+ |
| **Produção Small** | VPS otimizado | $20-50/mês | Média | 99.9%+ |
| **Produção Enterprise** | Cloud (AWS/GCP) | $50-200/mês | Alta | 99.99%+ |

## 🏠 Deploy Local (Desenvolvimento)

### Setup Básico

```bash
# 1. Clonar repositório
git clone https://github.com/rootkit-original/xbot-v2.git
cd xbot-v2

# 2. Criar ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependências
pip install -e .

# 4. Configurar ambiente
cp .env.example .env
# Editar .env com suas configurações

# 5. Inicializar banco de dados
python -m src.main init-db

# 6. Executar
python -m src.main
```

### Configuração para Desenvolvimento

```bash
# .env para desenvolvimento
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///xbot_dev.db

# Binance Testnet
BINANCE_API_KEY=your_testnet_key
BINANCE_SECRET_KEY=your_testnet_secret
BINANCE_TESTNET=true

# Telegram (opcional para dev)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Recursos reduzidos para dev
MAX_CONCURRENT_BOTS=3
ANALYSIS_INTERVAL=60
```

### Docker para Desenvolvimento

```dockerfile
# Dockerfile.dev
FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código
COPY src/ src/
COPY tests/ tests/
COPY .env.example .env

# Instalar em modo desenvolvimento
RUN pip install -e .

# Expor porta para dashboard
EXPOSE 8080

# Comando padrão
CMD ["python", "-m", "src.main", "dashboard", "--host", "0.0.0.0"]
```

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  xbot:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
    volumes:
      - ./src:/app/src
      - ./logs:/app/logs
      - ./data:/app/data
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    restart: unless-stopped
```

## 🖥️ Deploy em VPS

### Escolha do Provedor

**Recomendações por orçamento:**

**Básico ($5-10/mês):**
- DigitalOcean Droplet (1GB RAM, 1 vCPU)
- Vultr Cloud Compute (1GB RAM, 1 vCPU)
- Linode Nanode (1GB RAM, 1 vCPU)

**Intermediário ($20-50/mês):**
- AWS EC2 t3.small (2GB RAM, 2 vCPU)
- Google Cloud e2-small (2GB RAM, 2 vCPU)
- Azure B2s (4GB RAM, 2 vCPU)

**Avançado ($50+/mês):**
- Servidores dedicados
- Multi-região setup
- Load balancing

### Setup no Ubuntu 20.04/22.04

```bash
#!/bin/bash
# setup_vps.sh - Script de setup inicial

# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    htop \
    nginx \
    supervisor \
    certbot \
    python3-certbot-nginx

# 3. Criar usuário para o bot
sudo useradd -m -s /bin/bash xbot
sudo usermod -aG sudo xbot

# 4. Configurar firewall
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# 5. Instalar Docker (opcional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker xbot

echo "✅ VPS básico configurado!"
```

### Deploy Manual no VPS

```bash
# 1. Conectar ao VPS
ssh root@your-vps-ip

# 2. Executar setup
bash setup_vps.sh

# 3. Mudar para usuário xbot
su - xbot

# 4. Clonar e configurar aplicação
git clone https://github.com/rootkit-original/xbot-v2.git
cd xbot-v2

python3 -m venv venv
source venv/bin/activate
pip install -e .

# 5. Configurar ambiente
cp .env.example .env
nano .env  # Editar configurações

# 6. Inicializar
python -m src.main init-db

# 7. Testar funcionamento
python -m src.main test-connection
```

### Configuração com Supervisor

```ini
# /etc/supervisor/conf.d/xbot.conf
[program:xbot-main]
command=/home/xbot/xbot-v2/venv/bin/python -m src.main run
directory=/home/xbot/xbot-v2
user=xbot
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/xbot/main.log
environment=PATH="/home/xbot/xbot-v2/venv/bin"

[program:xbot-dashboard]
command=/home/xbot/xbot-v2/venv/bin/python -m src.main dashboard --host 0.0.0.0 --port 8080
directory=/home/xbot/xbot-v2
user=xbot
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/xbot/dashboard.log
environment=PATH="/home/xbot/xbot-v2/venv/bin"
```

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/xbot
sudo chown xbot:xbot /var/log/xbot

# Atualizar supervisor
sudo supervisorctl reread
sudo supervisorctl update

# Controlar serviços
sudo supervisorctl start xbot-main
sudo supervisorctl start xbot-dashboard
sudo supervisorctl status
```

### Configuração do Nginx

```nginx
# /etc/nginx/sites-available/xbot
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    location /static/ {
        alias /home/xbot/xbot-v2/static/;
        expires 30d;
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/xbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Configurar SSL com Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

## 🐳 Deploy com Docker

### Dockerfile de Produção

```dockerfile
# Dockerfile
FROM python:3.9-slim as builder

# Instalar dependências de build
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Estágio final
FROM python:3.9-slim

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash xbot

# Copiar dependências do builder
COPY --from=builder /root/.local /home/xbot/.local

# Copiar aplicação
WORKDIR /app
COPY --chown=xbot:xbot . .

# Configurar PATH
ENV PATH=/home/xbot/.local/bin:$PATH

# Mudar para usuário não-root
USER xbot

# Instalar aplicação
RUN pip install --user -e .

# Expor porta
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -m src.main health-check || exit 1

# Comando padrão
CMD ["python", "-m", "src.main", "run"]
```

### Docker Compose para Produção

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  xbot:
    build: .
    restart: unless-stopped
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
    networks:
      - xbot-network
    depends_on:
      - redis
      - prometheus
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.xbot.rule=Host(`your-domain.com`)"
      - "traefik.http.services.xbot.loadbalancer.server.port=8080"

  redis:
    image: redis:alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - xbot-network
    command: redis-server --appendonly yes

  prometheus:
    image: prom/prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - xbot-network

  grafana:
    image: grafana/grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning
    networks:
      - xbot-network

  traefik:
    image: traefik:v2.9
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./traefik:/etc/traefik
      - ./acme:/acme
    networks:
      - xbot-network

volumes:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  xbot-network:
    driver: bridge
```

### Deploy Script Docker

```bash
#!/bin/bash
# deploy.sh - Script de deploy com Docker

set -e

echo "🚀 Starting XBot v2 deployment..."

# 1. Verificar pré-requisitos
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# 2. Criar diretórios necessários
mkdir -p data logs config monitoring/grafana monitoring/prometheus traefik acme

# 3. Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# 4. Build e deploy
echo "📦 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# 5. Aguardar inicialização
echo "⏳ Waiting for services to start..."
sleep 30

# 6. Verificar health
echo "🔍 Checking service health..."
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "✅ Services started successfully!"
else
    echo "❌ Some services failed to start. Check logs:"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi

# 7. Executar inicialização se necessário
echo "🔧 Running initialization..."
docker-compose -f docker-compose.prod.yml exec xbot python -m src.main init-db

echo "🎉 Deployment completed successfully!"
echo "Dashboard: https://your-domain.com"
echo "Monitoring: http://your-domain.com:3000"
echo "Metrics: http://your-domain.com:9090"
```

## ☁️ Deploy na Cloud

### AWS EC2 com Auto Scaling

```yaml
# aws-cloudformation.yml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'XBot v2 Auto Scaling Deployment'

Parameters:
  KeyName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: EC2 Key Pair for SSH access

Resources:
  XBotLaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: XBot-LaunchTemplate
      LaunchTemplateData:
        ImageId: ami-0c02fb55956c7d316  # Amazon Linux 2
        InstanceType: t3.small
        KeyName: !Ref KeyName
        SecurityGroupIds:
          - !Ref XBotSecurityGroup
        IamInstanceProfile:
          Arn: !GetAtt XBotInstanceProfile.Arn
        UserData:
          Fn::Base64: !Sub |
            #!/bin/bash
            yum update -y
            amazon-linux-extras install docker
            service docker start
            usermod -a -G docker ec2-user
            curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            chmod +x /usr/local/bin/docker-compose
            
            # Deploy XBot
            cd /home/ec2-user
            git clone https://github.com/rootkit-original/xbot-v2.git
            cd xbot-v2
            cp .env.aws .env
            ./deploy.sh

  XBotAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      LaunchTemplate:
        LaunchTemplateId: !Ref XBotLaunchTemplate
        Version: !GetAtt XBotLaunchTemplate.LatestVersionNumber
      MinSize: '1'
      MaxSize: '3'
      DesiredCapacity: '1'
      VPCZoneIdentifier:
        - subnet-12345678
        - subnet-87654321
      TargetGroupARNs:
        - !Ref XBotTargetGroup

  XBotLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Scheme: internet-facing
      SecurityGroups:
        - !Ref XBotSecurityGroup
      Subnets:
        - subnet-12345678
        - subnet-87654321

  XBotTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Port: 8080
      Protocol: HTTP
      VpcId: vpc-12345678
      HealthCheckPath: /health
      HealthCheckProtocol: HTTP
      HealthCheckIntervalSeconds: 30
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 5
```

### Kubernetes Deployment

```yaml
# k8s/namespace.yml
apiVersion: v1
kind: Namespace
metadata:
  name: xbot

---
# k8s/configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: xbot-config
  namespace: xbot
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  DATABASE_URL: "postgresql://user:pass@postgres:5432/xbot"
  REDIS_URL: "redis://redis:6379"

---
# k8s/secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: xbot-secrets
  namespace: xbot
type: Opaque
stringData:
  BINANCE_API_KEY: "your-api-key"
  BINANCE_SECRET_KEY: "your-secret-key"
  TELEGRAM_BOT_TOKEN: "your-bot-token"

---
# k8s/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: xbot
  namespace: xbot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: xbot
  template:
    metadata:
      labels:
        app: xbot
    spec:
      containers:
      - name: xbot
        image: xbot:latest
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: xbot-config
        - secretRef:
            name: xbot-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5

---
# k8s/service.yml
apiVersion: v1
kind: Service
metadata:
  name: xbot-service
  namespace: xbot
spec:
  selector:
    app: xbot
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP

---
# k8s/ingress.yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: xbot-ingress
  namespace: xbot
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - xbot.yourdomain.com
    secretName: xbot-tls
  rules:
  - host: xbot.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: xbot-service
            port:
              number: 80
```

## 📊 Monitoramento e Observabilidade

### Configuração do Prometheus

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'xbot'
    static_configs:
      - targets: ['xbot:8080']
    metrics_path: /metrics
    scrape_interval: 30s

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### Alertas do Prometheus

```yaml
# monitoring/alert_rules.yml
groups:
- name: xbot.rules
  rules:
  - alert: XBotDown
    expr: up{job="xbot"} == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "XBot instance is down"
      description: "XBot has been down for more than 5 minutes."

  - alert: HighCPUUsage
    expr: cpu_usage_percent > 80
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage on XBot"
      description: "CPU usage is above 80% for more than 10 minutes."

  - alert: TradingErrors
    expr: increase(trading_errors_total[5m]) > 10
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "High number of trading errors"
      description: "More than 10 trading errors in the last 5 minutes."
```

### Dashboard do Grafana

```json
# monitoring/grafana/dashboards/xbot-dashboard.json
{
  "dashboard": {
    "id": null,
    "title": "XBot v2 Monitoring",
    "tags": ["xbot", "trading"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Active Bots",
        "type": "stat",
        "targets": [
          {
            "expr": "xbot_active_bots_total",
            "format": "time_series",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "unit": "short"
          }
        }
      },
      {
        "id": 2,
        "title": "Total Trades (24h)",
        "type": "stat",
        "targets": [
          {
            "expr": "increase(xbot_trades_total[24h])",
            "format": "time_series",
            "refId": "A"
          }
        ]
      },
      {
        "id": 3,
        "title": "Profit/Loss (24h)",
        "type": "stat",
        "targets": [
          {
            "expr": "increase(xbot_profit_usd[24h])",
            "format": "time_series",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "currencyUSD"
          }
        }
      },
      {
        "id": 4,
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(xbot_request_duration_seconds_bucket[5m]))",
            "format": "time_series",
            "refId": "A",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ],
    "time": {
      "from": "now-6h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
```

## 🔒 Segurança em Produção

### Configurações de Segurança

```python
# config/security.py
SECURITY_CONFIG = {
    # API Keys encryption
    'api_key_encryption': True,
    'encryption_algorithm': 'AES-256-GCM',
    
    # Network security
    'allowed_ips': ['192.168.1.0/24', '10.0.0.0/8'],
    'rate_limiting': {
        'requests_per_minute': 60,
        'burst_size': 10
    },
    
    # Authentication
    'jwt_secret': 'your-jwt-secret',
    'jwt_expiry': 3600,
    'api_key_required': True,
    
    # Logging
    'log_api_requests': True,
    'log_trades': True,
    'sensitive_data_masking': True,
    
    # Backup
    'encrypted_backups': True,
    'backup_retention_days': 30,
    
    # Monitoring
    'failed_login_threshold': 5,
    'suspicious_activity_detection': True
}
```

### Certificados SSL

```bash
# Configurar SSL com certbot
sudo certbot --nginx -d your-domain.com

# Renovação automática
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -

# Verificar renovação
sudo certbot renew --dry-run
```

### Firewall Configuration

```bash
# Configurar iptables básico
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT   # SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT   # HTTP
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT  # HTTPS
sudo iptables -A INPUT -j DROP

# Salvar regras
sudo iptables-save > /etc/iptables/rules.v4

# Ou usar UFW (mais simples)
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 📋 Checklist de Deploy

### Pré-Deploy

- [ ] Código testado e validado
- [ ] Configurações de produção revisadas
- [ ] Backup do ambiente anterior
- [ ] Certificados SSL válidos
- [ ] Monitoramento configurado
- [ ] Alertas testados

### Durante o Deploy

- [ ] Manter log detalhado
- [ ] Verificar health checks
- [ ] Testar conectividade externa
- [ ] Validar funcionamento dos bots
- [ ] Confirmar recebimento de alertas

### Pós-Deploy

- [ ] Monitorar logs por 24h
- [ ] Verificar performance
- [ ] Confirmar backups automáticos
- [ ] Documentar alterações
- [ ] Notificar equipe sobre conclusão

## 🆘 Troubleshooting de Deploy

### Problemas Comuns

**Erro: "Port already in use"**
```bash
# Verificar processos usando a porta
sudo lsof -i :8080
sudo netstat -tulpn | grep :8080

# Matar processo se necessário
sudo kill -9 PID
```

**Erro: "Permission denied"**
```bash
# Verificar permissões
ls -la /path/to/xbot-v2

# Ajustar propriedade
sudo chown -R xbot:xbot /path/to/xbot-v2

# Ajustar permissões de execução
chmod +x deploy.sh
```

**Erro: "Database connection failed"**
```bash
# Verificar se database está rodando
sudo systemctl status postgresql

# Testar conexão manual
psql -h localhost -U xbot -d xbot_db

# Verificar configurações no .env
cat .env | grep DATABASE
```

**Erro: "SSL certificate expired"**
```bash
# Verificar status do certificado
sudo certbot certificates

# Renovar certificado
sudo certbot renew

# Reiniciar nginx
sudo systemctl restart nginx
```

## 📚 Scripts Úteis

### Script de Health Check

```bash
#!/bin/bash
# health_check.sh

HEALTH_URL="http://localhost:8080/health"
MAX_RETRIES=5
RETRY_DELAY=10

for i in $(seq 1 $MAX_RETRIES); do
    if curl -f $HEALTH_URL > /dev/null 2>&1; then
        echo "✅ Health check passed"
        exit 0
    else
        echo "❌ Health check failed (attempt $i/$MAX_RETRIES)"
        if [ $i -lt $MAX_RETRIES ]; then
            sleep $RETRY_DELAY
        fi
    fi
done

echo "❌ Health check failed after $MAX_RETRIES attempts"
exit 1
```

### Script de Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/xbot"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
APP_DIR="/home/xbot/xbot-v2"

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
docker-compose exec -T postgres pg_dump -U xbot xbot_db > $BACKUP_DIR/db_$TIMESTAMP.sql

# Backup de configurações
tar -czf $BACKUP_DIR/config_$TIMESTAMP.tar.gz $APP_DIR/.env $APP_DIR/config/

# Backup de logs (últimos 7 dias)
find $APP_DIR/logs -name "*.log" -mtime -7 | tar -czf $BACKUP_DIR/logs_$TIMESTAMP.tar.gz -T -

# Limpeza de backups antigos (manter últimos 30 dias)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "✅ Backup completed: $TIMESTAMP"
```

### Script de Rollback

```bash
#!/bin/bash
# rollback.sh

PREVIOUS_VERSION=$1
if [ -z "$PREVIOUS_VERSION" ]; then
    echo "Usage: ./rollback.sh <previous_version>"
    exit 1
fi

echo "🔄 Rolling back to version $PREVIOUS_VERSION..."

# Parar serviços atuais
docker-compose down

# Checkout versão anterior
git fetch origin
git checkout $PREVIOUS_VERSION

# Restaurar configurações se necessário
if [ -f "backup/config_$PREVIOUS_VERSION.tar.gz" ]; then
    tar -xzf "backup/config_$PREVIOUS_VERSION.tar.gz"
fi

# Rebuild e restart
docker-compose build
docker-compose up -d

# Verificar saúde
sleep 30
./health_check.sh

if [ $? -eq 0 ]; then
    echo "✅ Rollback completed successfully"
else
    echo "❌ Rollback failed - check logs"
    exit 1
fi
```

---

🚀 **Deploy bem feito = Sistema estável! Use este guia para colocar o XBot v2 em produção com segurança.**
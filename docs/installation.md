# 🛠️ Instalação e Configuração

Guia completo para instalar e configurar o XBot v2.

## 📋 Pré-requisitos

### Sistema Operacional
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, CentOS 7+)

### Software Necessário
- **Python 3.8+** (Recomendado: Python 3.11)
- **Git** (para clonar o repositório)
- **Editor de código** (VS Code recomendado)

### Contas Necessárias
- **Conta Binance** com API habilitada
- **Bot Telegram** (opcional, para notificações)

## 🚀 Instalação Rápida

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/xbot-v2.git
cd xbot-v2
```

### 2. Execute o Setup Automático
```bash
python setup.py
```

O script de setup irá:
- ✅ Verificar versão do Python
- ✅ Criar ambiente virtual
- ✅ Instalar dependências
- ✅ Criar estrutura de diretórios
- ✅ Configurar arquivo .env

## 🔧 Instalação Manual

### 1. Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Environment
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

## 🔑 Configuração de Credenciais

### Binance API
1. Acesse [Binance API Management](https://www.binance.com/en/my/settings/api-management)
2. Crie uma nova API Key
3. Habilite permissões de trading
4. Configure IP whitelist (recomendado)
5. Adicione as chaves no arquivo `.env`:

```env
BINANCE_API_KEY=sua_api_key_aqui
BINANCE_SECRET_KEY=sua_secret_key_aqui
BINANCE_TESTNET=true  # Use testnet primeiro
```

### Telegram (Opcional)
1. Crie um bot com [@BotFather](https://t.me/botfather)
2. Obtenha o token do bot
3. Obtenha seu chat ID:
   - Envie uma mensagem para o bot
   - Acesse: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Copie o "chat_id"

```env
TELEGRAM_BOT_TOKEN=seu_bot_token_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
TELEGRAM_NOTIFICATIONS_ENABLED=true
```

## ✅ Verificação da Instalação

### Teste Básico
```bash
python test_xbot.py
```

Saída esperada:
```
✅ Entidades de domínio
✅ Interfaces de domínio  
✅ Configuração
✅ Estratégias pré-definidas
🎉 Todos os testes passaram!
```

### Demo Completo
```bash
python test_xbot.py --demo
```

### Teste do CLI
```bash
python -m src.main --help
```

## 🔧 Configuração Avançada

### Configuração de Log
```env
LOG_LEVEL=INFO
LOG_FILE=./logs/xbot.log
LOG_TO_CONSOLE=true
```

### Configuração de Performance
```env
MARKET_ANALYSIS_INTERVAL=60
SIGNAL_CHECK_INTERVAL=30
API_REQUEST_TIMEOUT=30
```

### Configuração de Backup
```env
AUTO_BACKUP_ENABLED=true
BACKUP_INTERVAL=24
BACKUP_DIR=./backups
```

## 🚨 Testnet vs Mainnet

### Sempre Comece com Testnet
```env
BINANCE_TESTNET=true
```

**Credenciais Testnet:**
- URL: https://testnet.binance.vision/
- Crie conta separada para testes
- Use apenas para desenvolvimento

### Migração para Mainnet
⚠️ **CUIDADO**: Só migre após testes extensivos!

```env
BINANCE_TESTNET=false
```

## 🔍 Troubleshooting

### Erro: "Module not found"
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro de API Key
- Verifique se as chaves estão corretas
- Confirme permissões de trading
- Teste no testnet primeiro

### Problemas de Performance
- Monitore uso de CPU/memória
- Ajuste intervalos de análise
- Configure rate limits

## 📱 Próximos Passos

Após a instalação:
1. 📖 Leia o [Guia de Início Rápido](quick-start.md)
2. 🎯 Configure sua primeira [Estratégia](user-guide/trading-strategies.md)
3. 📊 Configure [Monitoramento](user-guide/monitoring.md)
4. 🛡️ Revise [Gestão de Risco](user-guide/risk-management.md)

---
**Instalação concluída! Ready to trade! 🚀**
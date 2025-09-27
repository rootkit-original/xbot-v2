# 🔒 Segurança

Guia completo de segurança para proteger seus fundos e dados no XBot v2.

## ⚠️ Avisos Importantes de Segurança

### 🚨 NUNCA FAÇA ISSO:
- ❌ **Nunca compartilhe** suas API keys com terceiros
- ❌ **Nunca publique** suas chaves em repositórios públicos
- ❌ **Nunca use** credenciais reais em ambiente de desenvolvimento
- ❌ **Nunca desabilite** permissões de withdraw nas API keys
- ❌ **Nunca execute** o bot em computadores compartilhados
- ❌ **Nunca ignore** alertas de segurança

### ✅ SEMPRE FAÇA ISSO:
- ✅ **Sempre use** API keys somente-leitura quando possível
- ✅ **Sempre mantenha** backup de configurações importantes
- ✅ **Sempre monitore** atividades suspeitas
- ✅ **Sempre atualize** dependências de segurança
- ✅ **Sempre use** 2FA em todas as contas
- ✅ **Sempre teste** em ambiente controlado primeiro

## 🔐 Configuração Segura da Binance API

### Criando API Keys Seguras

#### 1. **Acessar Gerenciamento de API**
1. Entre na sua conta Binance
2. Acesse **API Management** no perfil
3. Clique em **Create API**
4. Nome sugestivo: `XBot-Trading-Restricted`

#### 2. **Configurar Permissões (CRÍTICO)**

```bash
Permissões Recomendadas:
✅ Read Info                    # Ler informações da conta
✅ Spot & Margin Trading       # Trading spot (se necessário)
✅ Futures Trading            # Trading futures (se necessário)
❌ Enable Withdrawals         # NUNCA HABILITAR
❌ Enable Internal Transfer   # NUNCA HABILITAR
❌ Read Key                   # Não necessário
```

#### 3. **Restrições de IP (OBRIGATÓRIO)**

```bash
# Configurar IP fixo do seu servidor
IP Restrictions:
✅ Restrict access to trusted IPs only
📍 Adicionar IP: [seu-ip-fixo]
📍 Adicionar IP: [ip-backup] (opcional)

# Verificar seu IP atual
curl ifconfig.me
```

#### 4. **Configurar Outras Restrições**

```bash
Configurações Adicionais:
✅ Enable Spot & Margin Trading
✅ Enable Futures Trading (se necessário)
❌ Enable Withdrawals (MANTER DESABILITADO)
❌ Enable Internal Transfer (MANTER DESABILITADO)
✅ IP Access Restriction (OBRIGATÓRIO)
```

### Testando API Keys

```bash
# Testar conectividade
python -m src.main test-connection --api-key YOUR_KEY --secret YOUR_SECRET

# Testar permissões
python -m src.main test-permissions

# Verificar restrições
python -m src.main verify-restrictions
```

## 🛡️ Configuração Segura do Sistema

### Variáveis de Ambiente

```bash
# .env (NUNCA COMMITTAR)
BINANCE_API_KEY=sua_api_key_aqui
BINANCE_SECRET_KEY=seu_secret_aqui
TELEGRAM_BOT_TOKEN=bot_token_aqui
TELEGRAM_CHAT_ID=chat_id_aqui

# Configurar permissões do arquivo
chmod 600 .env  # Somente leitura para o proprietário

# Adicionar ao .gitignore
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "config/secrets/*" >> .gitignore
```

### Criptografia Local

```bash
# Ativar criptografia de configurações
python -m src.main config --encrypt-settings true
python -m src.main config --set-master-password

# Descriptografar quando necessário
python -m src.main config --decrypt-settings
```

### Configuração de Logs Seguros

```bash
# Configurar logs sem informações sensíveis
python -m src.main config --log-level INFO  # Não usar DEBUG em produção
python -m src.main config --mask-sensitive-data true
python -m src.main config --log-retention 30  # Manter logs por 30 dias

# Configurar rotação de logs
python -m src.main config --log-rotation daily
python -m src.main config --log-max-size 100MB
```

## 🔒 Autenticação e Controle de Acesso

### Configurar Senha Master

```bash
# Definir senha master para o bot
python -m src.main auth set-master-password

# Alterar senha
python -m src.main auth change-password

# Verificar autenticação
python -m src.main auth verify
```

### Controle de Acesso por IP

```bash
# Configurar IPs permitidos
python -m src.main config --allowed-ips "192.168.1.100,10.0.0.50"

# Bloquear IPs específicos
python -m src.main config --blocked-ips "suspicious-ip-here"

# Verificar tentativas de acesso
python -m src.main auth access-log
```

### Token JWT para API

```bash
# Gerar token JWT para acesso API
python -m src.main auth generate-jwt --expires-in 3600

# Revogar tokens
python -m src.main auth revoke-token [token-id]

# Listar tokens ativos
python -m src.main auth list-tokens
```

## 🚨 Monitoramento de Segurança

### Alertas de Segurança

```bash
# Configurar alertas críticos
python -m src.main alerts add-security \
  --name "API Key Compromise" \
  --condition "unusual_api_activity" \
  --priority critical

python -m src.main alerts add-security \
  --name "Large Position" \
  --condition "position_size > 10000" \
  --priority high

python -m src.main alerts add-security \
  --name "Failed Login" \
  --condition "failed_auth > 3" \
  --priority medium
```

### Log de Auditoria

```bash
# Visualizar logs de segurança
python -m src.main security audit-log --days 7

# Verificar atividades suspeitas
python -m src.main security detect-anomalies

# Relatório de segurança
python -m src.main security report --send-email
```

### Monitoramento de API

```python
# Exemplo de monitoramento de API
security_monitors = {
    "api_rate_limit": {
        "threshold": 1000,  # requests per minute
        "action": "alert"
    },
    "unusual_trading_volume": {
        "threshold": "3x_average",
        "action": "pause_bot"
    },
    "api_errors": {
        "threshold": 10,  # errors per hour
        "action": "alert_and_pause"
    },
    "position_size": {
        "threshold": 50000,  # USD
        "action": "require_confirmation"
    }
}
```

## 🔐 Backup e Recuperação

### Backup Seguro

```bash
# Backup automático (sem chaves sensíveis)
python -m src.main backup create --exclude-secrets

# Backup completo criptografado
python -m src.main backup create --encrypt --password

# Agendar backups
python -m src.main backup schedule --frequency daily --keep 30
```

### Recuperação de Emergência

```bash
# Restaurar configurações
python -m src.main restore --backup-file backup_2024-03-15.enc

# Recuperar bots específicos
python -m src.main restore --bot-name "Critical Bot" --backup-file backup.enc

# Modo de recuperação
python -m src.main recovery-mode --safe-shutdown
```

### Chaves de Recuperação

```bash
# Gerar chave de recuperação
python -m src.main auth generate-recovery-key

# Usar chave de recuperação
python -m src.main auth recover --recovery-key [key]

# Desabilitar chave de recuperação
python -m src.main auth disable-recovery-key
```

## 🛡️ Hardening do Sistema

### Configurações de Sistema

```bash
# Configurar timeouts de segurança
python -m src.main config --session-timeout 3600
python -m src.main config --inactivity-timeout 1800

# Configurar limites de taxa
python -m src.main config --rate-limit-requests 100
python -m src.main config --rate-limit-window 60

# Ativar modo paranoid (extra segurança)
python -m src.main config --paranoid-mode true
```

### Firewall e Rede

```bash
# Configurar firewall (Linux)
sudo ufw allow from [trusted-ip] to any port 8080
sudo ufw deny 8080

# Configurar proxy (se necessário)
python -m src.main config --proxy socks5://proxy-server:1080

# Verificar conectividade segura
python -m src.main network verify-ssl
```

### Atualizações de Segurança

```bash
# Verificar atualizações de segurança
python -m src.main security check-updates

# Atualizar dependências críticas
pip install --upgrade requests urllib3 cryptography

# Verificar vulnerabilidades conhecidas
python -m src.main security scan-vulnerabilities
```

## 🔍 Detecção de Anomalias

### Monitoramento Comportamental

```python
# Configurar detecção de anomalias
anomaly_detection = {
    "trading_patterns": {
        "max_trades_per_hour": 100,
        "max_position_size": 10000,
        "unusual_symbols": "alert_on_new"
    },
    "api_usage": {
        "max_requests_per_minute": 200,
        "unusual_endpoints": "log_and_alert",
        "geographic_anomalies": true
    },
    "account_activity": {
        "login_patterns": "detect_unusual",
        "configuration_changes": "require_confirmation",
        "new_device_access": "block_and_alert"
    }
}
```

### Machine Learning para Segurança

```bash
# Treinar modelo de detecção de anomalias
python -m src.main security train-anomaly-model --data-days 90

# Executar detecção em tempo real
python -m src.main security enable-ml-monitoring

# Ajustar sensibilidade
python -m src.main security set-anomaly-threshold 0.95
```

## 📱 Segurança do Telegram

### Configuração Segura do Bot

```bash
# Criar bot Telegram com configurações seguras
# 1. Fale com @BotFather
# 2. Use /newbot
# 3. Nome: XBot_Trading_[username]_Bot (não use nome genérico)

# Configurar privacidade
python -m src.main telegram set-privacy-mode true

# Configurar whitelist de usuários
python -m src.main telegram add-authorized-user [user_id]
python -m src.main telegram remove-authorized-user [user_id]
```

### Comandos Seguros

```python
# Exemplo de comandos com autenticação
secure_commands = {
    "/start": "public",      # Qualquer um pode usar
    "/help": "public",       # Informações gerais
    "/status": "private",    # Apenas usuários autorizados
    "/stop_bot": "admin",    # Apenas administradores
    "/emergency": "owner"    # Apenas proprietário
}
```

## 🚨 Protocolo de Emergência

### Detecção de Comprometimento

```bash
# Sinais de comprometimento:
# - Trades não autorizados
# - Logins de IPs desconhecidos
# - Configurações alteradas sem sua ação
# - API errors excessivos
# - Alertas de segurança da Binance

# Ação imediata:
python -m src.main emergency shutdown-all-bots
python -m src.main emergency revoke-api-keys
python -m src.main emergency notify-admin
```

### Plano de Resposta a Incidentes

#### Nível 1 - Suspeita de Atividade
```bash
# 1. Pausar todos os bots
python -m src.main emergency pause-all

# 2. Revisar logs
python -m src.main security audit-log --urgent

# 3. Verificar posições
python -m src.main portfolio emergency-review
```

#### Nível 2 - Comprometimento Confirmado
```bash
# 1. Shutdown imediato
python -m src.main emergency total-shutdown

# 2. Revogar API keys
# - Acesse Binance > API Management
# - Delete todas as API keys do XBot

# 3. Alterar todas as senhas
# - Binance account
# - Email account
# - Telegram account

# 4. Notificar authorities se necessário
```

#### Nível 3 - Perda Financeira
```bash
# 1. Documentar todas as evidências
python -m src.main security export-incident-report

# 2. Contatar suporte Binance
# 3. Considerar relatório policial
# 4. Revisar todos os sistemas de segurança
```

## 🔧 Ferramentas de Segurança

### Scanner de Vulnerabilidades

```bash
# Verificar configurações de segurança
python -m src.main security scan --comprehensive

# Verificar dependências
python -m src.main security check-dependencies

# Teste de penetração básico
python -m src.main security pentest --basic
```

### Análise Forense

```bash
# Analisar logs suspeitos
python -m src.main forensics analyze-logs --suspicious

# Reconstruir timeline de eventos
python -m src.main forensics timeline --date 2024-03-15

# Exportar evidências
python -m src.main forensics export-evidence --case-id [case_id]
```

## 📋 Checklist de Segurança

### Configuração Inicial
- [ ] API keys criadas com permissões mínimas
- [ ] Withdrawals desabilitados na Binance
- [ ] IP restrictions configuradas
- [ ] Arquivo .env com permissões corretas (600)
- [ ] Master password definida
- [ ] Backup inicial criado

### Monitoramento Diário
- [ ] Verificar logs de segurança
- [ ] Revisar alertas de anomalias
- [ ] Confirmar posições abertas
- [ ] Verificar saldo da conta
- [ ] Monitorar uso de API

### Manutenção Semanal
- [ ] Atualizar dependências
- [ ] Rotacionar logs antigos
- [ ] Backup incremental
- [ ] Revisar configurações de segurança
- [ ] Testar procedimentos de emergência

### Auditoria Mensal
- [ ] Audit completo de segurança
- [ ] Revisar permissões de usuários
- [ ] Atualizar plano de resposta a incidentes
- [ ] Treinar cenários de emergência
- [ ] Revisar e atualizar documentação

## ⚡ Configuração Rápida e Segura

### Setup Seguro em 5 Minutos

```bash
# 1. Configurar variáveis de ambiente
cp .env.example .env
nano .env  # Editar com suas credenciais
chmod 600 .env

# 2. Ativar segurança básica
python -m src.main security quick-setup

# 3. Testar configurações
python -m src.main security verify-setup

# 4. Configurar alertas críticos
python -m src.main alerts setup-security-defaults

# 5. Criar backup inicial
python -m src.main backup create --initial
```

### Configuração Avançada

```bash
# Para usuários experientes
python -m src.main security advanced-setup \
  --enable-encryption \
  --setup-2fa \
  --configure-monitoring \
  --create-recovery-keys
```

## 🎯 Resumo das Melhores Práticas

### 🥇 **Essencial (Obrigatório)**
1. **Nunca habilitar withdrawals** nas API keys
2. **Sempre usar IP restrictions**
3. **Manter arquivos de configuração seguros**
4. **Monitorar logs regularmente**
5. **Fazer backups frequentes**

### 🥈 **Recomendado (Importante)**
1. **Usar 2FA em todas as contas**
2. **Criptografar configurações sensíveis**
3. **Configurar alertas de segurança**
4. **Manter sistema atualizado**
5. **Testar procedimentos de emergência**

### 🥉 **Opcional (Avançado)**
1. **Usar proxy/VPN dedicado**
2. **Implementar honeypots**
3. **Análise comportamental avançada**
4. **Auditoria de terceiros**
5. **Seguro de criptomoedas**

---

🔒 **A segurança dos seus fundos é sua responsabilidade - nunca comprometa na proteção!**
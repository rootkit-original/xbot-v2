# 🔧 Troubleshooting

Guia completo para resolução de problemas comuns no XBot v2.

## 🎯 Problemas Mais Comuns

### 📊 Quick Fix - Soluções Rápidas

| Problema | Solução Rápida | Comando |
|----------|---------------|---------|
| Bot não inicia | Verificar configuração | `python -m src.main config --validate` |
| API Error 401 | Reconfigurar API keys | `python -m src.main config --binance-setup` |
| Conexão perdida | Testar conectividade | `python -m src.main test-connection` |
| Bot travado | Restart forçado | `python -m src.main restart --force` |
| Logs não aparecem | Verificar permissões | `python -m src.main logs --check-permissions` |

## 🚨 Problemas de Conexão

### Erro: "Connection timeout"

```bash
# Sintomas:
TimeoutError: Connection timeout after 30 seconds

# Diagnóstico:
python -m src.main diagnose connection

# Soluções:
1. Verificar conexão com internet
2. Testar conectividade com Binance
3. Verificar firewall/proxy
4. Aumentar timeout
```

**Soluções passo a passo:**

```bash
# 1. Testar conectividade básica
ping api.binance.com

# 2. Testar conectividade do bot
python -m src.main test-connection --verbose

# 3. Configurar timeout maior
python -m src.main config --connection-timeout 60

# 4. Configurar retry
python -m src.main config --max-retries 5
```

### Erro: "SSL Certificate verification failed"

```bash
# Sintomas:
ssl.SSLCertVerificationError: certificate verify failed

# Soluções:
# 1. Atualizar certificados
pip install --upgrade certifi requests

# 2. Verificar sistema
python -m src.main system verify-ssl

# 3. Configurar SSL (se necessário)
python -m src.main config --ssl-verify true
```

### Erro: "API rate limit exceeded"

```bash
# Sintomas:
BinanceAPIException: Rate limit exceeded

# Diagnóstico:
python -m src.main diagnose api-limits

# Soluções:
1. Reduzir frequência de requests
2. Implementar backoff exponencial
3. Verificar outros bots na mesma API
```

**Configuração de rate limiting:**

```bash
# Configurar limits conservadores
python -m src.main config --api-rate-limit 1000  # per minute
python -m src.main config --request-delay 0.1    # seconds between requests
python -m src.main config --backoff-factor 2     # exponential backoff
```

## 🔑 Problemas de Autenticação

### Erro: "Invalid API key"

```bash
# Sintomas:
BinanceAPIException: Invalid API-key, IP, or permissions

# Diagnóstico:
python -m src.main diagnose api-auth

# Verificações:
1. API key está correta
2. Secret key está correto
3. IP está autorizado
4. Permissões estão adequadas
```

**Solução completa:**

```bash
# 1. Verificar configuração atual
python -m src.main config --show-api-config

# 2. Reconfigurar API keys
python -m src.main config --binance-api-key "nova_key"
python -m src.main config --binance-secret "novo_secret"

# 3. Testar autenticação
python -m src.main test-auth

# 4. Verificar permissões na Binance
# Acesse: Binance > API Management > Verificar permissões
```

### Erro: "Timestamp for this request is outside the recvWindow"

```bash
# Sintomas:
BinanceAPIException: Timestamp for this request is outside the recvWindow

# Causa: Relógio do sistema desatualizado

# Solução:
# Windows:
w32tm /resync

# Linux:
sudo ntpdate -s time.nist.gov

# Verificar sincronização:
python -m src.main system check-time
```

## 💰 Problemas de Trading

### Erro: "Insufficient funds"

```bash
# Sintomas:
BinanceAPIException: Account has insufficient balance

# Diagnóstico:
python -m src.main diagnose balance

# Verificações:
1. Saldo disponível na conta
2. Ordens abertas bloqueando saldo
3. Configuração de capital do bot
```

**Soluções:**

```bash
# 1. Verificar saldo atual
python -m src.main balance --detailed

# 2. Cancelar ordens pendentes
python -m src.main cancel-all-orders --confirm

# 3. Ajustar capital do bot
python -m src.main bot update "Bot Name" --capital 500

# 4. Liberar fundos reservados
python -m src.main balance release-reserved
```

### Erro: "Order would trigger immediately"

```bash
# Sintomas:
BinanceAPIException: Order would trigger immediately

# Causa: Preço de ordem muito próximo do preço atual

# Solução:
python -m src.main config --order-buffer 0.1  # 0.1% buffer
python -m src.main config --price-precision 4  # precisão de preço
```

### Bot não está fazendo trades

```bash
# Diagnóstico completo:
python -m src.main diagnose trading-issues

# Verificações comuns:
1. Bot está rodando?
2. Estratégia está ativa?
3. Condições de mercado atendem critérios?
4. Capital suficiente disponível?
5. Símbolos estão corretos?
```

**Checklist de troubleshooting:**

```bash
# 1. Verificar status do bot
python -m src.main status --bot-name "Seu Bot"

# 2. Verificar logs em tempo real
python -m src.main logs --follow --bot "Seu Bot"

# 3. Verificar condições da estratégia
python -m src.main strategy analyze "sua_estrategia" --symbol BTCUSDT

# 4. Forçar análise manual
python -m src.main analyze --symbol BTCUSDT --force
```

## 📱 Problemas do Telegram

### Bot Telegram não responde

```bash
# Verificações:
1. Token está correto?
2. Bot está inicializado?
3. Chat ID está correto?
4. Bot foi adicionado ao chat?

# Diagnóstico:
python -m src.main diagnose telegram

# Testar conectividade:
python -m src.main test-telegram --verbose
```

**Soluções:**

```bash
# 1. Reconfigurar Telegram
python -m src.main config --telegram-token "novo_token"
python -m src.main config --telegram-chat-id "novo_chat_id"

# 2. Reinicializar bot Telegram
python -m src.main telegram restart

# 3. Verificar permissões
python -m src.main telegram check-permissions
```

### Alertas não chegam

```bash
# Verificar configuração de alertas:
python -m src.main alerts list --active

# Testar alerta específico:
python -m src.main alerts test --alert-name "Trade Alert"

# Verificar filtros:
python -m src.main alerts show-filters
```

## 🗄️ Problemas de Database

### Erro: "Database is locked"

```bash
# Sintomas:
sqlite3.OperationalError: database is locked

# Soluções:
1. Fechar todas as instâncias do bot
2. Verificar processos em background
3. Remover lock files
```

**Recuperação de database:**

```bash
# 1. Parar todos os bots
python -m src.main stop --all --force

# 2. Verificar processos
ps aux | grep python  # Linux/Mac
tasklist | findstr python  # Windows

# 3. Remover locks
rm *.db-wal *.db-shm  # Linux/Mac
del *.db-wal *.db-shm  # Windows

# 4. Verificar integridade
python -m src.main database check-integrity

# 5. Reparar se necessário
python -m src.main database repair
```

### Dados corrompidos

```bash
# Sintomas:
- Bots desaparecendo
- Histórico de trades inconsistente
- Erros de integridade

# Recuperação:
python -m src.main database backup  # Backup antes de reparar
python -m src.main database repair --force
python -m src.main database rebuild --from-backup
```

## 🔍 Problemas de Performance

### Bot muito lento

```bash
# Diagnóstico de performance:
python -m src.main diagnose performance

# Métricas principais:
1. CPU usage
2. Memory usage
3. Disk I/O
4. Network latency
```

**Otimizações:**

```bash
# 1. Otimizar configurações
python -m src.main optimize --auto

# 2. Reduzir frequência de análise
python -m src.main config --analysis-interval 60  # segundos

# 3. Limpar logs antigos
python -m src.main cleanup --logs --older-than 30

# 4. Otimizar database
python -m src.main database optimize
```

### Alto uso de CPU/Memória

```bash
# Monitoramento de recursos:
python -m src.main monitor system --detailed

# Configurações para reduzir uso:
python -m src.main config --max-threads 4
python -m src.main config --memory-limit 1024  # MB
python -m src.main config --gc-frequency 300   # garbage collection
```

## 📊 Problemas de Estratégias

### Estratégia não funciona como esperado

```bash
# Análise detalhada da estratégia:
python -m src.main strategy debug "scalping_conservative" --symbol BTCUSDT

# Verificar indicadores:
python -m src.main indicators test --symbol BTCUSDT --period 24h

# Comparar com backtest:
python -m src.main backtest strategy "scalping_conservative" --recent
```

### Parâmetros da estratégia

```bash
# Ver parâmetros atuais:
python -m src.main strategy show-params "sua_estrategia"

# Ajustar parâmetros:
python -m src.main bot update "Seu Bot" --stop-loss 1.5 --take-profit 3.0

# Resetar para padrão:
python -m src.main strategy reset-params "sua_estrategia"
```

## 🛠️ Ferramentas de Diagnóstico

### Diagnóstico Completo do Sistema

```bash
# Executar diagnóstico completo:
python -m src.main diagnose --comprehensive

# Salvar relatório:
python -m src.main diagnose --save-report diagnosis_report.txt

# Enviar relatório por email:
python -m src.main diagnose --email-report support@xbot.com
```

### Health Check

```bash
# Verificação rápida de saúde:
python -m src.main health-check

# Health check detalhado:
python -m src.main health-check --detailed --save-report
```

**Exemplo de saída:**

```text
XBot v2 Health Check Report
===========================
✅ System Resources: OK
✅ Database Connection: OK  
✅ Binance API: OK
✅ Telegram Bot: OK
⚠️  High CPU Usage: 85%
❌ Network Latency: High (>500ms)

Recommendations:
- Consider optimizing bot configurations
- Check network connection
- Monitor system resources
```

### System Information

```bash
# Informações detalhadas do sistema:
python -m src.main system info

# Verificar dependências:
python -m src.main system check-dependencies

# Verificar versões:
python -m src.main system versions
```

## 🔧 Ferramentas de Recuperação

### Recovery Mode

```bash
# Modo de recuperação seguro:
python -m src.main recovery-mode

# Opções disponíveis em recovery mode:
1. Safe shutdown all bots
2. Reset configurations
3. Repair database
4. Export logs
5. Create emergency backup
```

### Emergency Tools

```bash
# Parada de emergência:
python -m src.main emergency stop-all

# Cancelar todas as ordens:
python -m src.main emergency cancel-orders --confirm

# Backup de emergência:
python -m src.main emergency backup

# Reset completo (cuidado!):
python -m src.main emergency reset --confirm-destruction
```

## 📋 Checklist de Troubleshooting

### Antes de Reportar um Bug

- [ ] Tentei reiniciar o bot?
- [ ] Verifiquei os logs de erro?
- [ ] Testei a conectividade?
- [ ] Confirmei que as configurações estão corretas?
- [ ] Tentei as soluções sugeridas neste guia?
- [ ] Executei o diagnóstico completo?

### Informações para Incluir no Report

```bash
# Gerar relatório completo para suporte:
python -m src.main support generate-report

# Relatório contém:
1. System information
2. Error logs
3. Configuration (sem dados sensíveis)
4. Recent activity
5. Performance metrics
```

## 🆘 Suporte e Comunidade

### Recursos de Ajuda

- 📧 **Email Support**: support@xbot-trading.com
- 💬 **Discord**: [Discord Community](https://discord.gg/xbot-trading)
- 📱 **Telegram Group**: [@xbot_trading](https://t.me/xbot_trading)
- 🐛 **GitHub Issues**: [Report Bug](https://github.com/rootkit-original/xbot-v2/issues)
- 📚 **Documentation**: [Full Docs](https://docs.xbot-trading.com)

### FAQ Rápido

**Q: Bot parou de funcionar do nada**
A: Execute `python -m src.main diagnose --quick` e verifique logs

**Q: Não recebo alertas no Telegram**
A: Teste com `python -m src.main test-telegram --verbose`

**Q: API keys não funcionam**
A: Verifique IP whitelist na Binance e permissões da API

**Q: Performance muito lenta**
A: Execute `python -m src.main optimize --auto`

**Q: Database corrompido**
A: Use `python -m src.main database repair --backup-first`

### Como Reportar Bugs Efetivamente

```bash
# 1. Gerar relatório de diagnóstico
python -m src.main diagnose --comprehensive --save-report

# 2. Incluir no relatório:
- Versão do XBot v2
- Sistema operacional
- Versão do Python
- Logs de erro
- Passos para reproduzir
- Comportamento esperado vs atual

# 3. Enviar para:
- GitHub Issues (bugs técnicos)
- Discord (dúvidas gerais)
- Email (problemas críticos)
```

## 🎯 Dicas de Prevenção

### Manutenção Preventiva

```bash
# Executar semanalmente:
python -m src.main maintenance weekly

# Limpeza mensal:
python -m src.main cleanup --comprehensive

# Backup automático:
python -m src.main config --auto-backup daily
```

### Monitoramento Proativo

```bash
# Configurar alertas preventivos:
python -m src.main alerts add --name "High CPU" --condition "cpu_usage > 80"
python -m src.main alerts add --name "Low Disk" --condition "disk_free < 1GB"
python -m src.main alerts add --name "Memory Leak" --condition "memory_usage > 2GB"
```

---

🔧 **Problemas resolvidos = Trading mais estável! Use este guia como referência rápida.**
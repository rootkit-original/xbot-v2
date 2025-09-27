# ❓ FAQ - Perguntas Frequentes

Respostas às perguntas mais comuns sobre o XBot v2.

## 🎯 Sobre o XBot v2

### O que é o XBot v2?

O XBot v2 é um sistema completo de trading automatizado para criptomoedas, desenvolvido com Clean Architecture e projetado para ser robusto, escalável e fácil de usar. Ele suporta múltiplas estratégias de trading, oferece notificações via Telegram e possui um sistema avançado de gerenciamento de risco.

### Que exchanges são suportadas?

Atualmente o XBot v2 suporta:
- ✅ **Binance** (Spot Trading) - Totalmente integrado
- 🔄 **Binance Futures** - Em desenvolvimento
- 📋 **Outras exchanges** - Planejado para versões futuras

### Preciso de conhecimento técnico para usar?

**Básico**: Não precisa ser programador, mas é necessário:
- Conhecimento básico de terminal/linha de comando
- Entender conceitos básicos de trading
- Conseguir seguir instruções de instalação

**Avançado**: Para personalizar estratégias ou desenvolver novas funcionalidades, é recomendável conhecimento em Python.

## 🚀 Instalação e Configuração

### Quais são os requisitos mínimos?

**Sistema Operacional:**
- Windows 10+ / Linux / macOS
- Mínimo 4GB RAM
- 1GB espaço em disco
- Conexão estável com internet

**Software:**
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Como instalar o XBot v2?

```bash
# 1. Clonar repositório
git clone https://github.com/rootkit-original/xbot-v2.git
cd xbot-v2

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar
python -m src.main config --setup
```

### Como configurar as API keys da Binance?

```bash
# Configuração interativa
python -m src.main config --binance-setup

# Ou configuração manual
python -m src.main config --binance-api-key "sua_api_key"
python -m src.main config --binance-secret "seu_secret"
```

**⚠️ Importante**: Na Binance, configure sua API key com:
- ✅ Enable Reading
- ✅ Enable Spot & Margin Trading
- ❌ Enable Futures (desnecessário)
- ✅ Restrict access to trusted IPs (recomendado)

### Preciso do Telegram para usar o bot?

**Não é obrigatório**, mas é **altamente recomendado** porque:
- Recebe alertas em tempo real
- Monitora desempenho remotamente
- Controla bots via comandos
- Recebe relatórios diários

**Como configurar:**

```bash
# 1. Criar bot no Telegram (@BotFather)
# 2. Obter token
# 3. Configurar no XBot
python -m src.main config --telegram-token "seu_token"
python -m src.main config --telegram-chat-id "seu_chat_id"
```

## 💰 Trading e Estratégias

### Quais estratégias estão disponíveis?

O XBot v2 inclui 7 estratégias prontas:

1. **Scalping Conservative** - Para mercados estáveis
2. **Scalping Aggressive** - Para alta volatilidade
3. **Mean Reversion** - Reversão à média
4. **Momentum** - Segue tendências
5. **DCA (Dollar Cost Average)** - Compra gradual
6. **Grid Trading** - Grade de ordens
7. **Swing Trading** - Operações de médio prazo

### Qual estratégia escolher?

**Para iniciantes**: Scalping Conservative ou DCA
**Para experientes**: Mean Reversion ou Momentum
**Para mercados laterais**: Grid Trading
**Para tendências**: Swing Trading

```bash
# Comparar estratégias com backtest
python -m src.main backtest compare --period 30d --symbol BTCUSDT
```

### Posso usar múltiplas estratégias?

**Sim!** Você pode:
- Executar diferentes estratégias em símbolos diferentes
- Usar múltiplas estratégias no mesmo símbolo (com cuidado)
- Alternar estratégias baseado em condições de mercado

```bash
# Criar bot com múltiplas estratégias
python -m src.main bot create "Multi Bot" \
    --strategy scalping_conservative \
    --symbols BTCUSDT,ETHUSDT \
    --capital 1000
```

### Como definir o capital para cada bot?

**Regra geral**: Nunca invista mais do que pode perder

**Recomendações:**
- Iniciantes: $100-500 por bot
- Intermediário: $500-2000 por bot
- Avançado: Baseado em gestão de risco

```bash
# Configurar capital
python -m src.main bot create "Meu Bot" --capital 500
python -m src.main bot update "Meu Bot" --capital 750  # Ajustar depois
```

### O bot opera 24/7?

**Sim**, o bot pode operar continuamente, mas você pode:

```bash
# Configurar horários de operação
python -m src.main bot update "Meu Bot" \
    --trading-hours "08:00-22:00" \
    --timezone "America/Sao_Paulo"

# Pausar temporariamente
python -m src.main bot pause "Meu Bot"

# Pausar em finais de semana
python -m src.main config --weekend-trading false
```

## 📊 Gestão de Risco

### Como configurar stop-loss e take-profit?

```bash
# Configurações padrão (recomendado para iniciantes)
python -m src.main bot update "Meu Bot" \
    --stop-loss 2.0 \      # 2% perda máxima
    --take-profit 4.0 \    # 4% lucro alvo
    --risk-per-trade 1.0   # 1% do capital por trade
```

**Configurações por nível:**
- **Conservador**: Stop-loss 1.5%, Take-profit 3%
- **Moderado**: Stop-loss 2%, Take-profit 4%
- **Agressivo**: Stop-loss 3%, Take-profit 6%

### Como o bot gerencia risco?

**Gestão automática de risco:**
- Cálculo automático do tamanho da posição
- Monitoramento contínuo de drawdown
- Parada automática em perdas excessivas
- Diversificação entre símbolos

```bash
# Configurar limites de risco
python -m src.main config \
    --max-daily-loss 5.0 \     # Parar se perder 5% no dia
    --max-drawdown 10.0 \      # Parar se drawdown > 10%
    --max-open-positions 5     # Máximo 5 posições abertas
```

### Posso limitar as perdas diárias?

**Sim!** Configurações de proteção:

```bash
# Limitar perdas
python -m src.main bot update "Meu Bot" \
    --daily-loss-limit 50 \    # $50 perda máxima por dia
    --weekly-loss-limit 200 \  # $200 perda máxima por semana
    --monthly-loss-limit 500   # $500 perda máxima por mês
```

## 📱 Monitoramento e Alertas

### Como monitorar o desempenho?

**Dashboard Web:**
```bash
python -m src.main dashboard --start
# Acesse: http://localhost:8080
```

**Relatórios via Telegram:**
```bash
# Configurar relatórios automáticos
python -m src.main config \
    --daily-report true \
    --weekly-report true \
    --report-time "09:00"
```

**Logs em tempo real:**
```bash
python -m src.main logs --follow --bot "Meu Bot"
```

### Que tipos de alertas posso receber?

**Alertas automáticos:**
- ✅ Trade executado
- ⚠️ Stop-loss ativado
- 🎯 Take-profit atingido
- ❌ Erro crítico
- 📊 Relatório de performance
- 🔴 Limite de perda atingido

**Configurar alertas personalizados:**
```bash
python -m src.main alerts add \
    --name "Lucro Alto" \
    --condition "daily_profit > 5%" \
    --message "🎉 Lucro diário acima de 5%!"
```

### Como receber notificações no celular?

**Via Telegram** (recomendado):
1. Configure o bot do Telegram
2. Alertas chegam instantaneamente
3. Controle bots via comandos

**Via Email:**
```bash
python -m src.main config \
    --email-alerts true \
    --email-recipient "seu@email.com"
```

**Via Webhook:**
```bash
python -m src.main config \
    --webhook-url "https://seu-webhook.com/alerts"
```

## 🔧 Troubleshooting

### Bot não está fazendo trades

**Verificações básicas:**

```bash
# 1. Verificar se bot está rodando
python -m src.main status

# 2. Verificar saldo
python -m src.main balance

# 3. Verificar condições de mercado
python -m src.main analyze --symbol BTCUSDT

# 4. Verificar logs
python -m src.main logs --recent --bot "Meu Bot"
```

**Possíveis causas:**
- Saldo insuficiente
- Condições de mercado não atendem critérios
- Bot pausado ou parado
- Problemas de conectividade

### Erro de API key inválida

```bash
# Verificar configuração
python -m src.main config --show-api-config

# Testar conectividade
python -m src.main test-auth

# Reconfigurar se necessário
python -m src.main config --binance-setup
```

### Bot muito lento ou travando

```bash
# Diagnóstico de performance
python -m src.main diagnose performance

# Otimizar configurações
python -m src.main optimize --auto

# Limpar dados antigos
python -m src.main cleanup --logs --trades
```

### Não recebo alertas no Telegram

```bash
# Testar bot do Telegram
python -m src.main test-telegram

# Verificar configuração
python -m src.main config --show-telegram-config

# Reconfigurar se necessário
python -m src.main config --telegram-setup
```

## 💡 Boas Práticas

### Como começar com segurança?

1. **Comece pequeno**: Use capital que pode perder
2. **Teste em papel**: Use modo simulação primeiro
3. **Uma estratégia**: Comece com uma estratégia simples
4. **Monitor frequente**: Acompanhe nas primeiras semanas
5. **Educação contínua**: Aprenda sobre trading e mercados

```bash
# Modo simulação (recomendado para iniciantes)
python -m src.main bot create "Teste" \
    --strategy scalping_conservative \
    --capital 1000 \
    --simulation-mode true
```

### Dicas para otimizar resultados

**Diversificação:**
```bash
# Múltiplos pares para reduzir risco
python -m src.main bot create "Diversificado" \
    --symbols BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT \
    --capital 2000
```

**Rebalanceamento:**
```bash
# Rebalancear automaticamente
python -m src.main config --auto-rebalance daily
```

**Ajustes baseados em performance:**
```bash
# Análise de performance
python -m src.main analyze performance --bot "Meu Bot" --period 30d

# Otimizar parâmetros baseado no histórico
python -m src.main optimize parameters --bot "Meu Bot"
```

### Erros comuns a evitar

❌ **Não fazer:**
- Investir mais do que pode perder
- Usar apenas uma estratégia em um mercado
- Ignorar stop-loss
- Não monitorar regularmente
- Alterar parâmetros constantemente

✅ **Fazer:**
- Começar com capital pequeno
- Diversificar estratégias e símbolos
- Usar gestão de risco adequada
- Monitorar e ajustar gradualmente
- Manter disciplina

## 🎓 Educação e Recursos

### Onde aprender mais sobre trading?

**Recursos gratuitos:**
- 📚 [Binance Academy](https://academy.binance.com/)
- 📺 YouTube: Canais de educação financeira
- 📖 Livros: "A Random Walk Down Wall Street"
- 💬 Comunidades: Discord/Telegram do XBot

**Recursos pagos:**
- 🎓 Cursos especializados de trading
- 📊 Análise técnica avançada
- 🧠 Psicologia do trading

### Como entender os indicadores técnicos?

**Indicadores básicos no XBot:**
- **RSI**: Sobrecompra/sobrevenda
- **MACD**: Momentum e tendência
- **MA**: Médias móveis para trend
- **Bollinger Bands**: Volatilidade e suporte/resistência

```bash
# Analisar indicadores para um símbolo
python -m src.main indicators analyze BTCUSDT --period 24h
```

### Posso criar minhas próprias estratégias?

**Sim!** O XBot v2 é extensível:

```python
# Exemplo de estratégia personalizada
from src.domain.entities.strategy import BaseStrategy

class MinhaEstrategia(BaseStrategy):
    def should_buy(self, data):
        # Sua lógica de compra
        return True
    
    def should_sell(self, data):
        # Sua lógica de venda
        return False
```

**Recursos para desenvolvedores:**
- 📖 [Developer Guide](developer-guide/architecture.md)
- 🔧 [API Documentation](api/endpoints.md)
- 💻 [Strategy Examples](strategies/examples.md)

## 💰 Custos e Taxas

### Quanto custa usar o XBot v2?

**XBot v2 é gratuito e open-source!**

**Custos associados:**
- 💱 **Taxas da Exchange**: Binance cobra ~0.1% por trade
- 🖥️ **VPS** (opcional): $5-20/mês para rodar 24/7
- ⚡ **Eletricidade**: Mínima se rodar em casa

### Como reduzir taxas de trading?

**Na Binance:**
- Use BNB para pagar taxas (desconto 25%)
- Aumente seu VIP level com maior volume
- Considere Binance Spot vs Futures

**No XBot:**
```bash
# Configurar para usar BNB para taxas
python -m src.main config --use-bnb-for-fees true

# Otimizar frequência de trades
python -m src.main config --min-profit-threshold 0.5  # Só opera se profit > 0.5%
```

### Vale a pena usar um VPS?

**Vantagens:**
- ✅ Uptime 24/7
- ✅ Latência menor
- ✅ Conexão estável
- ✅ Não depende do seu computador

**Recomendações de VPS:**
- AWS EC2 t3.micro (grátis por 1 ano)
- DigitalOcean Droplet ($5/mês)
- Vultr High Frequency ($6/mês)

```bash
# Configuração otimizada para VPS
python -m src.main config --vps-mode true
```

## 🔒 Segurança

### O XBot v2 é seguro?

**Sim!** Medidas de segurança implementadas:
- 🔒 API keys criptografadas localmente
- 🛡️ Não armazenamos suas credenciais
- 🔐 Código open-source (auditável)
- 🚫 Sem acesso à função de withdraw na API

### Como proteger minhas API keys?

**Configuração segura da API:**
- ✅ Apenas permissões necessárias (Spot Trading)
- ✅ Whitelist de IPs
- ❌ Nunca ative Withdraw
- 🔄 Rotacione keys periodicamente

```bash
# Verificar permissões da API
python -m src.main security check-api-permissions

# Testar restrições de IP
python -m src.main security verify-ip-restrictions
```

### E se eu perder o acesso ao bot?

**Backup essencial:**
```bash
# Backup completo
python -m src.main backup create --full

# Backup apenas configurações
python -m src.main backup create --config-only

# Agendar backups automáticos
python -m src.main config --auto-backup daily
```

**Emergency stop via Binance:**
- Acesse sua conta Binance
- Vá em API Management
- Desative ou delete a API key

## 🌟 Recursos Avançados

### Posso usar machine learning?

**Em desenvolvimento!** Recursos futuros:
- 🤖 Estratégias com ML/AI
- 📊 Análise preditiva
- 🧠 Auto-otimização de parâmetros

### Integração com outras ferramentas?

**APIs disponíveis:**
```bash
# Webhook para sinais externos
python -m src.main webhook --enable --url "http://localhost:8080/signals"

# API REST para controle externo
python -m src.main api --start --port 8080
```

**Integrações planejadas:**
- TradingView signals
- Discord bots
- Portfolio trackers
- Tax reporting tools

## 🆘 Suporte

### Onde obter ajuda?

1. **Documentação**: Primeiro recurso - muito completa
2. **FAQ**: Este documento resolve 80% das dúvidas
3. **Discord**: Comunidade ativa e prestativa
4. **GitHub Issues**: Para bugs e problemas técnicos
5. **Email**: Para questões específicas

### Como reportar um bug?

```bash
# Gerar relatório detalhado
python -m src.main support generate-report

# Incluir no relatório:
1. Versão do XBot v2
2. Sistema operacional
3. Logs de erro
4. Passos para reproduzir
5. Comportamento esperado vs atual
```

### Contribuindo para o projeto

**Formas de contribuir:**
- 🐛 Reportar bugs
- 💡 Sugerir funcionalidades
- 📝 Melhorar documentação
- 🔧 Desenvolver estratégias
- 🌟 Dar star no GitHub
- 💬 Ajudar outros usuários

```bash
# Fork do projeto
git clone https://github.com/seu-usuario/xbot-v2.git
cd xbot-v2

# Criar branch para sua contribuição
git checkout -b minha-contribuicao

# Fazer alterações e enviar PR
```

---

❓ **Não encontrou sua pergunta? Faça-a na nossa comunidade Discord ou abra uma issue no GitHub!**
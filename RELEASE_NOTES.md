# 🤖 XBot v2 - Dashboard Web Release

[![Release](https://img.shields.io/github/v/release/rootkit-original/xbot-v2)](https://github.com/rootkit-original/xbot-v2/releases)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎉 **Novidades da v2.1.0**

### 📊 **Dashboard Web Completo**
- ✅ Interface moderna e responsiva
- ✅ Dados em tempo real da Binance
- ✅ Gráficos interativos
- ✅ Ordens em aberto e saldos
- ✅ Mobile-friendly

![Dashboard Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=XBot+v2+Dashboard)

### 🚀 **Acesso Rápido**

```bash
# 1. Clone o repositório
git clone https://github.com/rootkit-original/xbot-v2.git
cd xbot-v2

# 2. Configure as credenciais
cp .env.example .env
nano .env  # Adicione suas credenciais

# 3. Execute o dashboard
python main.py dashboard

# 4. Acesse: http://localhost:5000
```

## 📋 **O que foi implementado:**

### ✅ **Funcionalidades Principais**
- [x] Dashboard web com Flask
- [x] Integração real com Binance API  
- [x] Visualização de ordens em aberto
- [x] Saldos e dados de mercado em tempo real
- [x] Gráficos de performance interativos
- [x] Sistema de persistência de bots
- [x] Notificações Telegram
- [x] Layout responsivo corrigido

### 🐛 **Bugs Corrigidos**
- [x] Layout inconsistente da seção "Trades por Dia"
- [x] Configuração .env com python-dotenv
- [x] Conectividade API estabilizada
- [x] Responsividade mobile

### 📈 **Métricas da Release**
- **25 arquivos alterados**
- **2,183 linhas adicionadas**
- **1,215 linhas removidas**
- **100% funcional** com dados reais

## 🎯 **Como usar**

### 1️⃣ **Configuração Inicial**
```bash
# Credenciais necessárias no .env:
BINANCE_API_KEY=sua_api_key
BINANCE_SECRET_KEY=sua_secret_key  
TELEGRAM_BOT_TOKEN=seu_bot_token
TELEGRAM_CHAT_ID=seu_chat_id
```

### 2️⃣ **Comandos Disponíveis**
```bash
python main.py dashboard    # Dashboard web
python main.py create       # Criar novo bot
python main.py status       # Status do sistema
python main.py performance  # Relatório de performance
```

### 3️⃣ **Dashboard Features**
- 📊 Métricas em tempo real
- 📋 Lista de ordens em aberto
- 💰 Saldos por moeda  
- 📈 Gráficos de performance
- 🔄 Auto-refresh (30s)

## 🔧 **Arquivos Principais**

| Arquivo | Descrição |
|---------|-----------|
| `dashboard_app.py` | Aplicação Flask do dashboard |
| `templates/dashboard.html` | Interface web completa |
| `main.py` | Orquestrador principal |
| `CHANGELOG.md` | Histórico de versões |

## 🎯 **Screenshot do Dashboard**

**Antes vs Depois:**
- ❌ Apenas console text-based
- ✅ Interface web moderna e responsiva

**Funcionalidades destacadas:**
- 🎨 Design glassmorphism
- 📱 Responsivo para mobile
- ⚡ Carregamento rápido
- 🔄 Dados em tempo real

## 📝 **Roadmap**

### v2.2.0 (Próxima)
- [ ] Alertas personalizados
- [ ] Mais pares de trading
- [ ] API REST externa
- [ ] Sistema de backup

### v2.3.0 (Futuro)
- [ ] Mobile app nativo
- [ ] Machine learning integration
- [ ] Advanced analytics
- [ ] Multi-exchange support

## 🤝 **Contribuindo**

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 **Changelog**

Veja [CHANGELOG.md](CHANGELOG.md) para detalhes completos.

## 📧 **Suporte**

- 🐛 **Issues**: [GitHub Issues](https://github.com/rootkit-original/xbot-v2/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rootkit-original/xbot-v2/discussions)

---

**Desenvolvido com ❤️ por [@rootkit-original](https://github.com/rootkit-original)**
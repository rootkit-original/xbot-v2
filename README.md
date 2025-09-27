# XBot v2 - Sistema Profissional de Trading de Criptomoedas

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://pytest.org/)
[![VS Code](https://img.shields.io/badge/VS%20Code-Ready-blue.svg)](https://code.visualstudio.com/)

Sistema automatizado de trading de criptomoedas de nível empresarial construído com princípios de Clean Architecture, com reconhecimento avançado de padrões, gerenciamento sofisticado de risco e capacidades abrangentes de monitoramento para integração com Binance.

## ✨ Funcionalidades Principais

### 🎯 Capacidades Avançadas de Trading
- **Suporte Multi-Estratégia**: Scalping, swing trading, grid trading e estratégias personalizadas  
- **Reconhecimento de Padrões**: Padrões avançados de candlestick, análise de tendência e detecção de breakout
- **Geração Inteligente de Sinais**: Indicadores técnicos baseados em ML e análise de sentimento do mercado
- **Multi-Exchange Ready**: Integração primária com Binance e arquitetura extensível

### 🛡️ Gerenciamento de Risco
- **Análise Sofisticada de Risco**: Kelly Criterion, cálculos VaR, dimensionamento de posição ajustado por volatilidade
- **Monitoramento em Tempo Real**: Avaliação contínua de risco e ajustes automáticos de posição  
- **Framework de Compliance**: Validação integrada, trilhas de auditoria e ferramentas de conformidade
- **Controles de Emergência**: Circuit breakers, kill switches e mitigação automatizada de risco

### 🏗️ Arquitetura Empresarial
- **Clean Architecture**: Design orientado por domínio com clara separação de responsabilidades
- **Orquestrador Principal**: main.py centralizado para todas as operações e gerenciamento do sistema
- **100% Cobertura de Testes**: Suite abrangente de testes unitários e integração (23/23 testes passando)
- **Documentação Profissional**: Documentação completa de API e exemplos de uso
- **Integração VS Code**: Ambiente de desenvolvimento pré-configurado com 18+ tarefas
- **Estrutura Simplificada**: Diretório scripts otimizado apenas com setup essencial

## 💻 Uso - Orquestrador Principal

O main.py é o **ponto central de orquestração** do sistema XBot v2:

`ash
# 🚀 Inicia o sistema XBot completo
python main.py start

# 🤖 Cria um novo bot de trading  
python main.py create-bot "MeuBot" --capital 1000 --symbols BTCUSDT,ETHUSDT

# 📝 Lista todos os bots ativos
python main.py list-bots

# 📊 Mostra status do sistema
python main.py status

# 🖥️ Abre dashboard de monitoramento
python main.py dashboard

# ⚙️ Configura ambiente inicial
python main.py setup

# 🧪 Executa suite completa de testes
python main.py test

# 🔴 Para o sistema
python main.py stop
`

## 🎯 Comandos do Orquestrador

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| start | Inicia o sistema completo | python main.py start |
| stop | Para todos os bots e serviços | python main.py stop |
| status | Mostra status detalhado do sistema | python main.py status |
| create-bot | Cria novo bot de trading | python main.py create-bot "MeuBot" --capital 1000 |
| list-bots | Lista todos os bots ativos | python main.py list-bots |
| dashboard | Abre dashboard de monitoramento | python main.py dashboard |
| setup | Configura ambiente inicial | python main.py setup |
| 	est | Executa suite completa de testes | python main.py test |

## 🚀 Início Rápido

### Instalação
1. Clone o repositório: git clone <repository-url> && cd xBotv2
2. Execute o script de configuração: python scripts/setup.py
3. Configure variáveis de ambiente no arquivo .env
4. Inicie o sistema: python main.py start

### Estrutura Simplificada
`
xBotv2/
├── main.py                      # 🎯 Orquestrador principal
├── src/                         # Código fonte Clean Architecture
├── scripts/setup.py            # Setup simplificado 
├── examples/basic/              # Exemplos de uso
├── tests/                       # Testes (23/23 passando)
└── docs/                       # Documentação
`

## 🧪 Testes e Qualidade

- **100% Cobertura**: 23/23 testes unitários passando
- **Execução**: python main.py test ou python -m pytest tests/
- **CI/CD**: Integração contínua com VS Code Tasks
- **Quality Gates**: Black, Flake8, mypy integrados

## ⚠️ Segurança e Risco

**Práticas Essenciais:**
1. Sempre teste em testnet primeiro
2. Nunca arrisque mais do que pode perder  
3. Monitore constantemente o sistema
4. Mantenha backups regulares
5. Use API keys com permissões limitadas

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch de feature
3. Mantenha 100% cobertura de testes
4. Siga Clean Architecture
5. Abra Pull Request

## 📄 Licença

MIT License - Veja arquivo LICENSE para detalhes.

---

🚀 **XBot v2** - Construído com ❤️ para a comunidade de trading algorítmico

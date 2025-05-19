# 🤖 Chatbot Weather API

Este projeto é um chatbot inteligente construído com **Python + AWS Chalice** que responde perguntas sobre **clima** e outras questões gerais usando **IA (Groq)**.

---

## 📌 Funcionalidades

- ☀️ Retorna a previsão do tempo para cidades mencionadas na mensagem
- 🧠 Responde perguntas genéricas usando modelo LLM via Groq API
- ✅ Testes automatizados com Pytest
- ⚙️ Executável localmente via `chalice local`

---

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/matheusassmann/chatbot-weather-api.git
cd chatbot-weather-api
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências do projeto

```bash
pip install -r requirements-dev.txt
```

### 4. Obter API Key

- Acesse https://groq.com
- Crie uma conta e obtenha uma API Key gratuitamente

### 5. Defina suas variáveis de ambiente
Crie um arquivo .env, na raiz do projeto com:
```bash
GROQ_API_KEY="sua-chave-aqui"
```

### 6. Execute localmente
```bash
chalice local
```

Para execução dos testes do projeto:
```bash
python -m pytest -m unit # testes unitários
python -m pytest -m integration # testes de integração
```

Exemplo de requisição utilizando o HTTPie:
```bash
http POST http://localhost:8000 message="Vai chover amanhã em Bertioga?"
```
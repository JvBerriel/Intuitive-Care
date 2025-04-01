# 🧪 Projeto IntuitiveCare – Teste Técnico

Este projeto foi desenvolvido como parte do processo seletivo para vaga de estágio na IntuitiveCare. Ele é composto por quatro etapas principais: Web Scraping, Transformação de Dados, Banco de Dados e API + Frontend (Vue.js).

## 🔍 Testes Realizados

### ✅ 1. Web Scraping
- Acessa o site oficial da ANS
- Baixa os anexos I e II em formato PDF
- Compacta os arquivos em um .zip

**Linguagem:** Python  
**Libs:** requests, beautifulsoup4

### ✅ 2. Transformação de Dados
- Extrai as tabelas do Anexo I (PDF)
- Salva em um CSV estruturado
- Substitui as siglas OD e AMB por suas descrições completas
- Compacta em `Teste_Joao_Vitor_Costa_Berriel_Braga.zip`

**Linguagem:** Python  
**Libs:** tabula-py, pandas

### ✅ 3. Banco de Dados
- Scripts SQL para:
  - Criar tabelas compatíveis com PostgreSQL/MySQL
  - Executar análises:
    - Top 10 operadoras com maiores despesas em assistência médico-hospitalar nos últimos trimestre e ano

### ✅ 4. API + Frontend Vue
- Interface em Vue.js para buscar operadoras pelo nome, CNPJ e razão social
- Backend em Flask com rota `/buscar-operadoras`
- Integração via Axios
- Demonstração no Postman

**Linguagens:** JavaScript (Vue 3) + Python (Flask)  
**Libs:** axios, file-saver, flask, flask-cors, core-js

## 🚀 Como rodar o projeto

### 🖥️ Execução pelo Arquivo Principal (main.py)
O sistema completo pode ser controlado via menu interativo:

```bash
# Ative o ambiente virtual (se necessário)
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Execute o sistema
python main.py
Menu de Opções:

Copy
1. Baixar anexos
2. Converter PDFs em CSV
3. Iniciar sistema completo (API + Frontend)
4. Sair

📦 Execução Manual (Backend Python)
bash
Copy
# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor Flask
python api/server.py

🌐 Frontend (Vue.js)
bash
Copy
cd frontend
npm install
npm run serve
🛠️ Tecnologias Principais
Backend:

Python 3.8+

Flask (API REST)

Pandas (processamento de dados)

Tabula-py (extração de PDFs)

BeautifulSoup (web scraping)

Frontend:

Vue.js 3

Axios (chamadas HTTP)

FileSaver.js (exportação de dados)

Banco de Dados:

PostgreSQL/MySQL


⚠️ Pré-requisitos
Python 3.8+

Node.js (para o frontend)

PostgreSQL ou MySQL (para testes de banco de dados)


📫 Autor
João Vitor Costa Berriel Braga
📧 jberriel.vitor@gmail.com
 

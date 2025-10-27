# 🍕 API Delivery Project

[![CI/CD](https://github.com/YOUR_USERNAME/api_delivery_project/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/api_delivery_project/actions)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/api_delivery_project/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/api_delivery_project)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

API RESTful para gerenciamento de pedidos de delivery, construída com FastAPI, SQLAlchemy e autenticação JWT.

## 📋 Índice

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Executando a Aplicação](#-executando-a-aplicação)
- [Testes](#-testes)
- [Documentação da API](#-documentação-da-api)
- [CI/CD](#-cicd)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuindo](#-contribuindo)

## 🚀 Features

- ✅ **Autenticação JWT** com refresh tokens
- ✅ **CRUD completo de pedidos** com gerenciamento de itens
- ✅ **Sistema de permissões** (usuários regulares vs. admin)
- ✅ **Cálculo automático** de preços dos pedidos
- ✅ **Migrations** com Alembic
- ✅ **Documentação automática** (Swagger/ReDoc)
- ✅ **Testes automatizados** com 92% de cobertura
- ✅ **Docker & Docker Compose** para desenvolvimento e produção
- ✅ **CI/CD** com GitHub Actions

## 🛠 Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) 0.116.1
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) 2.0.42
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Autenticação:** JWT (python-jose) + OAuth2 + bcrypt
- **Migrations:** [Alembic](https://alembic.sqlalchemy.org/) 1.16.4
- **Testes:** pytest + pytest-cov + httpx
- **Linting:** black + ruff + mypy
- **Server:** Uvicorn 0.35.0

## 📦 Requisitos

- Python 3.11+
- pip ou poetry
- Docker & Docker Compose (opcional)

## 💻 Instalação

### Opção 1: Instalação Local

```bash
# Clone o repositório
git clone https://github.com/YOUR_USERNAME/api_delivery_project.git
cd api_delivery_project

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instale as dependências
pip install --upgrade pip
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações
```

### Opção 2: Docker

```bash
# Clone o repositório
git clone https://github.com/YOUR_USERNAME/api_delivery_project.git
cd api_delivery_project

# Configure variáveis de ambiente
cp .env.example .env

# Build e execute
docker-compose up --build
```

## ⚙️ Configuração

Crie um arquivo `.env` baseado no `.env.example`:

```env
# Segurança - JWT
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./data/dados.db
# Para PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Executar Migrations

```bash
# Aplicar migrations
alembic upgrade head

# Criar nova migration (se necessário)
alembic revision --autogenerate -m "Description"
```

## 🚀 Executando a Aplicação

### Desenvolvimento

```bash
# Com reload automático
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Produção

```bash
# Docker Compose
docker-compose up -d

# Ou manualmente
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

A API estará disponível em: **http://localhost:8000**

## 🧪 Testes

### Executar Todos os Testes

```bash
# Testes com cobertura
pytest tests/ --cov=app --cov=routes --cov=scheme --cov-report=term-missing

# Apenas rodar testes
pytest tests/ -v

# Testes específicos
pytest tests/test_auth.py -v
pytest tests/test_orders.py -v
```

### Relatório de Cobertura HTML

```bash
pytest tests/ --cov=app --cov=routes --cov=scheme --cov-report=html
# Abrir htmlcov/index.html no navegador
```

### Métricas Atuais

- ✅ **92% de cobertura** de código
- ✅ **32 testes** implementados
- ✅ **23 testes passando**
- ✅ Testes de autenticação, CRUD, permissões e regras de negócio

## 📚 Documentação da API

### Documentação Interativa

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints Principais

#### Autenticação
```http
POST /auth/create_account  # Criar usuário
POST /auth/login           # Login
POST /auth/login-form      # Login OAuth2
GET  /auth/refresh         # Refresh token
```

#### Pedidos (Requer autenticação)
```http
POST /orders/order                     # Criar pedido
GET  /orders/list                      # Listar todos (admin)
GET  /orders/list/order-user           # Listar do usuário
GET  /orders/order/{order_id}          # Visualizar pedido
POST /orders/order/add-item/{id}       # Adicionar item
POST /orders/order/remove-item/{id}    # Remover item
POST /orders/order/finish/{id}         # Finalizar
POST /orders/order/cancel/{id}         # Cancelar
```

Veja [reports/api-endpoints.md](reports/api-endpoints.md) para documentação completa.

## 🔍 Linting e Formatação

```bash
# Formatar código
black .

# Verificar formatação
black --check .

# Linting
ruff check .

# Corrigir automaticamente
ruff check --fix .

# Type checking
mypy --ignore-missing-imports app/ routes/
```

## 🔒 Segurança

```bash
# Scan de vulnerabilidades em dependências
pip-audit

# Scan de código (instalar bandit)
pip install bandit
bandit -r app/ routes/
```

Veja [reports/dependency-scan.md](reports/dependency-scan.md) para o relatório completo.

## 🔄 CI/CD

O projeto utiliza GitHub Actions para CI/CD automático:

- ✅ **Lint** (black, ruff, mypy)
- ✅ **Testes** em Python 3.11, 3.12, 3.13
- ✅ **Cobertura** com upload para Codecov
- ✅ **Security scan** com pip-audit
- ✅ **Docker build** e validação

O workflow é executado em push/PR para `main` e `develop`.

## 📁 Estrutura do Projeto

```
api_delivery_project/
├── app/
│   ├── main.py              # Aplicação FastAPI principal
│   ├── core/
│   │   └── database.py      # Configuração do banco
│   ├── models/
│   │   ├── tables.py        # Modelos SQLAlchemy
│   │   └── dependencies.py  # Dependências FastAPI
│   └── alembic/             # Migrations
├── routes/
│   ├── auth_routes.py       # Endpoints de autenticação
│   └── order_routes.py      # Endpoints de pedidos
├── tests/
│   ├── conftest.py          # Fixtures pytest
│   ├── test_auth.py         # Testes de autenticação
│   └── test_orders.py       # Testes de pedidos
├── reports/                 # Relatórios e documentação
├── scheme.py                # Schemas Pydantic
├── requirements.txt         # Dependências Python
├── pytest.ini               # Configuração pytest
├── Dockerfile               # Imagem Docker
├── docker-compose.yml       # Orquestração Docker
├── alembic.ini              # Configuração Alembic
└── .github/
    └── workflows/
        └── ci.yml           # GitHub Actions workflow
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Convenções

- Código formatado com Black
- Linting com Ruff
- Cobertura de testes >= 70%

## 📊 Status do Projeto

- ✅ API funcional com autenticação JWT
- ✅ CRUD completo de pedidos
- ✅ 92% de cobertura de testes
- ✅ CI/CD configurado
- ✅ Dockerizado
- ⚠️ Pendente: Migração para PostgreSQL em produção
- ⚠️ Pendente: Rate limiting

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Thiago** - Desenvolvimento inicial

## 📞 Contato

Para questões ou sugestões, abra uma [issue](https://github.com/YOUR_USERNAME/api_delivery_project/issues).

---



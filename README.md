<h1 align="left">🚀API Delivery com FastAPI</h1>

Meu primeiro projeto completo, juntando autenticação segura, persistência de dados, migrações de banco e deploy automatizado.
O objetivo foi aprender criando algo real: uma API de delivery com login, pedidos, itens e deploy funcionando no Render usando Docker.

---
<h2 aling="left">📖 Documentação da API</h2>

Swagger UI --> https://api-delivery-tuk2.onrender.com/docs#/

---

<h2 align="left">🛠️ Tecnologias Utilizadas:

Python 3.13, FastAPI, SQLAlchemy, Alembic, Docker, Render</h2>

Objetivo técnico: autenticação com JWT, CRUD de pedidos e itens, migrações com Alembic e deploy com Docker/Render

Abordagem: separar responsabilidades (core, models, routes), garantir que o banco seja criado automaticamente em ambientes simples e manter a porta aberta para migrar para Postgres quando fizer sentido

Por que existe cada peça
---
Este projeto nasceu como meu primeiro app completo.
Eu queria aprender de ponta a ponta: autenticação segura, banco de dados, migrações, deploy.
Muitos erros apareceram no caminho, e foi resolvendo cada um que realmente aprendi: migrações que não rodavam, tokens que não passavam, deploys que quebravam.

Cada arquivo da estrutura existe para resolver um problema concreto e registrar o aprendizado.

⚙️ Como Rodar o Projeto Localmente
---
1️⃣ Clonar o repositório
git clone https://github.com/Thiago-jss/ApiDelivery.git
cd seu-repo


	
2️⃣ Criar e ativar ambiente virtual

python -m venv .venv
source .venv/bin/activate  -- # Linux/Mac

.venv\\Scripts\\activate --  # Windows



3️⃣ Instalar dependências


pip install -r requirements.txt



4️⃣ Rodar as migrações do banco de dados


alembic upgrade head



5️⃣ Rodar localmente


uvicorn app.main:app --reload



🐳 Como Rodar com Docker


docker build -t meu-projeto .


docker run -d -p 8000:8000 meu-projeto

<h3 align="left">📂 Arquitetura e arquivos principais</h3>
main.py

Cria a instância do FastAPI e registra os routers (auth, order)

No evento startup, chama criar_bd() para garantir que o SQLite crie as tabelas automaticamente

Centraliza configuração de segurança (OAuth2PasswordBearer + passlib)

app/core/database.py

Constrói o engine do SQLAlchemy a partir da DATABASE_URL (fallback para SQLite)

Normaliza postgres:// → postgresql:// quando necessário

Expõe Base, SessionLocal e criar_bd()

Motivo: manter o deploy simples, mas preparado para Postgres depois.

app/models/*

tables.py: modelos ORM.

__init__.py: garante que os models sejam importados dinamicamente. evitando problemas com migrações do Alembic

dependencies.py: funções reusáveis como get_session()

app/routes/*

Auth: registro, login, refresh token.

Orders: CRUD de pedidos e itens.

Usa JWT com python-jose e dependências para injetar a sessão do DB.

alembic/

Configuração de migrações. Precisei ajustar env.py para importar os models corretamente

Dockerfile / docker-compose.yml

Dockerfile: ambiente igual para dev e prod

docker-compose: volume ./data mapeado para persistir dados.db

Arquivos auxiliares

requirements.txt

.env.example

teste.py: script simples para testar o header Authorization

scheme.py: schemas Pydantic.

<h2 align="left">🏆Problemas que apareceram e o que aprendi</h2>

1º erro - Migrations com Alembic - o banco de dados não subia

erro: migrations não detectavam models / Render sem tabelas

Causa: env.py não apontava para o target_metadata certo e __init__.py faltando

Solução: limpei histórico de migrations, corrigi env.py, implementei criar_bd() como fallback

Aprendizado: Alembic só funciona se o metadata estiver visível


2º erro - Refresh token / headers

erro: token não era aceito em alguns testes

Causa: diferença no formato do header e falta de variáveis em alguns ambientes

Solução: padronizei "Authorization: Bearer <token>" e criei uma pasta para testes = teste.py

Aprendizado: pequenos scripts aceleram o debug



3º erro - Deploy no Render / Docker

erro:  faltavam os enviroments SECRET_KEY, ALGORITHM, warnings de bcrypt, permissões no Docker

Solução: ajustei Dockerfile, validei fallbacks, configurei env vars no Render

Aprendizado: logs, variáveis e persistência são muito importantes e essenciais no processo para deploy

---

<h2 align="left">🔧 Melhorias aplicadas</h2>

criar_bd() implementado para ambientes sem DB gerenciado

Fallback seguro para SECRET_KEY e ALGORITHM

Ajustes em __init__.py nos models

Dockerfile atualizado para dependências nativas

docker-compose com volume persistente

---

<h2 align="left">📚 O que esse projeto me ensinou</h2>


Técnico: diferenças práticas entre SQLite e Postgres, como Alembic depende do metadata, e como volumes do Docker afetam persistência

Processo: logs e testes rápidos são melhores para ter uma resulução mais ampla

Pessoal: errar faz parte. cada bug que corrigi aumentou minha confiança e me fez aprender coisas novas

---
<h2 align="left">🚧 Limitações e próximos passos</h2>

SQLite em produção não é ideal; preciso migrar para Postgres

Histórico de migrations precisa de limpeza conforme o projeto crescer

Faltam testes E2E

Próximos passos:

Migrar para Postgres gerenciado.

CI com pytest + Alembic.

Adicionar testes E2E.

Monitoramento e limitação de rate


<h1 aling="left">👨🏽‍🎓 Autor</h1>

Thiago Jesus

 

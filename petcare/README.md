# 🐾 PetCare Manager

> Sistema completo de gestão de animais de estimação — Projeto de Pós-Graduação em Serviços de Software

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Endpoints da API](#endpoints-da-api)
- [Modelo de Dados](#modelo-de-dados)
- [Docker](#docker)
- [Git Flow](#git-flow)

---

## Visão Geral

O **PetCare Manager** é uma aplicação web para gestão completa de animais de estimação, oferecendo:

- 🐶 **Cadastro de Pets** — com raça, idade, peso e informações clínicas
- 💉 **Controle Vacinal** — histórico e alertas de reforços
- 🏃 **Atividades Físicas** — registro e sugestões por raça
- 🗺️ **Passeios** — log e sugestões de locais por porte
- 🩺 **Guia de Cuidados** — orientações específicas por raça

---

## Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                   Docker Compose                    │
│                                                     │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────┐  │
│  │   Frontend   │   │   Backend    │   │   DB    │  │
│  │   React +    │──▶│  FastAPI +   │──▶│Postgres │  │
│  │    Vite      │   │  SQLAlchemy  │   │   15    │  │
│  │  port: 3000  │   │  port: 8000  │   │p: 5432  │  │
│  └──────────────┘   └──────────────┘   └─────────┘  │
└─────────────────────────────────────────────────────┘
```

**Padrões adotados:**
- REST API com versionamento (`/api/v1/`)
- Repository Pattern via SQLAlchemy ORM
- Schema validation com Pydantic v2
- Soft delete para Pets (campo `ativo`)
- Seed automático de raças no banco

---

## Tecnologias

| Camada | Tecnologia | Versão |
|---|---|---|
| Backend | Python + FastAPI | 3.11 / 0.111 |
| ORM | SQLAlchemy | 2.0 |
| Validação | Pydantic | v2 |
| Banco de Dados | PostgreSQL | 15 |
| Frontend | React + Vite | 18 / 5 |
| Roteamento | React Router DOM | v6 |
| HTTP Client | Axios | 1.7 |
| Containerização | Docker + Compose | 24+ / v2 |
| Servidor Web | Nginx | alpine |
| Controle de Versão | Git | — |

---

## Estrutura do Projeto

```
petcare/
├── docker-compose.yml          # Orquestração dos 3 serviços
├── .gitignore
├── README.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── init.sql                # Seed de raças e cuidados
│   └── app/
│       ├── main.py             # Entrypoint FastAPI + CORS + routers
│       ├── database.py         # Engine, Session, Settings
│       ├── models/
│       │   └── models.py       # Entidades SQLAlchemy (6 modelos)
│       ├── schemas/
│       │   └── schemas.py      # Pydantic DTOs (Request/Response)
│       └── routers/
│           ├── pets.py         # CRUD + dashboard por pet
│           ├── racas.py        # CRUD de raças
│           ├── vacinas.py      # CRUD + alertas de pendentes
│           ├── atividades.py   # CRUD + sugestões por raça
│           ├── passeios.py     # CRUD + sugestões por porte
│           └── cuidados.py     # CRUD de cuidados por raça
│
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx             # Shell + Sidebar + Router
        ├── index.css           # Design system completo
        ├── services/
        │   └── api.js          # Axios + todos os endpoints
        └── pages/
            ├── Dashboard.jsx   # Visão geral + alertas
            ├── Pets.jsx        # Listagem + cadastro
            ├── PetDetail.jsx   # Detalhe com abas
            ├── Vacinas.jsx     # Painel global de vacinas
            ├── Atividades.jsx  # Seleção de pet
            └── Passeios.jsx    # Seleção de pet
```

---

## Como Executar

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/) v2
- [Git](https://git-scm.com/)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/petcare-manager.git
cd petcare-manager
```

### 2. Suba os containers

```bash
docker compose up --build
```

Aguarde os 3 serviços subirem. O banco inicializa automaticamente com seed de raças.

### 3. Acesse a aplicação

| Serviço | URL |
|---|---|
| Frontend (React) | http://localhost:3000 |
| API (FastAPI) | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

### 4. Parar os serviços

```bash
docker compose down          # Para e remove containers
docker compose down -v       # Também remove o volume do banco
```

### Desenvolvimento local (sem Docker)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## Endpoints da API

### Pets — `/api/v1/pets`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Lista todos os pets ativos |
| POST | `/` | Cadastra novo pet |
| GET | `/{id}` | Busca pet por ID |
| PUT | `/{id}` | Atualiza dados do pet |
| DELETE | `/{id}` | Desativa o pet (soft delete) |
| GET | `/{id}/dashboard` | Resumo com stats do pet |

### Raças — `/api/v1/racas`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Lista raças (filtro por espécie) |
| POST | `/` | Cadastra nova raça |
| GET | `/{id}` | Busca raça por ID |

### Vacinas — `/api/v1/vacinas`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/pet/{pet_id}` | Histórico do pet |
| GET | `/pendentes` | Todas vencidas/próximas (30 dias) |
| POST | `/` | Registra nova vacina |
| PUT | `/{id}` | Atualiza status/data |
| DELETE | `/{id}` | Remove registro |

### Atividades — `/api/v1/atividades`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/pet/{pet_id}` | Histórico do pet |
| GET | `/sugestoes/{pet_id}` | Sugestões por nível da raça |
| POST | `/` | Registra atividade |
| DELETE | `/{id}` | Remove registro |

### Passeios — `/api/v1/passeios`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/pet/{pet_id}` | Histórico do pet |
| GET | `/sugestoes/{pet_id}` | Sugestões por porte |
| POST | `/` | Registra passeio |
| DELETE | `/{id}` | Remove registro |

### Cuidados — `/api/v1/cuidados`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/raca/{raca_id}` | Cuidados da raça (filtro por categoria) |
| POST | `/` | Cadastra cuidado |
| DELETE | `/{id}` | Remove cuidado |

---

## Modelo de Dados

```
Raca (1) ──────── (N) Pet
  │                     │
  │                     ├── (N) Vacina
  │                     ├── (N) Atividade
  │                     └── (N) Passeio
  │
  ├── (N) Cuidado
  └── (N) VacinaRecomendada
```

**Enums utilizados:**
- `EspecieEnum`: cao | gato | outro
- `PorteEnum`: pequeno | medio | grande
- `SexoEnum`: macho | femea
- `StatusVacinaEnum`: pendente | aplicada | atrasada

---

## Docker

### Serviços no docker-compose.yml

**`db`** — PostgreSQL 15 Alpine
- Volume persistente `petcare_pgdata`
- Healthcheck antes de iniciar a API
- Seed via `init.sql` no `docker-entrypoint-initdb.d`

**`api`** — FastAPI + Uvicorn
- Build multi-stage com `python:3.11-slim`
- Hot-reload ativo em desenvolvimento
- Depende do health check do banco

**`frontend`** — React + Nginx
- Build de produção com Vite
- Proxy `/api` para o serviço `api`
- Serve SPA com `try_files` para React Router

---

## Git Flow

```bash
# Estrutura de branches recomendada
main          # produção estável
develop       # integração
feature/*     # novas funcionalidades
hotfix/*      # correções urgentes

# Exemplos de commits semânticos
git commit -m "feat: adiciona controle vacinal por pet"
git commit -m "fix: corrige cálculo de dias para reforço"
git commit -m "docs: atualiza README com endpoints"
git commit -m "chore: adiciona docker-compose healthcheck"
```

---

## Autor

Desenvolvido como projeto acadêmico para a disciplina de **Serviços de Software** — Pós-Graduação.

---

*"Cuidar bem de um pet é um ato de amor que começa com organização."* 🐾

# 🐾 PetCare Manager

> Sistema completo de gestão de animais de estimação
> Projeto de Pós-Graduação em Serviços de Software — **Instituto Mauá de Tecnologia**

**Versão:** 2.0.0

**Autores:**
- Claudinei Manoel dos Santos — RA 25.80224-0
- Cleber Luiz da Silva — RA 25.80133-3

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Endpoints da API](#endpoints-da-api)
- [Modelo de Dados](#modelo-de-dados)
- [Armazenamento de Fotos](#armazenamento-de-fotos)
- [Motor de Recomendações (IA)](#motor-de-recomendações-ia)
- [Cronograma Vacinal](#cronograma-vacinal)
- [Testes](#testes)
- [Docker](#docker)

---

## Visão Geral

O **PetCare Manager** é uma aplicação web para gestão completa de animais de estimação:

- 🐶 **Pets** — CRUD completo com foto, edição, exclusão (soft delete) e busca
- 💉 **Cronograma Vacinal** — 21 vacinas recomendadas (V10, Antirrábica, Bordetella, Giárdia, V4, FeLV) com confirmação de dose em 1 clique
- 🏃🗺️ **Atividades & Passeios** — aba unificada com sugestões por raça e porte
- 🩺 **Guia de Cuidados** — 70 cuidados pré-cadastrados (5 por raça) em 5 categorias
- 🤖 **Recomendações Personalizadas (IA)** — motor de regras com análise por idade, porte, nível de atividade
- 📸 **Upload de Foto** — imagens dos pets em volume Docker persistente
- 📊 **Dashboard** — estatísticas, alertas vacinais e visão geral

---

## Arquitetura

```
┌────────────────────────────────────────────────────────────┐
│                      Docker Compose                        │
│                                                            │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────┐   │
│  │   Frontend   │    │     API      │    │     DB      │   │
│  │   React +    │◀──▶│  FastAPI +   │◀──▶│ PostgreSQL  │   │
│  │    Vite      │    │  SQLAlchemy  │    │     15      │   │
│  │  :3000       │    │    :8000     │    │   :5432     │   │
│  └──────────────┘    └──────┬───────┘    └─────────────┘   │
│                             │                              │
│                             ▼                              │
│                      ┌──────────────┐                      │
│                      │   Volumes    │                      │
│                      │  pgdata      │ (banco)              │
│                      │  uploads     │ (fotos)              │
│                      └──────────────┘                      │
└────────────────────────────────────────────────────────────┘
```

**Padrões adotados:**
- REST API versionada (`/api/v1/`)
- SQLAlchemy ORM + Pydantic v2 para validação
- Soft delete para Pets (campo `ativo`)
- Seed idempotente no startup (14 raças + 70 cuidados + 21 vacinas recomendadas)
- Healthchecks encadeados (db → api → frontend)
- 52 testes automatizados com SQLite in-memory

---

## Tecnologias

| Camada | Tecnologia | Versão |
|---|---|---|
| Backend | Python + FastAPI | 3.11 / 0.111 |
| ORM | SQLAlchemy | 2.0 |
| Validação | Pydantic | v2 |
| Banco | PostgreSQL | 15-alpine |
| Frontend | React + Vite | 18 / 5 |
| Roteamento | React Router DOM | v6 |
| HTTP Client | Axios | 1.7 |
| Ícones | Lucide React | 0.383 |
| Datas | date-fns | 3.6 |
| Servidor Web | Nginx | alpine |
| Containerização | Docker + Compose | 24+ / v2 |
| Testes | pytest + httpx TestClient | 8.2 / 0.27 |

---

## Estrutura do Projeto

```
petcare/
├── docker-compose.yml          # Orquestração (3 serviços + 2 volumes)
├── gerar_documentacao.py       # Script de geração do PDF de docs
├── README.md
│
├── backend/
│   ├── Dockerfile              # python:3.11-slim + curl
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .dockerignore
│   ├── AI/
│   │   ├── __init__.py
│   │   └── recomendacoes.py    # Motor de regras (IA)
│   ├── app/
│   │   ├── main.py             # FastAPI + CORS + StaticFiles + lifespan
│   │   ├── database.py         # Engine + Session + Settings
│   │   ├── seed.py             # 14 raças + 70 cuidados + 21 vacinas
│   │   ├── models/models.py    # 7 entidades + enums
│   │   ├── schemas/schemas.py  # DTOs Pydantic
│   │   └── routers/            # 6 routers REST
│   │       ├── pets.py         # CRUD + foto + recomendações + dashboard
│   │       ├── racas.py
│   │       ├── vacinas.py      # CRUD + cronograma + confirmar dose
│   │       ├── atividades.py
│   │       ├── passeios.py
│   │       └── cuidados.py
│   └── tests/                  # 52 testes automatizados
│       ├── conftest.py         # SQLite in-memory + fixtures
│       ├── test_racas.py       # 8 testes
│       ├── test_pets.py        # 11 testes
│       ├── test_vacinas.py     # 12 testes
│       ├── test_atividades.py  # 10 testes
│       └── test_passeios.py    # 11 testes
│
├── frontend/
│   ├── Dockerfile              # Node 20 build + Nginx Alpine
│   ├── nginx.conf              # Proxy /api + SPA + gzip
│   ├── .dockerignore
│   ├── package.json
│   └── src/
│       ├── App.jsx             # Shell + Sidebar + Rotas
│       ├── services/api.js     # Axios centralizado + API_URL
│       └── pages/
│           ├── Dashboard.jsx
│           ├── Pets.jsx        # Lista + modal de cadastro com foto
│           ├── PetDetail.jsx   # Header + IA + 3 abas + edição
│           ├── Vacinas.jsx     # Painel global de vacinas
│           ├── Atividades.jsx  # Seleção de pet (Atividades+Passeios)
│           └── Cuidados.jsx    # Guia por raça
│
└── docs/                       # Documentação gerada
    ├── PetCare_Manager_Documentacao.pdf
    ├── arquitetura.png
    └── screenshots/
```

---

## Como Executar

### Pré-requisitos

- [Docker Desktop](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/) v2
- Portas livres: **3000**, **5432**, **8000**

### Subir a aplicação

```bash
cd petcare
docker compose up --build
```

O seed popula automaticamente 14 raças, 70 cuidados e 21 vacinas recomendadas no primeiro start.

### Acessar

| Serviço | URL |
|---|---|
| Frontend (React) | http://localhost:3000 |
| API (FastAPI) | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

### Parar

```bash
docker compose down          # para e remove containers (mantém dados)
docker compose down -v       # também remove volumes (banco + fotos)
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

Base URL: `/api/v1/` | Documentação interativa: `/docs` (Swagger)

### Pets — `/api/v1/pets`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/?ativo=true` | Lista pets (ativos ou inativos) |
| POST | `/` | Cadastra novo pet |
| GET | `/{id}` | Busca pet por ID |
| PUT | `/{id}` | Atualiza dados do pet |
| DELETE | `/{id}` | Soft delete (`ativo=False`) |
| **POST** | **`/{id}/photo`** | **Upload de foto (multipart/form-data)** |
| **DELETE** | **`/{id}/photo`** | **Remove a foto** |
| **GET** | **`/{id}/recomendacoes`** | **Recomendações IA (motor de regras)** |
| GET | `/{id}/dashboard` | Resumo com stats do pet |

### Raças — `/api/v1/racas`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/?especie=cao` | Lista raças (filtro por espécie) |
| POST | `/` | Cadastra raça |
| GET | `/{id}` | Busca raça |
| PUT | `/{id}` | Atualiza raça |

### Vacinas — `/api/v1/vacinas`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/pet/{pet_id}` | Histórico de vacinas aplicadas |
| GET | `/pendentes` | Vacinas vencidas/próximas (30 dias) |
| **GET** | **`/cronograma/{pet_id}`** | **Cronograma vacinal personalizado** |
| **POST** | **`/confirmar/{pet_id}/{rec_id}`** | **Confirma dose do cronograma** |
| POST | `/` | Registra vacina manual |
| PUT | `/{id}` | Atualiza |
| DELETE | `/{id}` | Remove |

### Atividades — `/api/v1/atividades`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/pet/{pet_id}` | Histórico |
| GET | `/sugestoes/{pet_id}` | Sugestões por nível da raça |
| POST | `/` | Registra |
| DELETE | `/{id}` | Remove |

### Passeios — `/api/v1/passeios`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/pet/{pet_id}` | Histórico |
| GET | `/sugestoes/{pet_id}` | Sugestões por porte do pet |
| POST | `/` | Registra |
| DELETE | `/{id}` | Remove |

### Cuidados — `/api/v1/cuidados`

| Método | Rota | Descrição |
|---|---|---|
| GET | `/raca/{raca_id}` | Cuidados da raça (filtro por categoria) |
| POST | `/` | Cadastra |
| DELETE | `/{id}` | Remove |

### Arquivos estáticos

| Método | Rota | Descrição |
|---|---|---|
| GET | `/uploads/pets/{filename}` | Serve fotos dos pets |

---

## Modelo de Dados

```
Raca (1) ──────── (N) Pet ────── foto_url (String)
  │                    │
  │                    ├── (N) Vacina
  │                    ├── (N) Atividade
  │                    └── (N) Passeio
  │
  ├── (N) Cuidado
  └── (N) VacinaRecomendada
```

**Enums:**
- `EspecieEnum`: cao | gato | outro
- `PorteEnum`: pequeno | medio | grande
- `SexoEnum`: macho | femea
- `StatusVacinaEnum`: pendente | aplicada | atrasada

---

## Armazenamento de Fotos

### Como funciona

1. **Upload** — `POST /api/v1/pets/{id}/photo` recebe um arquivo via `multipart/form-data`
   - Valida tipo (JPG/PNG/WebP) e tamanho (≤ 5 MB)
   - Gera nome único: `{pet_id}_{uuid8}.{ext}` — ex: `2_cd72f00a.jpg`
   - Se o pet já tinha foto, a anterior é removida do disco
   - Salva em `/app/uploads/pets/` **dentro do container da API**
   - Grava o caminho relativo em `pet.foto_url` (ex: `/uploads/pets/2_cd72f00a.jpg`)

2. **Persistência** — volume Docker nomeado em `docker-compose.yml`:
   ```yaml
   api:
     volumes:
       - uploads:/app/uploads      # volume nomeado, sobrevive a restarts

   volumes:
     uploads:
       name: petcare_uploads       # gerenciado pelo Docker no host
   ```

3. **Servindo** — FastAPI expõe o diretório via `StaticFiles`:
   ```python
   app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")
   ```
   Qualquer arquivo fica acessível em `http://localhost:8000/uploads/pets/{filename}`.

4. **Banco** — apenas o **caminho relativo** vai para o PostgreSQL. O arquivo binário nunca entra no banco.

### Fluxo completo

```
Browser → <img src="http://localhost:8000/uploads/pets/2_cd72f00a.jpg">
         ↓
     FastAPI lê o arquivo do volume Docker petcare_uploads
         ↓
     Retorna o binário da imagem
```

### Considerações

| ✅ Prós | ⚠️ Contras |
|---|---|
| Simples, sem dependência externa | Não escala para múltiplas instâncias |
| Volume persiste entre restarts | Backup precisa ser manual |
| Zero custo adicional | Filesystem efêmero em PaaS free (Render) |
| Funciona offline | Precisa migrar para S3/R2 em produção |

> Para deploy em produção com escalabilidade, o ideal é migrar para **Cloudflare R2**, **Supabase Storage** ou **AWS S3** e guardar apenas a URL pública em `foto_url`.

---

## Motor de Recomendações (IA)

Módulo em `backend/AI/recomendacoes.py` — **motor baseado em regras determinísticas** (rule-based), sem chamadas externas.

### Regras aplicadas

1. **Nível de atividade da raça** (alto/médio/baixo) define frequência semanal e intensidade
2. **Pet idoso** (> 75% da expectativa de vida): reduz intensidade + alerta de acompanhamento
3. **Porte grande**: adiciona cuidado com articulações
4. **Filhote** (< 1 ano): alerta de socialização + treinamento básico

### Saída

```json
{
  "pet_id": 2,
  "idade_anos": 0,
  "idade_anos_detalhe": 0,
  "idade_meses_detalhe": 4,
  "perfil_ia": "medio",
  "recomendacoes": {
    "frequencia_semanal": "3 a 4 vezes por semana",
    "intensidade": "moderada",
    "atividades_sugeridas": ["caminhada", "brincadeiras leves"],
    "cuidados_prioritarios": ["manutenção da rotina de exercícios", "treinamento básico e socialização"],
    "alertas": ["Filhote: priorize socialização e atividades adequadas à idade"]
  }
}
```

Idade formatada no frontend como `1 ano e 2 meses`, `4 meses`, `menos de 1 mês`, etc.

---

## Cronograma Vacinal

21 vacinas recomendadas pré-cadastradas para cães e gatos, seguindo protocolos do **CFMV** e **MAPA** (Brasil):

### Cães

| Vacina | Doses | Idades | Obrigatória |
|---|---|---|---|
| V10 (polivalente) | 3 doses + reforço anual | 6, 9, 12 semanas | ✅ |
| Antirrábica | 1 dose + reforço anual | 12 semanas | ✅ (por lei) |
| Bordetella (tosse dos canis) | 2 doses + reforço anual | 8, 12 semanas | — |
| Giardíase | 2 doses | 8, 11 semanas | — |

### Gatos

| Vacina | Doses | Idades | Obrigatória |
|---|---|---|---|
| V4 (quádrupla felina) | 3 doses + reforço anual | 8, 12, 16 semanas | ✅ |
| Antirrábica | 1 dose + reforço anual | 16 semanas | ✅ (por lei) |
| FeLV (leucemia felina) | 2 doses + reforço anual | 9, 13 semanas | — |

### Funcionamento

O endpoint `GET /api/v1/vacinas/cronograma/{pet_id}`:
1. Busca as vacinas recomendadas para a espécie do pet
2. Calcula a **data prevista** de cada dose: `data_nascimento + idade_semanas`
3. Cruza com as vacinas já aplicadas no histórico (match por nome exato `grupo + dose`)
4. Retorna cada item com status: `aplicada` | `atrasada` | `pendente`

O usuário pode confirmar uma dose com 1 clique via `POST /api/v1/vacinas/confirmar/{pet_id}/{rec_id}`, que cria automaticamente o registro e agenda o próximo reforço anual.

---

## Testes

**52 testes automatizados** com pytest + SQLite in-memory (não requer PostgreSQL rodando).

```bash
# Com Docker rodando
docker compose exec api pytest -v

# Local
cd backend && pytest -v
```

**Cobertura:**

| Arquivo | Testes |
|---|---|
| `test_racas.py` | 8 |
| `test_pets.py` | 11 |
| `test_vacinas.py` | 12 |
| `test_atividades.py` | 10 |
| `test_passeios.py` | 11 |

---

## Docker

### Serviços

**`db`** — PostgreSQL 15 Alpine
- Volume `petcare_pgdata` (dados do banco)
- Healthcheck com `pg_isready` antes de liberar a API

**`api`** — FastAPI + Uvicorn (python:3.11-slim)
- Hot reload em `ENVIRONMENT=development`
- 2 workers em `ENVIRONMENT=production`
- Volume `petcare_uploads` para fotos dos pets
- Healthcheck em `/health`
- Depende de `db` saudável

**`frontend`** — React + Nginx (multi-stage)
- Build com Node 20 Alpine + `npm run build`
- Runtime com Nginx Alpine servindo `/dist`
- Proxy `/api` → `api:8000` + gzip + SPA fallback
- Depende de `api` saudável

### Volumes

| Volume | Propósito |
|---|---|
| `petcare_pgdata` | Dados do PostgreSQL |
| `petcare_uploads` | Fotos dos pets (servidas em `/uploads/`) |

### Comandos úteis

```bash
# Ver logs de um serviço
docker compose logs -f api

# Entrar no container da API
docker compose exec api bash

# Reset completo (apaga banco e fotos)
docker compose down -v && docker compose up --build

# Rodar apenas os testes
docker compose exec api pytest -v
```

---

## Documentação Adicional

- 📄 **PDF completo** com screenshots e arquitetura: `docs/PetCare_Manager_Documentacao.pdf`
- 🖼️ **Diagrama de arquitetura**: `docs/arquitetura.png`
- 📸 **Screenshots**: `docs/screenshots/`

Para regenerar o PDF:

```bash
pip install fpdf2 playwright pillow
python -m playwright install chromium
docker compose up -d
python gerar_documentacao.py
```

---

*"Cuidar bem de um pet é um ato de amor que começa com organização."* 🐾

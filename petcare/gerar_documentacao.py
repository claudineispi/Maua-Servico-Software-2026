"""
PetCare Manager - Gerador de Documentacao PDF
Captura screenshots da aplicacao rodando + diagrama de arquitetura.
Requer: pip install fpdf2 playwright pillow && python -m playwright install chromium
Requer: docker compose up (app rodando em localhost:3000 / 8000)
"""
import os
import time
import json
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

BASE_DIR = Path(__file__).parent
SHOTS_DIR = BASE_DIR / "docs" / "screenshots"
DOCS_DIR = BASE_DIR / "docs"
SHOTS_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND = "http://localhost:3000"
API = "http://localhost:8000"


# ═══════════════════════════════════════════════════════════
# 1. SCREENSHOTS
# ═══════════════════════════════════════════════════════════

def wait_for_app():
    """Aguarda a aplicacao estar disponivel."""
    print("Aguardando aplicacao...")
    for _ in range(30):
        try:
            urllib.request.urlopen(f"{API}/health", timeout=2)
            urllib.request.urlopen(FRONTEND, timeout=2)
            print("Aplicacao pronta!")
            return True
        except Exception:
            time.sleep(2)
    print("ERRO: Aplicacao nao respondeu. Certifique-se de rodar: docker compose up")
    return False


def ensure_test_data():
    """Garante que ha pelo menos 1 pet para as screenshots."""
    try:
        req = urllib.request.urlopen(f"{API}/api/v1/pets/")
        pets = json.loads(req.read())
        if len(pets) > 0:
            return pets[0]["id"]
    except Exception:
        pass

    # Cria um pet de exemplo
    racas_req = urllib.request.urlopen(f"{API}/api/v1/racas/")
    racas = json.loads(racas_req.read())
    raca_id = racas[0]["id"] if racas else 1

    data = json.dumps({
        "nome": "Rex",
        "raca_id": raca_id,
        "data_nascimento": "2023-06-15",
        "sexo": "macho",
        "peso_kg": 28.5,
        "cor": "Dourado",
    }).encode()
    req = urllib.request.Request(
        f"{API}/api/v1/pets/", data=data,
        headers={"Content-Type": "application/json"},
    )
    resp = urllib.request.urlopen(req)
    pet = json.loads(resp.read())
    return pet["id"]


def capture_screenshots():
    """Captura screenshots de todas as telas principais."""
    from playwright.sync_api import sync_playwright

    screens = [
        ("01_dashboard", "/", "Dashboard"),
        ("02_meus_pets", "/pets", "Meus Pets"),
        ("04_vacinas", "/vacinas", "Controle Vacinal"),
        ("05_atividades", "/atividades", "Atividades & Passeios"),
        ("06_cuidados", "/cuidados", "Guia de Cuidados"),
    ]

    pet_id = ensure_test_data()
    pet_screens = [
        ("03_pet_detalhe_vacinas", f"/pets/{pet_id}?tab=vacinas", "Detalhe do Pet - Vacinas"),
        ("03b_pet_detalhe_atividades", f"/pets/{pet_id}?tab=atividades", "Detalhe do Pet - Atividades"),
        ("03c_pet_detalhe_cuidados", f"/pets/{pet_id}?tab=cuidados", "Detalhe do Pet - Cuidados"),
    ]
    screens.extend(pet_screens)

    # Swagger
    screens.append(("07_swagger", None, "Swagger API Docs"))

    print(f"Capturando {len(screens)} screenshots...")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        for filename, path, label in screens:
            filepath = SHOTS_DIR / f"{filename}.png"
            if path is None:
                # Swagger
                page.goto(f"{API}/docs", wait_until="networkidle")
                time.sleep(2)
            else:
                page.goto(f"{FRONTEND}{path}", wait_until="networkidle")
                time.sleep(1.5)

                # Na tela de cuidados, seleciona Golden Retriever
                if "cuidados" in path and "pets" not in path:
                    try:
                        page.select_option("select.form-select", "1")
                        time.sleep(1)
                    except Exception:
                        pass

            page.screenshot(path=str(filepath), full_page=False)
            print(f"  OK: {label} -> {filepath.name}")

        browser.close()

    print(f"Screenshots salvas em: {SHOTS_DIR}")
    return sorted(SHOTS_DIR.glob("*.png"))


# ═══════════════════════════════════════════════════════════
# 2. DIAGRAMA DE ARQUITETURA
# ═══════════════════════════════════════════════════════════

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def generate_architecture_diagram():
    """Gera diagrama de arquitetura da aplicacao."""
    W, H = 1400, 850
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_h2 = ImageFont.truetype("arialbd.ttf", 18)
        font_body = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
        font_tech = ImageFont.truetype("ariali.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_h2 = font_title
        font_body = font_title
        font_small = font_title
        font_tech = font_title

    # Cores
    BG_BLUE = "#E8F4FD"
    BG_GREEN = "#E8F5E9"
    BG_ORANGE = "#FFF3E0"
    BG_PURPLE = "#F3E5F5"
    BORDER_BLUE = "#1976D2"
    BORDER_GREEN = "#388E3C"
    BORDER_ORANGE = "#F57C00"
    BORDER_PURPLE = "#7B1FA2"
    DARK = "#333333"
    GRAY = "#757575"
    ARROW = "#546E7A"

    # Titulo
    draw.text((W // 2 - 200, 20), "PetCare Manager - Arquitetura", fill=DARK, font=font_title)
    draw.text((W // 2 - 100, 55), "Docker Compose (3 servicos)", fill=GRAY, font=font_body)

    # ── BLOCO FRONTEND ──
    fx, fy = 50, 100
    fw, fh = 380, 320
    draw_rounded_rect(draw, (fx, fy, fx + fw, fy + fh), 12, BG_BLUE, BORDER_BLUE, 2)
    draw.text((fx + 15, fy + 12), "Frontend (petcare_frontend)", fill=BORDER_BLUE, font=font_h2)
    draw.text((fx + 15, fy + 40), "Container: nginx:alpine", fill=GRAY, font=font_tech)
    draw.text((fx + 15, fy + 58), "Porta: 3000", fill=GRAY, font=font_tech)

    # Sub-boxes frontend
    items_fe = [
        ("React 18 + Vite", "SPA com React Router v6"),
        ("Axios (api.js)", "Comunicacao com a API REST"),
        ("Pages", "Dashboard, Pets, PetDetail,\nVacinas, Atividades, Cuidados"),
        ("Nginx", "Proxy reverso /api -> api:8000\nServidor de arquivos estaticos"),
    ]
    by = fy + 82
    for title, desc in items_fe:
        draw_rounded_rect(draw, (fx + 12, by, fx + fw - 12, by + 48), 6, "#FFFFFF", "#90CAF9", 1)
        draw.text((fx + 20, by + 5), title, fill=DARK, font=font_h2)
        draw.text((fx + 20, by + 26), desc, fill=GRAY, font=font_small)
        by += 55

    # ── BLOCO API ──
    ax, ay = 510, 100
    aw, ah = 380, 320
    draw_rounded_rect(draw, (ax, ay, ax + aw, ay + ah), 12, BG_GREEN, BORDER_GREEN, 2)
    draw.text((ax + 15, ay + 12), "API (petcare_api)", fill=BORDER_GREEN, font=font_h2)
    draw.text((ax + 15, ay + 40), "Container: python:3.11-slim", fill=GRAY, font=font_tech)
    draw.text((ax + 15, ay + 58), "Porta: 8000 | FastAPI + Uvicorn", fill=GRAY, font=font_tech)

    items_api = [
        ("Routers (6)", "pets, racas, vacinas,\natividades, passeios, cuidados"),
        ("Models (SQLAlchemy 2.0)", "Raca, Pet, Vacina, Atividade,\nPasseio, Cuidado"),
        ("Schemas (Pydantic v2)", "Validacao de entrada/saida\ncom DTOs tipados"),
        ("Seed (seed.py)", "14 racas + 70 cuidados\ncarregados no startup"),
    ]
    by = ay + 82
    for title, desc in items_api:
        draw_rounded_rect(draw, (ax + 12, by, ax + aw - 12, by + 48), 6, "#FFFFFF", "#A5D6A7", 1)
        draw.text((ax + 20, by + 5), title, fill=DARK, font=font_h2)
        draw.text((ax + 20, by + 26), desc, fill=GRAY, font=font_small)
        by += 55

    # ── BLOCO BANCO ──
    dx, dy = 970, 100
    dw, dh = 380, 200
    draw_rounded_rect(draw, (dx, dy, dx + dw, dy + dh), 12, BG_ORANGE, BORDER_ORANGE, 2)
    draw.text((dx + 15, dy + 12), "Banco (petcare_db)", fill=BORDER_ORANGE, font=font_h2)
    draw.text((dx + 15, dy + 40), "Container: postgres:15-alpine", fill=GRAY, font=font_tech)
    draw.text((dx + 15, dy + 58), "Porta: 5432 | Volume: pgdata", fill=GRAY, font=font_tech)

    items_db = [
        ("PostgreSQL 15", "Tabelas: racas, pets, vacinas,\natividades, passeios, cuidados"),
        ("Healthcheck", "pg_isready antes da API subir"),
    ]
    by = dy + 82
    for title, desc in items_db:
        draw_rounded_rect(draw, (dx + 12, by, dx + dw - 12, by + 48), 6, "#FFFFFF", "#FFCC80", 1)
        draw.text((dx + 20, by + 5), title, fill=DARK, font=font_h2)
        draw.text((dx + 20, by + 26), desc, fill=GRAY, font=font_small)
        by += 55

    # ── BLOCO TESTES ──
    tx, ty = 970, 330
    tw, th = 380, 90
    draw_rounded_rect(draw, (tx, ty, tx + tw, ty + th), 12, BG_PURPLE, BORDER_PURPLE, 2)
    draw.text((tx + 15, ty + 12), "Testes (pytest)", fill=BORDER_PURPLE, font=font_h2)
    draw.text((tx + 15, ty + 38), "52 testes | SQLite in-memory", fill=GRAY, font=font_tech)
    draw.text((tx + 15, ty + 56), "test_racas, test_pets, test_vacinas,\ntest_atividades, test_passeios", fill=GRAY, font=font_small)

    # ── SETAS ──
    # Frontend -> API
    draw.line([(fx + fw, fy + fh // 2), (ax, ay + ah // 2)], fill=ARROW, width=3)
    mid_x = (fx + fw + ax) // 2
    draw.text((mid_x - 30, fy + fh // 2 - 20), "HTTP/REST", fill=ARROW, font=font_small)
    draw.text((mid_x - 25, fy + fh // 2 - 5), "/api/v1/*", fill=ARROW, font=font_small)
    # Seta
    draw.polygon([(ax, ay + ah // 2), (ax - 10, ay + ah // 2 - 6), (ax - 10, ay + ah // 2 + 6)], fill=ARROW)

    # API -> DB
    draw.line([(ax + aw, ay + ah // 2 - 40), (dx, dy + dh // 2)], fill=ARROW, width=3)
    mid_x2 = (ax + aw + dx) // 2
    draw.text((mid_x2 - 25, ay + ah // 2 - 65), "SQLAlchemy", fill=ARROW, font=font_small)
    draw.text((mid_x2 - 15, ay + ah // 2 - 50), "TCP 5432", fill=ARROW, font=font_small)
    draw.polygon([(dx, dy + dh // 2), (dx - 10, dy + dh // 2 - 6), (dx - 10, dy + dh // 2 + 6)], fill=ARROW)

    # ── BLOCO USUARIO ──
    ux, uy = 50, 480
    uw, uh = 1300, 50
    draw_rounded_rect(draw, (ux, uy, ux + uw, uy + uh), 8, "#ECEFF1", "#78909C", 1)
    draw.text((ux + 15, uy + 14), "Usuario: Browser -> http://localhost:3000 (Frontend) | http://localhost:8000/docs (Swagger)", fill=DARK, font=font_body)

    # ── LEGENDA DE FUNCIONALIDADES ──
    ly = 560
    draw.text((50, ly), "Funcionalidades Principais", fill=DARK, font=font_title)
    ly += 40

    features = [
        ("Gestao de Pets", "CRUD completo com soft delete. Cadastro com raca, peso, microchip, observacoes."),
        ("Controle Vacinal", "Registro de vacinas aplicadas com alertas de vencimento (30 dias). Dashboard de pendentes."),
        ("Atividades & Passeios", "Registro unificado. Sugestoes de atividades por nivel da raca e passeios por porte."),
        ("Guia de Cuidados", "70 cuidados pre-cadastrados (5 por raca). Categorias: alimentacao, higiene, saude, comportamento, exercicio."),
        ("Dashboard", "Visao geral com total de pets, vacinas pendentes e acesso rapido."),
        ("API REST", "Endpoints em /api/v1/ com documentacao automatica Swagger em /docs."),
    ]

    for title, desc in features:
        draw.ellipse((55, ly + 5, 63, ly + 13), fill=BORDER_GREEN)
        draw.text((72, ly - 2), title, fill=DARK, font=font_h2)
        draw.text((72, ly + 20), desc, fill=GRAY, font=font_body)
        ly += 44

    path = DOCS_DIR / "arquitetura.png"
    img.save(str(path), quality=95)
    print(f"Diagrama salvo: {path}")
    return path


# ═══════════════════════════════════════════════════════════
# 3. PDF
# ═══════════════════════════════════════════════════════════

class PetCarePDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, "PetCare Manager - Documentacao", align="C")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(80, 60, 40)
        self.cell(0, 12, title)
        self.ln(10)
        self.set_draw_color(120, 160, 100)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(60, 90, 60)
        self.cell(0, 10, title)
        self.ln(8)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def add_screenshot(self, img_path, caption):
        if not img_path.exists():
            self.body_text(f"[Screenshot nao disponivel: {caption}]")
            return

        self.section_title(caption)

        img = Image.open(img_path)
        w, h = img.size
        max_w = 190
        ratio = max_w / w
        display_h = h * ratio

        if self.get_y() + display_h + 20 > 270:
            self.add_page()

        self.image(str(img_path), x=10, w=max_w)
        self.ln(8)


def generate_pdf(screenshots, diagram_path):
    """Gera o PDF final."""
    pdf = PetCarePDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── CAPA ──
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 36)
    pdf.set_text_color(80, 60, 40)
    pdf.cell(0, 15, "PetCare Manager", align="C")
    pdf.ln(16)
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(120, 100, 80)
    pdf.cell(0, 10, "Documentacao da Aplicacao", align="C")
    pdf.ln(30)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)

    info = [
        "Projeto de Pos-Graduacao em Servicos de Software",
        "",
        "Stack: Python 3.11 + FastAPI | React 18 + Vite | PostgreSQL 15",
        "Infraestrutura: Docker Compose (3 servicos)",
        "",
        "Versao: 1.0.0",
    ]
    for line in info:
        pdf.cell(0, 7, line, align="C")
        pdf.ln(6)

    # ── 1. VISAO GERAL ──
    pdf.add_page()
    pdf.chapter_title("1. Visao Geral")
    pdf.body_text(
        "O PetCare Manager e uma aplicacao web completa para gestao de animais de estimacao, "
        "permitindo o cadastro de pets, controle vacinal com alertas, registro de atividades "
        "fisicas e passeios, alem de um guia de cuidados especificos por raca.\n\n"
        "A aplicacao foi desenvolvida como projeto de pos-graduacao em Servicos de Software, "
        "utilizando uma arquitetura moderna baseada em microsservicos com Docker Compose."
    )

    pdf.section_title("Funcionalidades")
    features = [
        "- CRUD completo de Pets com soft delete e busca por nome/raca",
        "- Cadastro de 14 racas pre-carregadas (caes e gatos)",
        "- Controle vacinal com alertas de vencimento (janela de 30 dias)",
        "- Registro de atividades fisicas com sugestoes por nivel da raca",
        "- Registro de passeios com sugestoes de locais por porte do pet",
        "- Guia de cuidados por raca (70 cuidados: alimentacao, higiene, saude, etc.)",
        "- Dashboard com estatisticas e alertas globais",
        "- API REST documentada com Swagger automatico",
        "- 52 testes automatizados cobrindo todos os endpoints",
    ]
    pdf.body_text("\n".join(features))

    # ── 2. ARQUITETURA ──
    pdf.add_page()
    pdf.chapter_title("2. Arquitetura")
    pdf.body_text(
        "A aplicacao segue uma arquitetura de 3 camadas orquestrada via Docker Compose:"
    )

    pdf.section_title("Stack Tecnologica")
    stack = (
        "Backend: Python 3.11 + FastAPI 0.111 + SQLAlchemy 2.0 + Pydantic v2\n"
        "Frontend: React 18 + Vite 5.2 + React Router v6 + Axios + date-fns\n"
        "Banco de Dados: PostgreSQL 15 (Alpine)\n"
        "Servidor Web: Nginx Alpine (proxy reverso + SPA)\n"
        "Testes: pytest + SQLite in-memory + httpx (TestClient)"
    )
    pdf.body_text(stack)

    pdf.section_title("Diagrama de Arquitetura")
    if diagram_path and diagram_path.exists():
        pdf.image(str(diagram_path), x=5, w=200)
    pdf.ln(5)

    pdf.section_title("Fluxo de Requisicao")
    pdf.body_text(
        "1. Usuario acessa http://localhost:3000 no navegador\n"
        "2. Nginx serve o SPA React (arquivos estaticos)\n"
        "3. React faz chamadas HTTP via Axios para /api/v1/*\n"
        "4. Nginx faz proxy reverso para http://api:8000\n"
        "5. FastAPI processa a requisicao, valida com Pydantic\n"
        "6. SQLAlchemy executa a query no PostgreSQL\n"
        "7. Resposta JSON retorna ao frontend"
    )

    # ── 3. ESTRUTURA DO PROJETO ──
    pdf.add_page()
    pdf.chapter_title("3. Estrutura do Projeto")
    structure = (
        "petcare/\n"
        "|-- docker-compose.yml          # Orquestra 3 servicos\n"
        "|-- backend/\n"
        "|   |-- Dockerfile              # Python 3.11-slim + curl\n"
        "|   |-- requirements.txt        # Dependencias + pytest\n"
        "|   |-- pytest.ini              # Configuracao dos testes\n"
        "|   |-- app/\n"
        "|   |   |-- main.py             # FastAPI app + CORS + lifespan\n"
        "|   |   |-- database.py         # Engine SQLAlchemy + get_db\n"
        "|   |   |-- seed.py             # Seed: 14 racas + 70 cuidados\n"
        "|   |   |-- models/models.py    # 6 modelos + enums\n"
        "|   |   |-- schemas/schemas.py  # DTOs Pydantic\n"
        "|   |   |-- routers/            # 6 routers REST\n"
        "|   |-- tests/                  # 52 testes automatizados\n"
        "|       |-- conftest.py         # Fixtures (SQLite in-memory)\n"
        "|       |-- test_racas.py       # 8 testes\n"
        "|       |-- test_pets.py        # 11 testes\n"
        "|       |-- test_vacinas.py     # 12 testes\n"
        "|       |-- test_atividades.py  # 10 testes\n"
        "|       |-- test_passeios.py    # 11 testes\n"
        "|-- frontend/\n"
        "    |-- Dockerfile              # Node 20 build + Nginx\n"
        "    |-- nginx.conf              # Proxy + SPA + gzip\n"
        "    |-- src/\n"
        "        |-- App.jsx             # Shell + Sidebar + Rotas\n"
        "        |-- services/api.js     # Axios centralizado\n"
        "        |-- pages/              # 6 paginas React"
    )
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 4.5, structure)
    pdf.ln(5)

    # ── 4. MODELOS DE DADOS ──
    pdf.add_page()
    pdf.chapter_title("4. Modelos de Dados")

    models = [
        ("Raca", "id, nome (unique), especie (enum: cao/gato/outro), porte (enum: pequeno/medio/grande), expectativa_vida_anos, descricao, nivel_atividade, created_at"),
        ("Pet", "id, nome, raca_id (FK), data_nascimento, sexo (enum: macho/femea), peso_kg, cor, microchip (unique), foto_url, observacoes, ativo (soft delete), created_at, updated_at"),
        ("Vacina", "id, pet_id (FK), nome, data_aplicacao, proxima_dose, veterinario, clinica, lote, status (enum: pendente/aplicada/atrasada), observacoes, created_at"),
        ("Atividade", "id, pet_id (FK), tipo, data, duracao_minutos, distancia_km, intensidade, observacoes, created_at"),
        ("Passeio", "id, pet_id (FK), local, data, duracao_minutos, avaliacao (1-5), observacoes, created_at"),
        ("Cuidado", "id, raca_id (FK), categoria, titulo, descricao, frequencia, prioridade"),
    ]
    for name, fields in models:
        pdf.section_title(name)
        pdf.body_text(fields)

    # ── 5. ENDPOINTS DA API ──
    pdf.add_page()
    pdf.chapter_title("5. Endpoints da API")
    pdf.body_text("Base URL: /api/v1 | Documentacao interativa: /docs (Swagger)")
    pdf.ln(3)

    endpoints = [
        ("Pets", [
            "GET    /pets/?ativo=true     Listar pets (ativos/inativos)",
            "POST   /pets/               Criar pet",
            "GET    /pets/{id}            Buscar pet por ID",
            "PUT    /pets/{id}            Atualizar pet",
            "DELETE /pets/{id}            Soft delete do pet",
            "GET    /pets/{id}/dashboard  Dashboard do pet",
        ]),
        ("Racas", [
            "GET    /racas/?especie=cao   Listar racas (filtro por especie)",
            "POST   /racas/              Criar raca",
            "GET    /racas/{id}           Buscar raca",
            "PUT    /racas/{id}           Atualizar raca",
        ]),
        ("Vacinas", [
            "GET    /vacinas/pet/{id}     Vacinas de um pet",
            "GET    /vacinas/pendentes    Vacinas vencidas/proximas (30d)",
            "POST   /vacinas/            Registrar vacina",
            "PUT    /vacinas/{id}         Atualizar vacina",
            "DELETE /vacinas/{id}         Remover vacina",
        ]),
        ("Atividades", [
            "GET    /atividades/pet/{id}       Atividades de um pet",
            "GET    /atividades/sugestoes/{id}  Sugestoes por nivel",
            "POST   /atividades/               Registrar atividade",
            "DELETE /atividades/{id}            Remover atividade",
        ]),
        ("Passeios", [
            "GET    /passeios/pet/{id}       Passeios de um pet",
            "GET    /passeios/sugestoes/{id}  Sugestoes por porte",
            "POST   /passeios/               Registrar passeio",
            "DELETE /passeios/{id}            Remover passeio",
        ]),
        ("Cuidados", [
            "GET    /cuidados/raca/{id}  Cuidados de uma raca",
            "POST   /cuidados/           Criar cuidado",
            "DELETE /cuidados/{id}        Remover cuidado",
        ]),
    ]

    for group, eps in endpoints:
        pdf.section_title(group)
        pdf.set_font("Courier", "", 9)
        pdf.set_text_color(50, 50, 50)
        for ep in eps:
            pdf.cell(0, 4.5, ep)
            pdf.ln(4.5)
        pdf.ln(4)

    # ── 6. PRINTS DE TELA ──
    pdf.add_page()
    pdf.chapter_title("6. Telas da Aplicacao")

    screen_labels = {
        "01_dashboard": "Dashboard - Visao geral com stats e alertas de vacinas",
        "02_meus_pets": "Meus Pets - Listagem com busca e cadastro",
        "03_pet_detalhe_vacinas": "Detalhe do Pet - Aba Vacinas (historico vacinal)",
        "03b_pet_detalhe_atividades": "Detalhe do Pet - Aba Atividades & Passeios",
        "03c_pet_detalhe_cuidados": "Detalhe do Pet - Aba Cuidados",
        "04_vacinas": "Controle Vacinal - Vacinas atrasadas e proximas",
        "05_atividades": "Atividades - Selecao de pet",
        "06_cuidados": "Guia de Cuidados - Cuidados por raca",
        "07_swagger": "Swagger - Documentacao interativa da API",
    }

    for shot in sorted(screenshots):
        name = shot.stem
        caption = screen_labels.get(name, name)
        pdf.add_screenshot(shot, caption)

    # ── 7. COMO EXECUTAR ──
    pdf.add_page()
    pdf.chapter_title("7. Como Executar")

    pdf.section_title("Pre-requisitos")
    pdf.body_text("- Docker e Docker Compose instalados\n- Portas 3000, 5432 e 8000 disponiveis")

    pdf.section_title("Subir a aplicacao")
    pdf.set_font("Courier", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, "cd petcare\ndocker compose up --build")
    pdf.ln(5)

    pdf.section_title("Acessar")
    pdf.body_text(
        "- Frontend: http://localhost:3000\n"
        "- API / Swagger: http://localhost:8000/docs\n"
        "- Banco: localhost:5432 (petcare_user / petcare_secret)"
    )

    pdf.section_title("Executar testes")
    pdf.set_font("Courier", "", 10)
    pdf.multi_cell(0, 5, "docker compose exec api pytest -v")
    pdf.ln(5)
    pdf.body_text("52 testes automatizados usando SQLite in-memory (nao requer PostgreSQL).")

    pdf.section_title("Parar a aplicacao")
    pdf.set_font("Courier", "", 10)
    pdf.multi_cell(0, 5, "docker compose down       # mantem dados\ndocker compose down -v    # apaga volume do banco")

    # ── SALVAR ──
    output = DOCS_DIR / "PetCare_Manager_Documentacao.pdf"
    pdf.output(str(output))
    print(f"\nPDF gerado: {output}")
    return output


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 50)
    print("PetCare Manager - Geracao de Documentacao")
    print("=" * 50)

    # Diagrama (nao precisa da app rodando)
    diagram = generate_architecture_diagram()

    # Screenshots (precisa da app)
    screenshots = []
    if wait_for_app():
        screenshots = capture_screenshots()
    else:
        print("\nGerando PDF sem screenshots (Docker nao esta rodando).")
        print("Para incluir prints, rode: docker compose up && python gerar_documentacao.py")

    # PDF
    pdf_path = generate_pdf(screenshots, diagram)
    print(f"\nConcluido! Abra: {pdf_path}")

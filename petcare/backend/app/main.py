import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.database import engine, Base, SessionLocal
from app.routers import pets, racas, vacinas, atividades, passeios, cuidados
from app.seed import seed_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Cria diretório de uploads
    os.makedirs("/app/uploads/pets", exist_ok=True)
    # 2. Cria tabelas (idempotente — não recria se já existem)
    Base.metadata.create_all(bind=engine)
    # 3. Popula dados iniciais (idempotente — só insere se banco estiver vazio)
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="PetCare Manager API",
    description="""
    ## 🐾 API de Gestão de Pets

    Sistema completo para gerenciamento de animais de estimação.

    ### Funcionalidades:
    - **Pets**: Cadastro e gestão de animais
    - **Raças**: Informações por raça com cuidados específicos
    - **Vacinas**: Calendário vacinal e controle de imunização
    - **Atividades**: Registro e recomendação de atividades físicas
    - **Passeios**: Sugestões de locais e roteiros
    - **Cuidados**: Guia personalizado por raça
    """,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(racas.router, prefix="/api/v1/racas", tags=["Raças"])
app.include_router(pets.router, prefix="/api/v1/pets", tags=["Pets"])
app.include_router(vacinas.router, prefix="/api/v1/vacinas", tags=["Vacinas"])
app.include_router(atividades.router, prefix="/api/v1/atividades", tags=["Atividades"])
app.include_router(passeios.router, prefix="/api/v1/passeios", tags=["Passeios"])
app.include_router(cuidados.router, prefix="/api/v1/cuidados", tags=["Cuidados"])

app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "PetCare Manager API 🐾", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

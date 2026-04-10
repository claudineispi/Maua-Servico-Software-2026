"""
Fixtures compartilhadas entre todos os testes.
Usa SQLite in-memory para não depender de PostgreSQL rodando.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLITE_URL = "sqlite://"

engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── helpers reutilizáveis ──────────────────────────────────

def criar_raca(client, nome="Labrador", especie="cao", porte="grande", nivel_atividade="alto"):
    r = client.post("/api/v1/racas/", json={
        "nome": nome,
        "especie": especie,
        "porte": porte,
        "nivel_atividade": nivel_atividade,
    })
    assert r.status_code == 201, r.text
    return r.json()


def criar_pet(client, raca_id, nome="Rex", sexo="macho", data_nascimento="2022-01-01"):
    r = client.post("/api/v1/pets/", json={
        "nome": nome,
        "raca_id": raca_id,
        "data_nascimento": data_nascimento,
        "sexo": sexo,
    })
    assert r.status_code == 201, r.text
    return r.json()

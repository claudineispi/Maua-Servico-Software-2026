"""Testes para /api/v1/racas/"""
from tests.conftest import criar_raca


def test_criar_raca(client):
    r = client.post("/api/v1/racas/", json={
        "nome": "Golden Retriever",
        "especie": "cao",
        "porte": "grande",
        "nivel_atividade": "alto",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["nome"] == "Golden Retriever"
    assert data["especie"] == "cao"
    assert data["id"] is not None


def test_listar_racas(client):
    criar_raca(client, nome="Labrador", especie="cao")
    criar_raca(client, nome="Persa", especie="gato", porte="pequeno", nivel_atividade="baixo")

    r = client.get("/api/v1/racas/")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_filtrar_racas_por_especie(client):
    criar_raca(client, nome="Poodle", especie="cao", porte="pequeno")
    criar_raca(client, nome="Maine Coon", especie="gato", porte="grande")

    r = client.get("/api/v1/racas/?especie=cao")
    assert r.status_code == 200
    nomes = [x["nome"] for x in r.json()]
    assert "Poodle" in nomes
    assert "Maine Coon" not in nomes


def test_filtrar_racas_especie_invalida(client):
    r = client.get("/api/v1/racas/?especie=peixe")
    assert r.status_code == 422


def test_buscar_raca_por_id(client):
    raca = criar_raca(client)
    r = client.get(f"/api/v1/racas/{raca['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == raca["id"]


def test_buscar_raca_inexistente(client):
    r = client.get("/api/v1/racas/9999")
    assert r.status_code == 404


def test_atualizar_raca(client):
    raca = criar_raca(client)
    r = client.put(f"/api/v1/racas/{raca['id']}", json={"nivel_atividade": "baixo"})
    assert r.status_code == 200
    assert r.json()["nivel_atividade"] == "baixo"


def test_nao_permite_raca_duplicada(client):
    criar_raca(client, nome="Bulldog")
    r = client.post("/api/v1/racas/", json={"nome": "Bulldog", "especie": "cao", "porte": "medio"})
    # Nome único — banco deve rejeitar
    assert r.status_code in (400, 422, 500)

"""Testes para /api/v1/pets/"""
from tests.conftest import criar_raca, criar_pet


def test_criar_pet(client):
    raca = criar_raca(client)
    r = client.post("/api/v1/pets/", json={
        "nome": "Rex",
        "raca_id": raca["id"],
        "data_nascimento": "2022-06-15",
        "sexo": "macho",
        "peso_kg": 30.5,
    })
    assert r.status_code == 201
    data = r.json()
    assert data["nome"] == "Rex"
    assert data["ativo"] is True
    assert data["raca"]["id"] == raca["id"]


def test_criar_pet_campos_obrigatorios(client):
    r = client.post("/api/v1/pets/", json={"nome": "Sem Raca"})
    assert r.status_code == 422


def test_listar_pets_ativos(client):
    raca = criar_raca(client)
    criar_pet(client, raca["id"], nome="Ativo")
    pet_inativo = criar_pet(client, raca["id"], nome="Inativo")
    client.delete(f"/api/v1/pets/{pet_inativo['id']}")  # soft delete

    r = client.get("/api/v1/pets/")
    nomes = [p["nome"] for p in r.json()]
    assert "Ativo" in nomes
    assert "Inativo" not in nomes


def test_listar_pets_inativos(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"], nome="Arquivado")
    client.delete(f"/api/v1/pets/{pet['id']}")

    r = client.get("/api/v1/pets/?ativo=false")
    nomes = [p["nome"] for p in r.json()]
    assert "Arquivado" in nomes


def test_buscar_pet_por_id(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    r = client.get(f"/api/v1/pets/{pet['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == pet["id"]


def test_buscar_pet_inexistente(client):
    r = client.get("/api/v1/pets/9999")
    assert r.status_code == 404


def test_atualizar_pet(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    r = client.put(f"/api/v1/pets/{pet['id']}", json={"peso_kg": 25.0, "cor": "Dourado"})
    assert r.status_code == 200
    data = r.json()
    assert data["peso_kg"] == 25.0
    assert data["cor"] == "Dourado"


def test_soft_delete_pet(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])

    r = client.delete(f"/api/v1/pets/{pet['id']}")
    assert r.status_code == 204

    # Não aparece na listagem de ativos
    r = client.get("/api/v1/pets/")
    ids = [p["id"] for p in r.json()]
    assert pet["id"] not in ids


def test_delete_pet_inexistente(client):
    r = client.delete("/api/v1/pets/9999")
    assert r.status_code == 404


def test_dashboard_pet(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])

    r = client.get(f"/api/v1/pets/{pet['id']}/dashboard")
    assert r.status_code == 200
    data = r.json()
    assert data["total_vacinas"] == 0
    assert data["vacinas_pendentes"] == 0
    assert data["total_atividades"] == 0
    assert data["total_passeios"] == 0


def test_dashboard_conta_vacinas_pendentes(client):
    from datetime import date, timedelta
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])

    proxima = (date.today() + timedelta(days=10)).isoformat()
    client.post("/api/v1/vacinas/", json={
        "pet_id": pet["id"],
        "nome": "V10",
        "data_aplicacao": "2024-01-01",
        "proxima_dose": proxima,
    })

    r = client.get(f"/api/v1/pets/{pet['id']}/dashboard")
    assert r.status_code == 200
    assert r.json()["vacinas_pendentes"] == 1

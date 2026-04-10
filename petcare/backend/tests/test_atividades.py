"""Testes para /api/v1/atividades/"""
from tests.conftest import criar_raca, criar_pet


def _criar_atividade(client, pet_id, tipo="Caminhada", data="2024-03-10"):
    r = client.post("/api/v1/atividades/", json={
        "pet_id": pet_id,
        "tipo": tipo,
        "data": data,
        "duracao_minutos": 30,
        "intensidade": "moderada",
    })
    assert r.status_code == 201, r.text
    return r.json()


def test_registrar_atividade(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    at = _criar_atividade(client, pet["id"])
    assert at["tipo"] == "Caminhada"
    assert at["pet_id"] == pet["id"]


def test_registrar_atividade_pet_inexistente(client):
    r = client.post("/api/v1/atividades/", json={
        "pet_id": 9999,
        "tipo": "Corrida",
        "data": "2024-01-01",
    })
    assert r.status_code == 404


def test_registrar_atividade_pet_inativo(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    client.delete(f"/api/v1/pets/{pet['id']}")

    r = client.post("/api/v1/atividades/", json={
        "pet_id": pet["id"],
        "tipo": "Corrida",
        "data": "2024-01-01",
    })
    assert r.status_code == 404


def test_listar_atividades_pet(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    _criar_atividade(client, pet["id"], tipo="Natação", data="2024-03-01")
    _criar_atividade(client, pet["id"], tipo="Agility", data="2024-03-05")

    r = client.get(f"/api/v1/atividades/pet/{pet['id']}")
    assert r.status_code == 200
    tipos = [a["tipo"] for a in r.json()]
    assert "Natação" in tipos
    assert "Agility" in tipos


def test_listar_atividades_ordenadas_por_data(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    _criar_atividade(client, pet["id"], tipo="Primeira", data="2024-01-01")
    _criar_atividade(client, pet["id"], tipo="Segunda", data="2024-03-01")

    r = client.get(f"/api/v1/atividades/pet/{pet['id']}")
    assert r.status_code == 200
    # Ordenado desc — mais recente primeiro
    assert r.json()[0]["tipo"] == "Segunda"


def test_listar_atividades_pet_inexistente(client):
    r = client.get("/api/v1/atividades/pet/9999")
    assert r.status_code == 404


def test_sugestoes_atividades(client):
    raca = criar_raca(client, nivel_atividade="alto")
    pet = criar_pet(client, raca["id"])

    r = client.get(f"/api/v1/atividades/sugestoes/{pet['id']}")
    assert r.status_code == 200
    data = r.json()
    assert data["nivel_atividade"] == "alto"
    assert len(data["sugestoes"]) > 0


def test_sugestoes_atividades_nivel_medio_por_padrao(client):
    # Raça sem nivel_atividade → deve usar "medio"
    raca = criar_raca(client, nivel_atividade=None)
    pet = criar_pet(client, raca["id"])

    r = client.get(f"/api/v1/atividades/sugestoes/{pet['id']}")
    assert r.status_code == 200
    assert r.json()["nivel_atividade"] == "medio"


def test_sugestoes_pet_inexistente(client):
    r = client.get("/api/v1/atividades/sugestoes/9999")
    assert r.status_code == 404


def test_deletar_atividade(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    at = _criar_atividade(client, pet["id"])

    r = client.delete(f"/api/v1/atividades/{at['id']}")
    assert r.status_code == 204

    r = client.get(f"/api/v1/atividades/pet/{pet['id']}")
    assert len(r.json()) == 0


def test_deletar_atividade_inexistente(client):
    r = client.delete("/api/v1/atividades/9999")
    assert r.status_code == 404

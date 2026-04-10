"""Testes para /api/v1/passeios/"""
from tests.conftest import criar_raca, criar_pet


def _criar_passeio(client, pet_id, local="Parque Central", data="2024-04-01"):
    r = client.post("/api/v1/passeios/", json={
        "pet_id": pet_id,
        "local": local,
        "data": data,
        "duracao_minutos": 45,
        "avaliacao": 5,
    })
    assert r.status_code == 201, r.text
    return r.json()


def test_registrar_passeio(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    p = _criar_passeio(client, pet["id"])
    assert p["local"] == "Parque Central"
    assert p["pet_id"] == pet["id"]
    assert p["avaliacao"] == 5


def test_registrar_passeio_pet_inexistente(client):
    r = client.post("/api/v1/passeios/", json={
        "pet_id": 9999,
        "local": "Parque",
        "data": "2024-01-01",
    })
    assert r.status_code == 404


def test_registrar_passeio_pet_inativo(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    client.delete(f"/api/v1/pets/{pet['id']}")

    r = client.post("/api/v1/passeios/", json={
        "pet_id": pet["id"],
        "local": "Parque",
        "data": "2024-01-01",
    })
    assert r.status_code == 404


def test_listar_passeios_pet(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    _criar_passeio(client, pet["id"], local="Praia", data="2024-03-01")
    _criar_passeio(client, pet["id"], local="Serra", data="2024-04-01")

    r = client.get(f"/api/v1/passeios/pet/{pet['id']}")
    assert r.status_code == 200
    locais = [p["local"] for p in r.json()]
    assert "Praia" in locais
    assert "Serra" in locais


def test_listar_passeios_ordenados_por_data(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    _criar_passeio(client, pet["id"], local="Antigo", data="2024-01-01")
    _criar_passeio(client, pet["id"], local="Recente", data="2024-06-01")

    r = client.get(f"/api/v1/passeios/pet/{pet['id']}")
    assert r.status_code == 200
    assert r.json()[0]["local"] == "Recente"


def test_listar_passeios_pet_inexistente(client):
    r = client.get("/api/v1/passeios/pet/9999")
    assert r.status_code == 404


def test_sugestoes_passeios_por_porte(client):
    raca = criar_raca(client, porte="pequeno")
    pet = criar_pet(client, raca["id"])

    r = client.get(f"/api/v1/passeios/sugestoes/{pet['id']}")
    assert r.status_code == 200
    data = r.json()
    assert data["porte"] == "pequeno"
    assert len(data["sugestoes"]) > 0


def test_sugestoes_passeios_pet_inexistente(client):
    r = client.get("/api/v1/passeios/sugestoes/9999")
    assert r.status_code == 404


def test_deletar_passeio(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    p = _criar_passeio(client, pet["id"])

    r = client.delete(f"/api/v1/passeios/{p['id']}")
    assert r.status_code == 204

    r = client.get(f"/api/v1/passeios/pet/{pet['id']}")
    assert len(r.json()) == 0


def test_deletar_passeio_inexistente(client):
    r = client.delete("/api/v1/passeios/9999")
    assert r.status_code == 404


def test_avaliacao_invalida_rejeitada(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    r = client.post("/api/v1/passeios/", json={
        "pet_id": pet["id"],
        "local": "Parque",
        "data": "2024-01-01",
        "avaliacao": 10,  # inválido: máximo é 5
    })
    assert r.status_code == 422

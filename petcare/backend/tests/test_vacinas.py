"""Testes para /api/v1/vacinas/"""
from datetime import date, timedelta
from tests.conftest import criar_raca, criar_pet


def _criar_vacina(client, pet_id, nome="V10", proxima_dose=None):
    payload = {
        "pet_id": pet_id,
        "nome": nome,
        "data_aplicacao": "2024-01-01",
        "status": "aplicada",
    }
    if proxima_dose:
        payload["proxima_dose"] = proxima_dose
    r = client.post("/api/v1/vacinas/", json=payload)
    assert r.status_code == 201, r.text
    return r.json()


def test_registrar_vacina(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    v = _criar_vacina(client, pet["id"])
    assert v["nome"] == "V10"
    assert v["pet_id"] == pet["id"]


def test_registrar_vacina_pet_inexistente(client):
    r = client.post("/api/v1/vacinas/", json={
        "pet_id": 9999,
        "nome": "V10",
        "data_aplicacao": "2024-01-01",
    })
    assert r.status_code == 404


def test_registrar_vacina_pet_inativo(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    client.delete(f"/api/v1/pets/{pet['id']}")

    r = client.post("/api/v1/vacinas/", json={
        "pet_id": pet["id"],
        "nome": "V10",
        "data_aplicacao": "2024-01-01",
    })
    assert r.status_code == 404


def test_listar_vacinas_do_pet(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    _criar_vacina(client, pet["id"], nome="Antirrábica")
    _criar_vacina(client, pet["id"], nome="V8")

    r = client.get(f"/api/v1/vacinas/pet/{pet['id']}")
    assert r.status_code == 200
    nomes = [v["nome"] for v in r.json()]
    assert "Antirrábica" in nomes
    assert "V8" in nomes


def test_listar_vacinas_pet_inexistente(client):
    r = client.get("/api/v1/vacinas/pet/9999")
    assert r.status_code == 404


def test_listar_vacinas_pet_inativo(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    _criar_vacina(client, pet["id"])
    client.delete(f"/api/v1/pets/{pet['id']}")

    r = client.get(f"/api/v1/vacinas/pet/{pet['id']}")
    assert r.status_code == 404


def test_pendentes_retorna_vacinas_vencidas(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    vencida = (date.today() - timedelta(days=5)).isoformat()
    _criar_vacina(client, pet["id"], proxima_dose=vencida)

    r = client.get("/api/v1/vacinas/pendentes")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_pendentes_retorna_vacinas_proximas(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    em_breve = (date.today() + timedelta(days=15)).isoformat()
    _criar_vacina(client, pet["id"], proxima_dose=em_breve)

    r = client.get("/api/v1/vacinas/pendentes")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_pendentes_ignora_vacinas_longe_do_vencimento(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    longe = (date.today() + timedelta(days=60)).isoformat()
    _criar_vacina(client, pet["id"], proxima_dose=longe)

    r = client.get("/api/v1/vacinas/pendentes")
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_pendentes_ignora_pets_inativos(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    vencida = (date.today() - timedelta(days=1)).isoformat()
    _criar_vacina(client, pet["id"], proxima_dose=vencida)
    client.delete(f"/api/v1/pets/{pet['id']}")

    r = client.get("/api/v1/vacinas/pendentes")
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_atualizar_vacina(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    v = _criar_vacina(client, pet["id"])
    nova_data = (date.today() + timedelta(days=365)).isoformat()

    r = client.put(f"/api/v1/vacinas/{v['id']}", json={"proxima_dose": nova_data, "status": "aplicada"})
    assert r.status_code == 200
    assert r.json()["proxima_dose"] == nova_data


def test_deletar_vacina(client):
    raca = criar_raca(client)
    pet = criar_pet(client, raca["id"])
    v = _criar_vacina(client, pet["id"])

    r = client.delete(f"/api/v1/vacinas/{v['id']}")
    assert r.status_code == 204

    r = client.get(f"/api/v1/vacinas/pet/{pet['id']}")
    assert len(r.json()) == 0


def test_deletar_vacina_inexistente(client):
    r = client.delete("/api/v1/vacinas/9999")
    assert r.status_code == 404

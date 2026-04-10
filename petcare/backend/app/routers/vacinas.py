from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from app.database import get_db
from app.models.models import Vacina, Pet, VacinaRecomendada
from app.schemas.schemas import (
    VacinaCreate, VacinaUpdate, VacinaResponse,
    VacinaRecomendadaResponse, CronogramaItem,
)

router = APIRouter()


def _get_pet_ativo(pet_id: int, db: Session) -> Pet:
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.ativo == True).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet


@router.get("/pet/{pet_id}", response_model=List[VacinaResponse])
def listar_vacinas_pet(pet_id: int, db: Session = Depends(get_db)):
    _get_pet_ativo(pet_id, db)
    return db.query(Vacina).filter(Vacina.pet_id == pet_id).order_by(Vacina.data_aplicacao.desc()).all()


@router.get("/pendentes", response_model=List[VacinaResponse])
def vacinas_pendentes(db: Session = Depends(get_db)):
    """Retorna todas as vacinas com reforço vencido ou próximo do vencimento (30 dias)"""
    limite = date.today() + timedelta(days=30)
    return (
        db.query(Vacina)
        .join(Pet, Vacina.pet_id == Pet.id)
        .filter(Pet.ativo == True, Vacina.proxima_dose != None, Vacina.proxima_dose <= limite)
        .all()
    )


@router.get("/cronograma/{pet_id}", response_model=List[CronogramaItem])
def cronograma_vacinal(pet_id: int, db: Session = Depends(get_db)):
    """
    Retorna o cronograma vacinal personalizado para um pet,
    baseado na espécie e data de nascimento.
    Cruza vacinas recomendadas com vacinas já aplicadas.
    """
    pet = _get_pet_ativo(pet_id, db)
    especie = pet.raca.especie if pet.raca else "cao"
    nascimento = pet.data_nascimento

    # Busca vacinas recomendadas para a espécie
    recomendadas = (
        db.query(VacinaRecomendada)
        .filter(VacinaRecomendada.especie == especie)
        .order_by(VacinaRecomendada.idade_semanas, VacinaRecomendada.grupo)
        .all()
    )

    # Busca vacinas já aplicadas no pet
    aplicadas = db.query(Vacina).filter(Vacina.pet_id == pet_id).all()
    # Indexa por nome exato da vacina recomendada para matching preciso
    aplicadas_map = {}
    for v in aplicadas:
        nome_lower = v.nome.lower().strip()
        for rec in recomendadas:
            rec_nome_lower = rec.nome.lower().strip()
            # Match exato: "v10 - 1a dose" == "v10 - 1a dose"
            if nome_lower == rec_nome_lower:
                key = f"{rec.grupo}_{rec.dose}"
                if key not in aplicadas_map:
                    aplicadas_map[key] = v
                break

    hoje = date.today()
    cronograma = []

    for rec in recomendadas:
        data_prevista = nascimento + timedelta(weeks=rec.idade_semanas)
        key = f"{rec.grupo}_{rec.dose}"
        vacina_aplicada = aplicadas_map.get(key)

        if vacina_aplicada:
            item_status = "aplicada"
        elif data_prevista < hoje:
            item_status = "atrasada"
        else:
            item_status = "pendente"

        cronograma.append(CronogramaItem(
            vacina_recomendada=rec,
            data_prevista=data_prevista,
            status=item_status,
            vacina_aplicada_id=vacina_aplicada.id if vacina_aplicada else None,
        ))

    return cronograma


@router.post("/confirmar/{pet_id}/{recomendada_id}", response_model=VacinaResponse, status_code=status.HTTP_201_CREATED)
def confirmar_vacina_cronograma(
    pet_id: int,
    recomendada_id: int,
    db: Session = Depends(get_db),
):
    """Confirma a aplicação de uma vacina do cronograma, criando o registro."""
    pet = _get_pet_ativo(pet_id, db)
    rec = db.query(VacinaRecomendada).filter(VacinaRecomendada.id == recomendada_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Vacina recomendada não encontrada")

    # Calcula próxima dose se houver reforço anual
    proxima = None
    if rec.reforco_anual:
        proxima = date.today() + timedelta(days=365)

    db_vacina = Vacina(
        pet_id=pet_id,
        nome=f"{rec.grupo} - {rec.dose}a dose",
        data_aplicacao=date.today(),
        proxima_dose=proxima,
        status="aplicada",
        observacoes=f"Confirmada via cronograma vacinal (recomendada #{rec.id})",
    )
    db.add(db_vacina)
    db.commit()
    db.refresh(db_vacina)
    return db_vacina


@router.post("/", response_model=VacinaResponse, status_code=status.HTTP_201_CREATED)
def registrar_vacina(vacina: VacinaCreate, db: Session = Depends(get_db)):
    _get_pet_ativo(vacina.pet_id, db)
    db_vacina = Vacina(**vacina.model_dump())
    db.add(db_vacina)
    db.commit()
    db.refresh(db_vacina)
    return db_vacina


@router.put("/{vacina_id}", response_model=VacinaResponse)
def atualizar_vacina(vacina_id: int, dados: VacinaUpdate, db: Session = Depends(get_db)):
    vacina = db.query(Vacina).filter(Vacina.id == vacina_id).first()
    if not vacina:
        raise HTTPException(status_code=404, detail="Vacina não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(vacina, campo, valor)
    db.commit()
    db.refresh(vacina)
    return vacina


@router.delete("/{vacina_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_vacina(vacina_id: int, db: Session = Depends(get_db)):
    vacina = db.query(Vacina).filter(Vacina.id == vacina_id).first()
    if not vacina:
        raise HTTPException(status_code=404, detail="Vacina não encontrada")
    db.delete(vacina)
    db.commit()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from app.database import get_db
from app.models.models import Vacina, Pet
from app.schemas.schemas import VacinaCreate, VacinaUpdate, VacinaResponse

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

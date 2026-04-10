from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from app.database import get_db
from app.models.models import Pet, Vacina, Atividade, Passeio, StatusVacinaEnum
from app.schemas.schemas import PetCreate, PetUpdate, PetResponse, DashboardPet

router = APIRouter()


@router.get("/", response_model=List[PetResponse])
def listar_pets(ativo: bool = True, db: Session = Depends(get_db)):
    return db.query(Pet).filter(Pet.ativo == ativo).all()


@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def criar_pet(pet: PetCreate, db: Session = Depends(get_db)):
    db_pet = Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


@router.get("/{pet_id}", response_model=PetResponse)
def buscar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet


@router.put("/{pet_id}", response_model=PetResponse)
def atualizar_pet(pet_id: int, dados: PetUpdate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(pet, campo, valor)
    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    pet.ativo = False  # soft delete
    db.commit()


@router.get("/{pet_id}/dashboard", response_model=DashboardPet)
def dashboard_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    vacinas = db.query(Vacina).filter(Vacina.pet_id == pet_id).all()
    limite = date.today() + timedelta(days=30)
    pendentes = [v for v in vacinas if v.proxima_dose and v.proxima_dose <= limite]
    atividades = db.query(Atividade).filter(Atividade.pet_id == pet_id).all()
    passeios = db.query(Passeio).filter(Passeio.pet_id == pet_id).all()

    ultima = max([a.data for a in atividades], default=None) if atividades else None

    return DashboardPet(
        pet=pet,
        total_vacinas=len(vacinas),
        vacinas_pendentes=len(pendentes),
        total_atividades=len(atividades),
        ultima_atividade=ultima,
        total_passeios=len(passeios),
    )

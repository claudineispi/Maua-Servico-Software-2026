from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Passeio, Pet
from app.schemas.schemas import PasseioCreate, PasseioResponse

router = APIRouter()


def _get_pet_ativo(pet_id: int, db: Session) -> Pet:
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.ativo == True).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet


@router.get("/pet/{pet_id}", response_model=List[PasseioResponse])
def listar_passeios(pet_id: int, db: Session = Depends(get_db)):
    _get_pet_ativo(pet_id, db)
    return db.query(Passeio).filter(Passeio.pet_id == pet_id).order_by(Passeio.data.desc()).all()


@router.post("/", response_model=PasseioResponse, status_code=status.HTTP_201_CREATED)
def registrar_passeio(passeio: PasseioCreate, db: Session = Depends(get_db)):
    _get_pet_ativo(passeio.pet_id, db)
    db_passeio = Passeio(**passeio.model_dump())
    db.add(db_passeio)
    db.commit()
    db.refresh(db_passeio)
    return db_passeio


@router.get("/sugestoes/{pet_id}")
def sugestoes_passeios(pet_id: int, db: Session = Depends(get_db)):
    pet = _get_pet_ativo(pet_id, db)

    porte = pet.raca.porte if pet.raca else "medio"

    sugestoes_por_porte = {
        "pequeno": [
            {"local": "Parque de bairro", "descricao": "Ótimo para pets pequenos, trilhas curtas e seguras"},
            {"local": "Pet-friendly café", "descricao": "Socialização em ambiente controlado"},
            {"local": "Shopping pet-friendly", "descricao": "Passeio indoor sem exposição ao calor"},
        ],
        "medio": [
            {"local": "Parque Estadual", "descricao": "Trilhas de dificuldade moderada"},
            {"local": "Praia de pets", "descricao": "Excelente para exercício e socialização"},
            {"local": "Parque urbano", "descricao": "Espaço para correr livremente"},
        ],
        "grande": [
            {"local": "Trilha na serra", "descricao": "Ideal para raças ativas e de grande porte"},
            {"local": "Parque com lago", "descricao": "Natação e exploração ao ar livre"},
            {"local": "Campo aberto", "descricao": "Espaço para correr sem restrições"},
        ],
    }

    return {
        "pet": pet.nome,
        "porte": porte,
        "sugestoes": sugestoes_por_porte.get(porte, sugestoes_por_porte["medio"]),
    }


@router.delete("/{passeio_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_passeio(passeio_id: int, db: Session = Depends(get_db)):
    p = db.query(Passeio).filter(Passeio.id == passeio_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Passeio não encontrado")
    db.delete(p)
    db.commit()

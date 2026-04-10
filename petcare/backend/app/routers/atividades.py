from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Atividade, Pet
from app.schemas.schemas import AtividadeCreate, AtividadeResponse

router = APIRouter()


def _get_pet_ativo(pet_id: int, db: Session) -> Pet:
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.ativo == True).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet


@router.get("/pet/{pet_id}", response_model=List[AtividadeResponse])
def listar_atividades(pet_id: int, db: Session = Depends(get_db)):
    _get_pet_ativo(pet_id, db)
    return db.query(Atividade).filter(Atividade.pet_id == pet_id).order_by(Atividade.data.desc()).all()


@router.post("/", response_model=AtividadeResponse, status_code=status.HTTP_201_CREATED)
def registrar_atividade(atividade: AtividadeCreate, db: Session = Depends(get_db)):
    _get_pet_ativo(atividade.pet_id, db)
    db_at = Atividade(**atividade.model_dump())
    db.add(db_at)
    db.commit()
    db.refresh(db_at)
    return db_at


@router.get("/sugestoes/{pet_id}")
def sugestoes_atividades(pet_id: int, db: Session = Depends(get_db)):
    """Retorna sugestões de atividades baseadas na raça e porte do pet"""
    pet = _get_pet_ativo(pet_id, db)

    sugestoes = {
        "alto": ["Corrida (30 min)", "Agility", "Natação", "Busca e resgate", "Ciclismo junto"],
        "medio": ["Caminhada (20 min)", "Brincadeira com bola", "Frisbee", "Trilha leve"],
        "baixo": ["Caminhada curta (10 min)", "Brincadeira indoor", "Esconde-esconde"],
    }

    nivel = pet.raca.nivel_atividade if pet.raca and pet.raca.nivel_atividade else "medio"
    return {
        "pet": pet.nome,
        "raca": pet.raca.nome if pet.raca else "N/A",
        "nivel_atividade": nivel,
        "sugestoes": sugestoes.get(nivel, sugestoes["medio"]),
    }


@router.delete("/{atividade_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_atividade(atividade_id: int, db: Session = Depends(get_db)):
    at = db.query(Atividade).filter(Atividade.id == atividade_id).first()
    if not at:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    db.delete(at)
    db.commit()

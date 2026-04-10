from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.models import Raca, EspecieEnum
from app.schemas.schemas import RacaCreate, RacaUpdate, RacaResponse

router = APIRouter()

@router.get("/", response_model=List[RacaResponse])
def listar_racas(especie: Optional[EspecieEnum] = None, db: Session = Depends(get_db)):
    q = db.query(Raca)
    if especie:
        q = q.filter(Raca.especie == especie)
    return q.all()

@router.post("/", response_model=RacaResponse, status_code=201)
def criar_raca(raca: RacaCreate, db: Session = Depends(get_db)):
    db_raca = Raca(**raca.model_dump())
    db.add(db_raca)
    db.commit()
    db.refresh(db_raca)
    return db_raca

@router.get("/{raca_id}", response_model=RacaResponse)
def buscar_raca(raca_id: int, db: Session = Depends(get_db)):
    raca = db.query(Raca).filter(Raca.id == raca_id).first()
    if not raca:
        raise HTTPException(status_code=404, detail="Raça não encontrada")
    return raca

@router.put("/{raca_id}", response_model=RacaResponse)
def atualizar_raca(raca_id: int, dados: RacaUpdate, db: Session = Depends(get_db)):
    raca = db.query(Raca).filter(Raca.id == raca_id).first()
    if not raca:
        raise HTTPException(status_code=404, detail="Raça não encontrada")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(raca, campo, valor)
    db.commit()
    db.refresh(raca)
    return raca

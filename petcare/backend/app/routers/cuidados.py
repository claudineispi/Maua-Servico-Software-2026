from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Cuidado, Raca
from app.schemas.schemas import CuidadoCreate, CuidadoResponse

router = APIRouter()

@router.get("/raca/{raca_id}", response_model=List[CuidadoResponse])
def listar_cuidados_raca(raca_id: int, categoria: str = None, db: Session = Depends(get_db)):
    q = db.query(Cuidado).filter(Cuidado.raca_id == raca_id)
    if categoria:
        q = q.filter(Cuidado.categoria == categoria)
    return q.all()

@router.post("/", response_model=CuidadoResponse, status_code=201)
def criar_cuidado(cuidado: CuidadoCreate, db: Session = Depends(get_db)):
    db_cuidado = Cuidado(**cuidado.model_dump())
    db.add(db_cuidado)
    db.commit()
    db.refresh(db_cuidado)
    return db_cuidado

@router.delete("/{cuidado_id}", status_code=204)
def deletar_cuidado(cuidado_id: int, db: Session = Depends(get_db)):
    c = db.query(Cuidado).filter(Cuidado.id == cuidado_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cuidado não encontrado")
    db.delete(c)
    db.commit()

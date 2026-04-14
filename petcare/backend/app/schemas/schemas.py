from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from app.models.models import EspecieEnum, PorteEnum, SexoEnum, StatusVacinaEnum


# ──────────────────────────────────────────────
# RAÇA
# ──────────────────────────────────────────────
class RacaBase(BaseModel):
    nome: str
    especie: EspecieEnum
    porte: PorteEnum
    expectativa_vida_anos: Optional[int] = None
    descricao: Optional[str] = None
    nivel_atividade: Optional[str] = None

class RacaCreate(RacaBase): pass

class RacaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    nivel_atividade: Optional[str] = None
    expectativa_vida_anos: Optional[int] = None

class RacaResponse(RacaBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# PET
# ──────────────────────────────────────────────
class PetBase(BaseModel):
    nome: str
    raca_id: int
    data_nascimento: date
    sexo: SexoEnum
    peso_kg: Optional[float] = None
    cor: Optional[str] = None
    microchip: Optional[str] = None
    foto_url: Optional[str] = None
    observacoes: Optional[str] = None

class PetCreate(PetBase): pass

class PetUpdate(BaseModel):
    nome: Optional[str] = None
    peso_kg: Optional[float] = None
    cor: Optional[str] = None
    foto_url: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None

class PetResponse(PetBase):
    id: int
    ativo: bool
    created_at: datetime
    raca: Optional[RacaResponse] = None
    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# VACINA
# ──────────────────────────────────────────────
class VacinaBase(BaseModel):
    pet_id: int
    nome: str
    data_aplicacao: date
    proxima_dose: Optional[date] = None
    veterinario: Optional[str] = None
    clinica: Optional[str] = None
    lote: Optional[str] = None
    status: StatusVacinaEnum = StatusVacinaEnum.aplicada
    observacoes: Optional[str] = None

class VacinaCreate(VacinaBase): pass

class VacinaUpdate(BaseModel):
    proxima_dose: Optional[date] = None
    status: Optional[StatusVacinaEnum] = None
    observacoes: Optional[str] = None

class VacinaResponse(VacinaBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# ATIVIDADE
# ──────────────────────────────────────────────
class AtividadeBase(BaseModel):
    pet_id: int
    tipo: str
    data: date
    duracao_minutos: Optional[int] = None
    distancia_km: Optional[float] = None
    intensidade: Optional[str] = None
    observacoes: Optional[str] = None

class AtividadeCreate(AtividadeBase): pass

class AtividadeResponse(AtividadeBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# PASSEIO
# ──────────────────────────────────────────────
class PasseioBase(BaseModel):
    pet_id: int
    local: str
    data: date
    duracao_minutos: Optional[int] = None
    avaliacao: Optional[int] = Field(None, ge=1, le=5)
    observacoes: Optional[str] = None

class PasseioCreate(PasseioBase): pass

class PasseioResponse(PasseioBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# CUIDADO
# ──────────────────────────────────────────────
class CuidadoBase(BaseModel):
    raca_id: int
    categoria: str
    titulo: str
    descricao: str
    frequencia: Optional[str] = None
    prioridade: str = "media"

class CuidadoCreate(CuidadoBase): pass

class CuidadoResponse(CuidadoBase):
    id: int
    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# RECOMENDACOES IA (motor baseado em regras)
# ──────────────────────────────────────────────
class RecomendacoesPayload(BaseModel):
    frequencia_semanal: str
    intensidade: str
    atividades_sugeridas: List[str]
    cuidados_prioritarios: List[str]
    alertas: List[str]


class RecomendacaoResponse(BaseModel):
    pet_id: int
    idade_anos: int
    idade_anos_detalhe: int
    idade_meses_detalhe: int
    perfil_ia: Optional[str] = None
    recomendacoes: RecomendacoesPayload


# ──────────────────────────────────────────────
# VACINA RECOMENDADA (cronograma)
# ──────────────────────────────────────────────
class VacinaRecomendadaResponse(BaseModel):
    id: int
    especie: EspecieEnum
    nome: str
    descricao: Optional[str] = None
    grupo: str
    dose: int
    idade_semanas: int
    obrigatoria: bool
    reforco_anual: bool
    class Config:
        from_attributes = True


class CronogramaItem(BaseModel):
    vacina_recomendada: VacinaRecomendadaResponse
    data_prevista: date
    status: str  # "pendente", "aplicada", "atrasada"
    vacina_aplicada_id: Optional[int] = None


# ──────────────────────────────────────────────
# DASHBOARD
# ──────────────────────────────────────────────
class DashboardPet(BaseModel):
    pet: PetResponse
    total_vacinas: int
    vacinas_pendentes: int
    total_atividades: int
    ultima_atividade: Optional[date]
    total_passeios: int

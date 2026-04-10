from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class EspecieEnum(str, enum.Enum):
    cao = "cao"
    gato = "gato"
    outro = "outro"


class PorteEnum(str, enum.Enum):
    pequeno = "pequeno"
    medio = "medio"
    grande = "grande"


class SexoEnum(str, enum.Enum):
    macho = "macho"
    femea = "femea"


class StatusVacinaEnum(str, enum.Enum):
    pendente = "pendente"
    aplicada = "aplicada"
    atrasada = "atrasada"


# ──────────────────────────────────────────────
# RAÇA
# ──────────────────────────────────────────────
class Raca(Base):
    __tablename__ = "racas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    especie = Column(Enum(EspecieEnum), nullable=False)
    porte = Column(Enum(PorteEnum), nullable=False)
    expectativa_vida_anos = Column(Integer)
    descricao = Column(Text)
    nivel_atividade = Column(String(50))  # baixo, médio, alto
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pets = relationship("Pet", back_populates="raca")
    cuidados = relationship("Cuidado", back_populates="raca")
    vacinas_recomendadas = relationship("VacinaRecomendada", back_populates="raca")


# ──────────────────────────────────────────────
# PET
# ──────────────────────────────────────────────
class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    raca_id = Column(Integer, ForeignKey("racas.id"), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(Enum(SexoEnum), nullable=False)
    peso_kg = Column(Float)
    cor = Column(String(50))
    microchip = Column(String(50), unique=True)
    foto_url = Column(String(255))
    observacoes = Column(Text)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    raca = relationship("Raca", back_populates="pets")
    vacinas = relationship("Vacina", back_populates="pet")
    atividades = relationship("Atividade", back_populates="pet")
    passeios = relationship("Passeio", back_populates="pet")


# ──────────────────────────────────────────────
# VACINA RECOMENDADA (por raça/espécie)
# ──────────────────────────────────────────────
class VacinaRecomendada(Base):
    __tablename__ = "vacinas_recomendadas"

    id = Column(Integer, primary_key=True, index=True)
    especie = Column(Enum(EspecieEnum), nullable=False)
    nome = Column(String(150), nullable=False)
    descricao = Column(Text)
    grupo = Column(String(100), nullable=False)     # ex: "V10", "Antirrábica"
    dose = Column(Integer, nullable=False)           # 1, 2, 3...
    idade_semanas = Column(Integer, nullable=False)  # idade recomendada em semanas
    obrigatoria = Column(Boolean, default=True)
    reforco_anual = Column(Boolean, default=False)

    raca_id = Column(Integer, ForeignKey("racas.id"), nullable=True)
    raca = relationship("Raca", back_populates="vacinas_recomendadas")


# ──────────────────────────────────────────────
# VACINA APLICADA
# ──────────────────────────────────────────────
class Vacina(Base):
    __tablename__ = "vacinas"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    nome = Column(String(150), nullable=False)
    data_aplicacao = Column(Date, nullable=False)
    proxima_dose = Column(Date)
    veterinario = Column(String(150))
    clinica = Column(String(150))
    lote = Column(String(50))
    status = Column(Enum(StatusVacinaEnum), default=StatusVacinaEnum.aplicada)
    observacoes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pet = relationship("Pet", back_populates="vacinas")


# ──────────────────────────────────────────────
# ATIVIDADE
# ──────────────────────────────────────────────
class Atividade(Base):
    __tablename__ = "atividades"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    tipo = Column(String(100), nullable=False)  # caminhada, natação, brincadeira...
    data = Column(Date, nullable=False)
    duracao_minutos = Column(Integer)
    distancia_km = Column(Float)
    intensidade = Column(String(50))  # leve, moderada, intensa
    observacoes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pet = relationship("Pet", back_populates="atividades")


# ──────────────────────────────────────────────
# PASSEIO
# ──────────────────────────────────────────────
class Passeio(Base):
    __tablename__ = "passeios"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    local = Column(String(200), nullable=False)
    data = Column(Date, nullable=False)
    duracao_minutos = Column(Integer)
    avaliacao = Column(Integer)  # 1-5 estrelas
    fotos_url = Column(Text)
    observacoes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pet = relationship("Pet", back_populates="passeios")


# ──────────────────────────────────────────────
# CUIDADOS POR RAÇA
# ──────────────────────────────────────────────
class Cuidado(Base):
    __tablename__ = "cuidados"

    id = Column(Integer, primary_key=True, index=True)
    raca_id = Column(Integer, ForeignKey("racas.id"), nullable=False)
    categoria = Column(String(100), nullable=False)  # alimentação, higiene, saúde...
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    frequencia = Column(String(100))  # diário, semanal, mensal
    prioridade = Column(String(20), default="media")  # alta, media, baixa

    raca = relationship("Raca", back_populates="cuidados")

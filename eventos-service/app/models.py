# app/models.py
from sqlalchemy import Column, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    deporte = Column(String(100), nullable=False)
    fecha = Column(DateTime(timezone=True), nullable=False)
    estado = Column(String(20), nullable=False, default="programado")
    equipo_local = Column(String(255))
    equipo_visitante = Column(String(255))
    cuota_local = Column(Numeric(5, 2))
    cuota_empate = Column(Numeric(5, 2))
    cuota_visitante = Column(Numeric(5, 2))
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

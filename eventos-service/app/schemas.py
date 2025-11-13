# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class EventoBase(BaseModel):
    nombre: str
    deporte: str
    fecha: datetime
    estado: Optional[str] = "programado"
    equipo_local: Optional[str] = None
    equipo_visitante: Optional[str] = None
    cuota_local: Optional[float] = None
    cuota_empate: Optional[float] = None
    cuota_visitante: Optional[float] = None

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    deporte: Optional[str] = None
    fecha: Optional[datetime] = None
    estado: Optional[str] = None
    equipo_local: Optional[str] = None
    equipo_visitante: Optional[str] = None
    cuota_local: Optional[float] = None
    cuota_empate: Optional[float] = None
    cuota_visitante: Optional[float] = None

class Evento(EventoBase):
    id: UUID
    creado_en: datetime

    class Config:
        orm_mode = True

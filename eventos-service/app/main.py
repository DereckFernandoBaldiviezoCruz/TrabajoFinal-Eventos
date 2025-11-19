# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import threading

from . import models, schemas
from .database import engine, Base, get_db
from .auth import get_current_user
from .grpc_server import serve_grpc

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API del Microservicio de Eventos (CasiGano)",
    version="1.0",
    description="Maneja todas las operaciones sobre eventos deportivos.",
    openapi_tags=[
        {"name": "eventos", "description": "Operaciones sobre eventos deportivos"},
        {"name": "health", "description": "Estado del servicio"},
    ],
)

API_PREFIX = "/api/v1"


# Lanzar servidor gRPC en un hilo aparte cuando arranque la app
def start_grpc_server():
    # Ejecuta el servidor gRPC (bloqueante) en un hilo daemon
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    grpc_thread.start()


@app.on_event("startup")
def startup_event():
    # Este evento se ejecuta cuando FastAPI arranca
    start_grpc_server()


@app.get(f"{API_PREFIX}/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@app.post(
    f"{API_PREFIX}/eventos",
    response_model=schemas.Evento,
    status_code=status.HTTP_201_CREATED,
    tags=["eventos"],
    summary="Crea un nuevo evento",
    description="Crea un evento deportivo para que otros microservicios puedan usarlo (apuestas, frontend, etc.).",
)
def crear_evento(
    evento: schemas.EventoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    db_evento = models.Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento


@app.get(
    f"{API_PREFIX}/eventos",
    response_model=List[schemas.Evento],
    tags=["eventos"],
    summary="Lista todos los eventos",
)
def listar_eventos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return db.query(models.Evento).all()


@app.get(
    f"{API_PREFIX}/eventos/{{evento_id}}",
    response_model=schemas.Evento,
    tags=["eventos"],
    summary="Obtiene un evento por ID",
)
def obtener_evento(
    evento_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )
    return evento


@app.put(
    f"{API_PREFIX}/eventos/{{evento_id}}",
    response_model=schemas.Evento,
    tags=["eventos"],
    summary="Actualiza un evento existente",
)
def actualizar_evento(
    evento_id: UUID,
    evento_update: schemas.EventoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )

    for field, value in evento_update.dict(exclude_unset=True).items():
        setattr(evento, field, value)

    db.commit()
    db.refresh(evento)
    return evento


@app.delete(
    f"{API_PREFIX}/eventos/{{evento_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["eventos"],
    summary="Elimina un evento",
)
def eliminar_evento(
    evento_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )
    db.delete(evento)
    db.commit()
    return

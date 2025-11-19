# app/grpc_server.py
from concurrent import futures
import grpc
from uuid import UUID

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Evento
import eventos_pb2
import eventos_pb2_grpc


class EventoServiceServicer(eventos_pb2_grpc.EventoServiceServicer):
    """
    Implementación del servicio gRPC definido en eventos.proto
    """

    def __init__(self):
        # Usaremos SessionLocal de SQLAlchemy para acceder a la BD
        self.SessionLocal = SessionLocal

    def GetEvento(self, request, context):
        """
        Implementación de rpc GetEvento(GetEventoRequest) returns (EventoResponse)
        """
        db: Session = self.SessionLocal()
        try:
            try:
                evento_id = UUID(request.id)
            except ValueError:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID de evento inválido (no es un UUID).")
                return eventos_pb2.EventoResponse()

            evento: Evento = db.query(Evento).filter(Evento.id == evento_id).first()

            if not evento:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Evento no encontrado.")
                return eventos_pb2.EventoResponse()

            return eventos_pb2.EventoResponse(
                id=str(evento.id),
                nombre=evento.nombre,
                deporte=evento.deporte,
                fecha=evento.fecha.isoformat() if evento.fecha else "",
                estado=evento.estado,
                equipo_local=evento.equipo_local or "",
                equipo_visitante=evento.equipo_visitante or "",
                cuota_local=float(evento.cuota_local) if evento.cuota_local is not None else 0.0,
                cuota_empate=float(evento.cuota_empate) if evento.cuota_empate is not None else 0.0,
                cuota_visitante=float(evento.cuota_visitante) if evento.cuota_visitante is not None else 0.0,
            )
        finally:
            db.close()

    def ListEventos(self, request, context):
        """
        Implementación de rpc ListEventos(ListEventosRequest) returns (ListEventosResponse)
        Devuelve todos los eventos (se podría filtrar por estado en el futuro).
        """
        db: Session = self.SessionLocal()
        try:
            eventos = db.query(Evento).all()
            eventos_respuesta = []

            for ev in eventos:
                eventos_respuesta.append(
                    eventos_pb2.EventoResponse(
                        id=str(ev.id),
                        nombre=ev.nombre,
                        deporte=ev.deporte,
                        fecha=ev.fecha.isoformat() if ev.fecha else "",
                        estado=ev.estado,
                        equipo_local=ev.equipo_local or "",
                        equipo_visitante=ev.equipo_visitante or "",
                        cuota_local=float(ev.cuota_local) if ev.cuota_local is not None else 0.0,
                        cuota_empate=float(ev.cuota_empate) if ev.cuota_empate is not None else 0.0,
                        cuota_visitante=float(ev.cuota_visitante) if ev.cuota_visitante is not None else 0.0,
                    )
                )

            return eventos_pb2.ListEventosResponse(eventos=eventos_respuesta)
        finally:
            db.close()


def serve_grpc():
    """
    Arranca el servidor gRPC en el puerto 50051
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    eventos_pb2_grpc.add_EventoServiceServicer_to_server(
        EventoServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Servidor gRPC de Eventos escuchando en el puerto 50051...")
    server.wait_for_termination()

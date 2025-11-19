FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema necesarias para psycopg2 y compilación
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la app y los .proto
COPY app ./app
COPY proto ./proto

# Generar código gRPC a partir del .proto
# Salida: /app/eventos_pb2.py y /app/eventos_pb2_grpc.py (módulos top-level)
RUN python -m grpc_tools.protoc \
    -I./proto \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/eventos.proto

ENV PYTHONUNBUFFERED=1

# Variables de entorno por defecto (sobrescribibles desde docker-compose)
ENV DB_HOST=db_eventos
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=casigano_eventos_db
ENV JWT_SECRET=supersecret
ENV JWT_ALGORITHM=HS256

# FastAPI (HTTP) y gRPC
EXPOSE 8000
EXPOSE 50051

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

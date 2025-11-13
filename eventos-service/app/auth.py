# app/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Este objeto registra el esquema "http" bearer en OpenAPI
bearer_scheme = HTTPBearer(auto_error=True)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """
    Dependencia que obtiene y valida el token JWT usando el esquema HTTP Bearer.
    Esto hace que FastAPI agregue el botón 'Authorize' en Swagger.
    """
    token = credentials.credentials  # El JWT que viene después de 'Bearer '
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # Aquí podrías validar el rol si quieres:
        # if payload.get("role") != "admin":
        #     raise HTTPException(status_code=403, detail="No autorizado")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

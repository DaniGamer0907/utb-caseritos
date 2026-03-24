from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import get_db
from models.Usuario import Usuario
from auth.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    email = payload.get("sub")
    role = payload.get("role")

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"user": usuario, "role": role}


def solo_admin(current=Depends(get_current_user)):
    if current["role"] != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores")
    return current["user"]


def solo_cliente(current=Depends(get_current_user)):
    if current["role"] != "cliente":
        raise HTTPException(status_code=403, detail="Solo clientes")
    return current["user"]
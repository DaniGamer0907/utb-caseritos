from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Usuario import Usuario
from schemas.Usuario_schemas import UsuarioC
from schemas.schemas import token,loginRequest
from auth.hashing import verify_password, hash_password
from auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=token)
def login(data: loginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()
    
    if not usuario or not verify_password(data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    role = "admin" if usuario.rol_id == 1 else "cliente"
    token = create_access_token(user=usuario.email, role=role)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": role
    }

@router.post("/registro")
def registro(user: UsuarioC, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == user.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nuevo = Usuario(
        nombre=user.name,
        lastname=user.lastname,
        address=user.address,
        phone=user.phone,
        email=user.email,
        password=hash_password(user.password),
        rol_id=2  
    )
    db.add(nuevo)
    db.commit()
    return {"message": "Usuario registrado correctamente"}
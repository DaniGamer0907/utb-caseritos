from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Usuario import Usuario
from schemas.Usuario_schemas import UsuarioC
from auth.dependencies import require_admin

router = APIRouter(prefix="/usuario", tags=["Usuarios"])


@router.post("/addUsuario", dependencies=[Depends(require_admin)])
def agregar_usuario(usuario: UsuarioC, db: Session = Depends(get_db)):
    usuariodb = Usuario(
        nombre=usuario.name,
        lastname=usuario.lastname,
        address=usuario.address,
        phone=usuario.phone,
        email=usuario.email,
        password=usuario.password
    )
    db.add(usuariodb)
    db.commit()
    return {"message": "Usuario agregado correctamente!", "client": usuario}


@router.get("/listUsuarios", dependencies=[Depends(require_admin)])
def obtener_usuarios(db: Session = Depends(get_db)):
    get = db.query(Usuario).all()
    if not get:
        raise HTTPException(status_code=404, detail="Usuarios no encontrados")
    else:
        return get


@router.get("/getUsuario", dependencies=[Depends(require_admin)])
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    get = db.query(Usuario).filter(Usuario.id == id).first()
    if not get:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        return get


@router.put("/actualizarUsuario", dependencies=[Depends(require_admin)])
def actualizar_usuario(id: int, usuario_update: UsuarioC, db: Session = Depends(get_db)):
    dbusuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not dbusuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        dbusuario.address = usuario_update.address
        dbusuario.phone = usuario_update.phone
        dbusuario.password = usuario_update.password
        db.commit()
        return "Se ha actualizado los datos del usuario correctamente"


@router.delete("/deleteUsuario", dependencies=[Depends(require_admin)])
def borrar_usuario(id: int, db: Session = Depends(get_db)):
    dbusuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not dbusuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        db.delete(dbusuario)
        db.commit()
        return "Se ha borrado existosamente"

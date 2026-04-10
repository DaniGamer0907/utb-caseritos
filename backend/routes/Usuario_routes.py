from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Usuario import Usuario
from schemas.Usuario_schemas import UsuarioC
from auth.dependencies import get_current_user

router= APIRouter(prefix="/usuario", tags= ["Usuarios"])


@router.post("/addUsuario")
def agregar_usuario(usuario: UsuarioC, db: Session = Depends(get_db)):
    usuariodb = Usuario(nombre = usuario.name, lastname = usuario.lastname, address=usuario.address, phone=usuario.phone, email=usuario.email, password = usuario.password)
    db.add(usuariodb)
    db.commit()
    return {"message": "Usuario agregado correctamente!", "client": usuario}

@router.get("/listUsuarios")
def obtener_Usuarios(db: Session = Depends(get_db)):
    get = db.query(Usuario).all()
    if not get:
        raise HTTPException(status_code=404, detail="Usuarios no encontrados")
    else:
        return get

@router.get("/getUsuario")
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    get = db.query(Usuario).filter(Usuario.id==id).first()
    if not get:
         raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        return get

@router.put("/actualizarUsuario")
def actualizar_usuario(id: int, usuario_update: UsuarioC, db: Session = Depends(get_db)):
    dbusuario = db.query(Usuario).filter(Usuario.id==id).first()
    if not dbusuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        dbusuario.address = usuario_update.address 
        dbusuario.phone = usuario_update.phone 
        dbusuario.password = usuario_update.password
        db.commit()
        return "Se ha actualizado los datos del usuario correctamente"

@router.delete("/deleteUsuario")
def borrar_usuario(id: int , db: Session = Depends(get_db),user: str = Depends(get_current_user)):
    if user == "admin":
        dbusuario = db.query(Usuario).filter(Usuario.id==id).first()
        if not dbusuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        else:
            db.delete(dbusuario)
            db.commit()
            return "Se ha borrado existosamente"
    elif (user == "cliente"): 
        return "ERES UN CLIENTE"
    else:
        return user




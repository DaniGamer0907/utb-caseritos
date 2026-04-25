from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Proteina import Proteina
from schemas.Proteina_schemas import ProteinaC
from auth.dependencies import require_admin

router = APIRouter(prefix="/proteina", tags=["Proteinas"])


@router.post("/crearProteina", dependencies=[Depends(require_admin)])
def crear_proteina(proteinas: ProteinaC, db: Session = Depends(get_db)):
    proteina = Proteina(nombre=proteinas.nombre, avaliable=proteinas.avaliable)
    db.add(proteina)
    db.commit()
    return {"mensaje": "proteina agregado correctamente"}


@router.get("/listProteinas")
def obtener_lista_proteinas(db: Session = Depends(get_db)):
    get = db.query(Proteina).all()
    if not get:
        raise HTTPException(status_code=404, detail="Proteinas no encontradas")
    else:
        return get


@router.get("/getProteina")
def obtener_proteina(id: int, db: Session = Depends(get_db)):
    get = db.query(Proteina).filter(Proteina.id == id).first()
    if not get:
        raise HTTPException(status_code=404, detail="Proteina no encontrada")
    else:
        return get


@router.put("/actualizarProteina", dependencies=[Depends(require_admin)])
def actualizar_proteina(id: int, nueva_proteina: ProteinaC, db: Session = Depends(get_db)):
    get = db.query(Proteina).filter(Proteina.id == id).first()
    if not get:
        raise HTTPException(status_code=404, detail="Proteina no encontrada")
    else:
        get.nombre = nueva_proteina.nombre #type: ignore
        get.avaliable = nueva_proteina.avaliable #type: ignore
        db.commit()
        return {"mensaje": "proteina actualizada correctamente", "proteina": nueva_proteina}


@router.delete("/borrarProteina", dependencies=[Depends(require_admin)])
def eliminar_proteina(id: int, db: Session = Depends(get_db)):
    get = db.query(Proteina).filter(Proteina.id == id).first()
    if not get:
        raise HTTPException(status_code=404, detail="Proteina no encontrada")
    else:
        db.delete(get)
        db.commit()
        return {"mensaje": "proteina eliminada correctamente"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Almuerzo import Almuerzo
from schemas.Almuerzo_schemas import AlmuerzoC
from auth.dependencies import require_admin

router = APIRouter(prefix="/almuerzo", tags=["Almuerzos"])


@router.post("/crearAlmuerzo", dependencies=[Depends(require_admin)])
def crear_almuerzo(almuerzo: AlmuerzoC, db: Session = Depends(get_db)):
    almuerzodb = Almuerzo(descripcion=almuerzo.descripcion, fecha=almuerzo.fecha)
    db.add(almuerzodb)
    db.commit()
    return {"mensaje": "Almuerzo agregado correctamente"}


@router.get("/listAlmuerzos")
def obtener_almuerzos(db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).all()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzos no encontrados")
    else:
        return almuerzos


@router.get("/getAlmuerzo")
def obtener_almuerzo(id: int, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id == id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        return almuerzos


@router.put("/actualizarAlmuerzo", dependencies=[Depends(require_admin)])
def actualizar_almuerzo(id: int, nuevo_almuerzo: AlmuerzoC, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id == id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        almuerzos.descripcion = nuevo_almuerzo.descripcion  # type: ignore
        almuerzos.fecha = nuevo_almuerzo.fecha  # type: ignore
        db.commit()
        return {"mensaje": "Almuerzo actualizado correctamente"}


@router.delete("/borrarAlmuerzo", dependencies=[Depends(require_admin)])
def eliminar_almuerzo(id: int, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id == id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        db.delete(almuerzos)
        db.commit()
        return {"mensaje": "Almuerzo eliminado correctamente"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Almuerzo import Almuerzo
from schemas.Almuerzo_schemas import AlmuerzoC

router= APIRouter(prefix="/Almuerzo", tags= ["Almuerzo"])

@router.post("/crearAlmuerzo")
def crear_almuerzo(almuerzo: AlmuerzoC, db: Session = Depends(get_db)):
    almuerzodb = Almuerzo(descripcion=almuerzo.descripcion, fecha=almuerzo.fecha)
    db.add(almuerzodb)
    db.commit()
    return {"mensaje": "Almuerzo agregado correctamente"}

@router.get("/Almuerzo")
def obtener_almuerzo(db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).all()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzos no encontrados")
    else:
        return almuerzos

@router.get("/AlmuerzoID")
def obtener_almuerzo_id(id: int, db: Session=Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        return almuerzos
    
@router.put("/AlmuerzoID")
def actualizar_almuerzo(id: int, nuevo_almuerzo: AlmuerzoC, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        almuerzos.descripcion=nuevo_almuerzo.descripcion
        almuerzos.fecha=nuevo_almuerzo.fecha
        db.commit()
        return {"mensaje": "Almuerzo actualizado correctamente"}
    

@router.delete("/AlmuerzoID")
def eliminar_almuerzo(id: int, db: Session = Depends(get_db)):
    almuerzos = db.query(Almuerzo).filter(Almuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        db.delete(almuerzos)
        db.commit()
        return {"mensaje": "Almuerzo eliminado correctamente"}


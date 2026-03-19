from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.TipoAlmuerzo import TipoAlmuerzo
from schemas.TipoAlmuerzo_schemas import TipoAlmuerzoC

router= APIRouter(prefix="/crearTipoAlmuerzo", tags=["TipoAlmuerzo"])

@router.post("/crearTipoAlmuerzo")
def crear_tipo_almuerzo(tipo_almuerzo: TipoAlmuerzoC, db: Session = Depends(get_db)):
    almuerzodb = TipoAlmuerzo(nombre=tipo_almuerzo.nombre, precio=tipo_almuerzo.precio )
    db.add(almuerzodb)
    db.commit()
    return {"mensaje": "Tipo de almuerzo agregado correctamente"}

@router.get("/tipoAlmuerzo")
def obtener_tipo_almuerzo(db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).all()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzos no encontrados")
    else:
        return almuerzos

@router.get("/tipoAlmuerzoID")
def obtener_tipo_almuerzo_id(id: int, db: Session=Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        return almuerzos
    
@router.put("/tipoAlmuerzoID")
def actualizar_tipo_almuerzo(id: int, nuevo_tipo_almuerzo: TipoAlmuerzoC, db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        almuerzos.nombre = nuevo_tipo_almuerzo.nombre
        almuerzos.precio = nuevo_tipo_almuerzo.precio
        db.commit()
        return {"mensaje": "Tipo de almuerzo actualizado correctamente"}
    

@router.delete("/tipoAlmuerzoID")
def eliminar_tipo_almuerzo(id: int, db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        db.delete(almuerzos)
        db.commit()
        return {"mensaje": "Tipo de almuerzo eliminado correctamente"}


    
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.TipoAlmuerzo import TipoAlmuerzo
from schemas.TipoAlmuerzo_schemas import TipoAlmuerzoC

router= APIRouter(prefix="/tipoalmuerzo", tags=["Tipo de Almuerzos"])

@router.post("/crearTipoAlmuerzo")
def crear_tipo_de_almuerzo(tipo_almuerzo: TipoAlmuerzoC, db: Session = Depends(get_db)):
    almuerzodb = TipoAlmuerzo(nombre=tipo_almuerzo.nombre, precio=tipo_almuerzo.precio )
    db.add(almuerzodb)
    db.commit()
    return {"mensaje": "Tipo de almuerzo agregado correctamente"}

@router.get("/listTiposAlmuerzo")
def obtener_lista_tipos_de_almuerzo(db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).all()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzos no encontrados")
    else:
        return almuerzos

@router.get("/getTipoAlmuerzo")
def obtener_tipo_de_almuerzo(id: int, db: Session=Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        return almuerzos
    
@router.put("/actualizarTipoAlmuerzo")
def actualizar_tipo_de_almuerzo(id: int, nuevo_tipo_almuerzo: TipoAlmuerzoC, db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        almuerzos.nombre = nuevo_tipo_almuerzo.nombre #type: ignore
        almuerzos.precio = nuevo_tipo_almuerzo.precio #type: ignore
        db.commit()
        return {"mensaje": "Tipo de almuerzo actualizado correctamente"}
    

@router.delete("/borrarTipoAlmuerzo")
def eliminar_tipo_de_almuerzo(id: int, db: Session = Depends(get_db)):
    almuerzos = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id==id).first()
    if not almuerzos:
        raise HTTPException(status_code=404, detail="Almuerzo no encontrado")
    else:
        db.delete(almuerzos)
        db.commit()
        return {"mensaje": "Tipo de almuerzo eliminado correctamente"}


    
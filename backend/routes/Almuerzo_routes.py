from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Almuerzo import Almuerzo
from schemas.Almuerzo_schemas import AlmuerzoC
from auth.dependencies import require_admin
from datetime import datetime

router = APIRouter(prefix="/almuerzo", tags=["Almuerzos"])


@router.post("/crearAlmuerzo", dependencies=[Depends(require_admin)])
def crear_almuerzo(almuerzo: AlmuerzoC, db: Session = Depends(get_db)):
    almuerzodb = Almuerzo(
        proteinaid=almuerzo.proteinaid,
        tipalmuerzo=almuerzo.tipalmuerzo,
        fecha=almuerzo.fecha or datetime.utcnow()
    )
    db.add(almuerzodb)
    db.commit()
    db.refresh(almuerzodb)
    return {"mensaje": "Almuerzo agregado correctamente", "id": almuerzodb.id}


@router.get("/getOrCreateAlmuerzo")
def get_or_create_almuerzo(proteinaid: int, tipalmuerzo: int, db: Session = Depends(get_db)):
    # Busca uno existente para hoy con esa proteina y tipo
    hoy = datetime.utcnow().date()
    almuerzodb = db.query(Almuerzo).filter(
        Almuerzo.proteinaid == proteinaid,
        Almuerzo.tipalmuerzo == tipalmuerzo
    ).first()

    if not almuerzodb:
        almuerzodb = Almuerzo(
            proteinaid=proteinaid,
            tipalmuerzo=tipalmuerzo,
            fecha=datetime.utcnow()
        )
        db.add(almuerzodb)
        db.commit()
        db.refresh(almuerzodb)
    
    return almuerzodb


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
        almuerzos.proteinaid = nuevo_almuerzo.proteinaid  # type: ignore
        almuerzos.tipalmuerzo = nuevo_almuerzo.tipalmuerzo  # type: ignore
        if nuevo_almuerzo.fecha:
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

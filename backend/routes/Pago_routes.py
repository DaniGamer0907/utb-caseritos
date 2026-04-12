from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Pago import Pago
from schemas.Pago_schemas import PagoC
from auth.dependencies import solo_admin, solo_cliente

router= APIRouter(prefix="/Pago", tags= ["Pagos"])  

@router.post("/crearPago")
def crear_pago(pago: PagoC, db: Session = Depends(get_db)):
    pagodb = Pago(metodopago=pago.metodopago, diadelpago=pago.diadelpago )
    db.add(pagodb)
    db.commit()
    return {"mensaje": "Pago agregado correctamente"}

@router.get("/listPagos")
def obtener_pagos(db: Session = Depends(get_db)):
    pagos = db.query(Pago).all()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pagos no encontrados")
    else:
        return pagos

@router.get("/getPago")
def obtener_pago(id: int, db: Session=Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        return pagos
    
@router.put("/actualizarPago")
def actualizar_pago(id: int, nuevo_pago: PagoC, db: Session = Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        pagos.metodopago = nuevo_pago.metodopago #type: ignore
        pagos.diadelpago = nuevo_pago.diadelpago #type: ignore
        db.commit()
        return {"mensaje": "Pago actualizado correctamente"}
    

@router.delete("/borrarPago")
def eliminar_pago(id: int, db: Session = Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        db.delete(pagos)
        db.commit()
        return {"mensaje": "Pago eliminado correctamente"}

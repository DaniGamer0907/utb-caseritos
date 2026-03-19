from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Pago import Pago
from schemas.Pago_schemas import PagoC

router= APIRouter(prefix="/Pago", tags= ["Pago"])  

@router.post("/crearPago")
def crear_pago(pago: PagoC, db: Session = Depends(get_db)):
    pagodb = Pago(metodopago=pago.metodopago, diadelpago=pago.diadelpago )
    db.add(pagodb)
    db.commit()
    return {"mensaje": "Pago agregado correctamente"}

@router.get("/Pago")
def obtener_pago(db: Session = Depends(get_db)):
    pagos = db.query(Pago).all()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pagos no encontrados")
    else:
        return pagos

@router.get("/PagoID")
def obtener_pago_id(id: int, db: Session=Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        return pagos
    
@router.put("/PagoID")
def actualizar_pago(id: int, nuevo_pago: PagoC, db: Session = Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        pagos.metodopago = nuevo_pago.metodopago
        pagos.diadelpago = nuevo_pago.diadelpago
        db.commit()
        return {"mensaje": "Pago actualizado correctamente"}
    

@router.delete("/PagoID")
def eliminar_pago(id: int, db: Session = Depends(get_db)):
    pagos = db.query(Pago).filter(Pago.id==id).first()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        db.delete(pagos)
        db.commit()
        return {"mensaje": "Pago eliminado correctamente"}

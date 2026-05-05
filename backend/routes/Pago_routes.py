from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Pago import Pago
from models.Pedido import Pedido
from schemas.Pago_schemas import PagoC
from auth.dependencies import get_current_user, require_admin, require_cliente

router = APIRouter(prefix="/Pago", tags=["Pagos"])


def _obtener_pago_visible(db: Session, pago_id: int, current_user: dict) -> Pago | None:
    query = db.query(Pago).filter(Pago.id == pago_id)
    if current_user["role"] != "admin":
        query = query.join(Pedido, Pedido.pago_id == Pago.id).filter(Pedido.usuario_id == current_user["user"].id)
    return query.first()


@router.post("/crearPago", dependencies=[Depends(require_admin)])
def crear_pago(pago: PagoC, db: Session = Depends(get_db)):
    if pago.monto <= 0:
        raise HTTPException(status_code=400, detail="El monto del pago debe ser mayor que 0")
    pagodb = Pago(
        metodopago=pago.metodopago, 
        diadelpago=pago.diadelpago,
        monto=pago.monto,
        referencia=pago.referencia
    )
    db.add(pagodb)
    db.commit()
    db.refresh(pagodb)
    return {"mensaje": "Pago agregado correctamente", "id": pagodb.id}


@router.get("/listPagos", dependencies=[Depends(require_cliente)])
def obtener_pagos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(Pago)
    if current_user["role"] != "admin":
        query = query.join(Pedido, Pedido.pago_id == Pago.id).filter(Pedido.usuario_id == current_user["user"].id)
    pagos = query.all()
    if not pagos:
        raise HTTPException(status_code=404, detail="Pagos no encontrados")
    else:
        return pagos


@router.get("/getPago", dependencies=[Depends(require_cliente)])
def obtener_pago(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pagos = _obtener_pago_visible(db, id, current_user)
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        return pagos


@router.put("/actualizarPago", dependencies=[Depends(require_cliente)])
def actualizar_pago(
    id: int,
    nuevo_pago: PagoC,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pagos = _obtener_pago_visible(db, id, current_user)
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        pagos.metodopago = nuevo_pago.metodopago  # type: ignore
        pagos.diadelpago = nuevo_pago.diadelpago  # type: ignore
        pagos.monto = nuevo_pago.monto # type: ignore
        pagos.referencia = nuevo_pago.referencia # type: ignore
        db.commit()
        return {"mensaje": "Pago actualizado correctamente"}

@router.patch("/actualizarEstado", dependencies=[Depends(require_admin)])
def actualizar_estado_pago(
    id: int,
    estado: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pago = _obtener_pago_visible(db, id, current_user)

    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    pago.estado = estado  
    db.commit()

    return {"mensaje": "Estado actualizado correctamente"}

@router.delete("/borrarPago", dependencies=[Depends(require_cliente)])
def eliminar_pago(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pagos = _obtener_pago_visible(db, id, current_user)
    if not pagos:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    else:
        db.delete(pagos)
        db.commit()
        return {"mensaje": "Pago eliminado correctamente"}

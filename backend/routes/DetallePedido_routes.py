from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.DetallePedido import DetallePedido
from schemas.DetallePedido_schemas import DetallePedidoC

router= APIRouter(prefix="/Detallepedido", tags= ["DetallePedido"])

@router.post("/crearDetallePedidos")
def crear_detalle_pedido(detalle_pedido: DetallePedidoC, db: Session = Depends(get_db)):
    pedidodb = DetallePedido(cantidad=detalle_pedido.cantidad, precio_unitario=detalle_pedido.precio_unitario, total=detalle_pedido.total )
    db.add(pedidodb)
    db.commit()
    return {"mensaje": "Detalle de Pedido agregado correctamente"}

@router.get("/DetallePedidos")
def obtener_detalle_pedido(db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedido).all()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedidos no encontrados")
    else:
        return pedidos

@router.get("/DetallePedidosID")
def obtener_detalle_pedido_id(id: int, db: Session=Depends(get_db)):
    pedidos = db.query(DetallePedido).filter(DetallePedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        return pedidos
    
@router.put("/DetallePedidosID")
def actualizar_detalle_pedido(id: int, nuevo_detalle_pedido: DetallePedidoC, db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedido).filter(DetallePedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        pedidos.cantidad = nuevo_detalle_pedido.cantidad
        pedidos.precio_unitario = nuevo_detalle_pedido.precio_unitario
        pedidos.total = nuevo_detalle_pedido.total
        db.commit()
        return {"mensaje": "Detalle de Pedido actualizado correctamente"}
    

@router.delete("/DetallePedidosID")
def eliminar_detalle_pedido(id: int, db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedido).filter(DetallePedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        db.delete(pedidos)
        db.commit()
        return {"mensaje": "Detalle de Pedido eliminado correctamente"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.DetallePedido import DetallePedido
from schemas.DetallePedido_schemas import DetallePedidoC

router= APIRouter(prefix="/detallesPedido", tags= ["Detalles de Pedidos"])

@router.post("/crearDetallesPedido")
def crear_detalle_de_pedido(detalle_pedido: DetallePedidoC, db: Session = Depends(get_db)):
    pedidodb = DetallePedido(cantidad=detalle_pedido.cantidad, precio_unitario=detalle_pedido.precio_unitario, total=detalle_pedido.total )
    db.add(pedidodb)
    db.commit()
    return {"mensaje": "Detalle de Pedido agregado correctamente"}

@router.get("/listDetallesPedidos")
def obtener_detalles_de_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedido).all()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedidos no encontrados")
    else:
        return pedidos

@router.get("/getDetallesPedido")
def obtener_detalle_de_pedido(id: int, db: Session=Depends(get_db)):
    pedidos = db.query(DetallePedido).filter(DetallePedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        return pedidos
    
@router.put("/actualizarDetallesPedido")
def actualizar_detalle_de_pedido(id: int, nuevo_detalle_pedido: DetallePedidoC, db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedido).filter(DetallePedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        pedidos.cantidad = nuevo_detalle_pedido.cantidad #type: ignore
        pedidos.precio_unitario = nuevo_detalle_pedido.precio_unitario #type: ignore
        pedidos.total = nuevo_detalle_pedido.total #type: ignore
        db.commit()
        return {"mensaje": "Detalle de Pedido actualizado correctamente"}
    

@router.delete("/borrarDetallesPedido")
def eliminar_detalle_de_pedido(id: int, db: Session = Depends(get_db)):
    pedidos = db.query(DetallePedido).filter(DetallePedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        db.delete(pedidos)
        db.commit()
        return {"mensaje": "Detalle de Pedido eliminado correctamente"}

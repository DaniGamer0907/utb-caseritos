from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Pedido import Pedido
from schemas.Pedido_schemas import PedidoC
from auth.dependencies import solo_admin, solo_cliente

router= APIRouter(prefix="/pedido", tags=["Pedidos"])

@router.post("/crearPedido")
def crear_pedido(pedido: PedidoC, db: Session = Depends(get_db)):
    pedidodb = Pedido(fecha_creacion=pedido.fecha_creacion, estado=pedido.estado, sugerencia=pedido.sugerencia)
    db.add(pedidodb)
    db.commit()
    return {"mensaje": "Pedido agregado correctamente"}

@router.get("/listPedidos")
def obtener_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedidos no encontrados")
    else:
        return pedidos

@router.get("/getPedido")
def obtener_pedido(id: int, db: Session=Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        return pedidos
    
@router.put("/actualizarPedido")
def actualizar_pedido(id: int, nuevo_pedido: PedidoC, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        pedidos.fecha_creacion = nuevo_pedido.fecha_creacion #type: ignore
        pedidos.estado = nuevo_pedido.estado #type: ignore
        pedidos.sugerencia = nuevo_pedido.sugerencia #type: ignore
        db.commit()
        return {"mensaje": "Pedido actualizado correctamente"}
    

@router.delete("/borrarPedido")
def eliminar_pedido(id: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.id==id).first()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        db.delete(pedidos)
        db.commit()
        return {"mensaje": "Pedido eliminado correctamente"}
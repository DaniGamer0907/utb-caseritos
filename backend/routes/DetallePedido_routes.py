from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.DetallePedido import DetallePedido
from models.Pedido import Pedido
from schemas.DetallePedido_schemas import DetallePedidoC
from auth.dependencies import get_current_user, require_cliente

router = APIRouter(prefix="/detallesPedido", tags=["Detalles de Pedidos"])


def _obtener_detalle_visible(db: Session, detalle_id: int, current_user: dict) -> DetallePedido | None:
    query = db.query(DetallePedido).join(Pedido).filter(DetallePedido.id == detalle_id)
    if current_user["role"] != "admin":
        query = query.filter(Pedido.usuario_id == current_user["user"].id)
    return query.first()


@router.post("/crearDetallesPedido", dependencies=[Depends(require_cliente)])
def crear_detalle_de_pedido(
    detalle_pedido: DetallePedidoC,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pedido = db.query(Pedido).filter(Pedido.id == detalle_pedido.pedidoid).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if current_user["role"] != "admin" and pedido.usuario_id != current_user["user"].id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este pedido")

    pedidodb = DetallePedido(
        pedidoid=detalle_pedido.pedidoid,
        proteinaid=detalle_pedido.proteinaid,
        tipalmuerzoid=detalle_pedido.tipalmuerzoid,
        cantidad=detalle_pedido.cantidad,
        precio_unitario=detalle_pedido.precio_unitario,
        total=detalle_pedido.total
    )
    db.add(pedidodb)
    db.commit()
    return {"mensaje": "Detalle de Pedido agregado correctamente"}


@router.get("/listDetallesPedidos", dependencies=[Depends(require_cliente)])
def obtener_detalles_de_pedidos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(DetallePedido).join(Pedido)
    if current_user["role"] != "admin":
        query = query.filter(Pedido.usuario_id == current_user["user"].id)
    pedidos = query.all()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedidos no encontrados")
    else:
        return pedidos


@router.get("/getDetallesPedido", dependencies=[Depends(require_cliente)])
def obtener_detalle_de_pedido(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pedidos = _obtener_detalle_visible(db, id, current_user)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        return pedidos


@router.put("/actualizarDetallesPedido", dependencies=[Depends(require_cliente)])
def actualizar_detalle_de_pedido(
    id: int,
    nuevo_detalle_pedido: DetallePedidoC,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pedidos = _obtener_detalle_visible(db, id, current_user)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        if pedidos.pedidoid != nuevo_detalle_pedido.pedidoid:
            pedido = db.query(Pedido).filter(Pedido.id == nuevo_detalle_pedido.pedidoid).first()
            if not pedido:
                raise HTTPException(status_code=404, detail="Pedido no encontrado")
            if current_user["role"] != "admin" and pedido.usuario_id != current_user["user"].id:
                raise HTTPException(status_code=403, detail="No tienes permiso para mover este detalle")
            pedidos.pedidoid = nuevo_detalle_pedido.pedidoid  # type: ignore
        pedidos.proteinaid = nuevo_detalle_pedido.proteinaid  # type: ignore
        pedidos.tipalmuerzoid = nuevo_detalle_pedido.tipalmuerzoid  # type: ignore
        pedidos.cantidad = nuevo_detalle_pedido.cantidad  # type: ignore
        pedidos.precio_unitario = nuevo_detalle_pedido.precio_unitario  # type: ignore
        pedidos.total = nuevo_detalle_pedido.total  # type: ignore
        db.commit()
        return {"mensaje": "Detalle de Pedido actualizado correctamente"}


@router.delete("/borrarDetallesPedido", dependencies=[Depends(require_cliente)])
def eliminar_detalle_de_pedido(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pedidos = _obtener_detalle_visible(db, id, current_user)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Detalle de Pedido no encontrado")
    else:
        db.delete(pedidos)
        db.commit()
        return {"mensaje": "Detalle de Pedido eliminado correctamente"}

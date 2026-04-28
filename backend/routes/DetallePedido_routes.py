from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.DetallePedido import DetallePedido
from models.Pedido import Pedido
from models.TipoAlmuerzo import TipoAlmuerzo
from models.Proteina import Proteina
from schemas.DetallePedido_schemas import DetallePedidoC
from auth.dependencies import get_current_user, require_admin, require_cliente

router = APIRouter(prefix="/detallesPedido", tags=["Detalles de Pedidos"])


def _obtener_detalle_visible(db: Session, detalle_id: int, current_user: dict) -> DetallePedido | None:
    query = db.query(DetallePedido).join(Pedido).filter(DetallePedido.id == detalle_id)
    if current_user["role"] != "admin":
        query = query.filter(Pedido.usuario_id == current_user["user"].id)
    return query.first()


def _recalcular_total_pedido(db: Session, pedido_id: int) -> None:
    total = (
        db.query(DetallePedido.total)
        .filter(DetallePedido.pedidoid == pedido_id)
        .all()
    )
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido:
        pedido.total = float(sum(row[0] or 0 for row in total))


@router.post("/crearDetallesPedido", dependencies=[Depends(require_admin)])
def crear_detalle_de_pedido(
    detalle_pedido: DetallePedidoC,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pedido = db.query(Pedido).filter(Pedido.id == detalle_pedido.pedidoid).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    proteina = db.query(Proteina).filter(Proteina.id == detalle_pedido.proteinaid).first()
    if not proteina:
        raise HTTPException(status_code=404, detail="Proteina no encontrada")
    tipo_almuerzo = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id == detalle_pedido.tipalmuerzoid).first()
    if not tipo_almuerzo:
        raise HTTPException(status_code=404, detail="Tipo de almuerzo no encontrado")
    if current_user["role"] != "admin" and pedido.usuario_id != current_user["user"].id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar este pedido")
    if not proteina.avaliable:
        raise HTTPException(status_code=400, detail="La proteina seleccionada no esta disponible")

    precio_unitario = float(tipo_almuerzo.precio or 0)
    pedidodb = DetallePedido(
        pedidoid=detalle_pedido.pedidoid,
        proteinaid=detalle_pedido.proteinaid,
        tipalmuerzoid=detalle_pedido.tipalmuerzoid,
        cantidad=detalle_pedido.cantidad,
        precio_unitario=precio_unitario,
        total=precio_unitario * detalle_pedido.cantidad
    )
    db.add(pedidodb)
    db.commit()
    _recalcular_total_pedido(db, detalle_pedido.pedidoid)
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
        proteina = db.query(Proteina).filter(Proteina.id == nuevo_detalle_pedido.proteinaid).first()
        if not proteina:
            raise HTTPException(status_code=404, detail="Proteina no encontrada")
        tipo_almuerzo = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id == nuevo_detalle_pedido.tipalmuerzoid).first()
        if not tipo_almuerzo:
            raise HTTPException(status_code=404, detail="Tipo de almuerzo no encontrado")
        if not proteina.avaliable:
            raise HTTPException(status_code=400, detail="La proteina seleccionada no esta disponible")
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
        pedidos.precio_unitario = float(tipo_almuerzo.precio or 0)  # type: ignore
        pedidos.total = float(tipo_almuerzo.precio or 0) * nuevo_detalle_pedido.cantidad  # type: ignore
        db.commit()
        _recalcular_total_pedido(db, pedidos.pedidoid)
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
        pedido_id = pedidos.pedidoid
        db.delete(pedidos)
        db.commit()
        _recalcular_total_pedido(db, pedido_id)
        db.commit()
        return {"mensaje": "Detalle de Pedido eliminado correctamente"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Pedido import Pedido
from schemas.Pedido_schemas import PedidoC
from auth.dependencies import get_current_user, require_cliente
from models.Usuario import Usuario

router = APIRouter(prefix="/pedido", tags=["Pedidos"])


def _obtener_pedido_visible(db: Session, pedido_id: int, current_user: dict) -> Pedido | None:
    query = db.query(Pedido).filter(Pedido.id == pedido_id)
    if current_user["role"] != "admin":
        query = query.filter(Pedido.usuario_id == current_user["user"].id)
    return query.first()


@router.post("/crearPedido", dependencies=[Depends(require_cliente)])
def crear_pedido(pedido: PedidoC, db: Session = Depends(get_db), current_user: Usuario = Depends(require_cliente)):
    pedidodb = Pedido(
        fecha_creacion=pedido.fecha_creacion or Pedido.fecha_creacion.default.arg, # type: ignore
        estado=pedido.estado,
        sugerencia=pedido.sugerencia,
        total=pedido.total,
        pago_id=pedido.pago_id,
        usuario_id=current_user.id
    )
    db.add(pedidodb)
    db.commit()
    db.refresh(pedidodb)
    return {"mensaje": "Pedido agregado correctamente", "id": pedidodb.id}


@router.get("/listPedidos", dependencies=[Depends(require_cliente)])
def obtener_pedidos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(Pedido)
    if current_user["role"] != "admin":
        query = query.filter(Pedido.usuario_id == current_user["user"].id)
    pedidos = query.all()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedidos no encontrados")
    else:
        return pedidos


@router.get("/getPedido", dependencies=[Depends(require_cliente)])
def obtener_pedido(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pedidos = _obtener_pedido_visible(db, id, current_user)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        return pedidos


@router.put("/actualizarPedido", dependencies=[Depends(require_cliente)])
def actualizar_pedido(
    id: int,
    nuevo_pedido: PedidoC,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pedidos = _obtener_pedido_visible(db, id, current_user)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        pedidos.fecha_creacion = nuevo_pedido.fecha_creacion #type: ignore
        pedidos.estado = nuevo_pedido.estado #type: ignore
        pedidos.sugerencia = nuevo_pedido.sugerencia #type: ignore
        pedidos.total = nuevo_pedido.total #type: ignore
        pedidos.pago_id = nuevo_pedido.pago_id #type: ignore
        db.commit()
        return {"mensaje": "Pedido actualizado correctamente"}


@router.delete("/borrarPedido", dependencies=[Depends(require_cliente)])
def eliminar_pedido(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pedidos = _obtener_pedido_visible(db, id, current_user)
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    else:
        db.delete(pedidos)
        db.commit()
        return {"mensaje": "Pedido eliminado correctamente"}

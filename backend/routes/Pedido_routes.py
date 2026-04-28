from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.Pedido import Pedido
from models.Pago import Pago
from models.DetallePedido import DetallePedido
from models.TipoAlmuerzo import TipoAlmuerzo
from models.Proteina import Proteina
from schemas.Pedido_schemas import PedidoC, PedidoCheckoutRequest
from auth.dependencies import get_current_user, require_admin, require_cliente
from models.Usuario import Usuario

router = APIRouter(prefix="/pedido", tags=["Pedidos"])


def _obtener_pedido_visible(db: Session, pedido_id: int, current_user: dict) -> Pedido | None:
    query = db.query(Pedido).filter(Pedido.id == pedido_id)
    if current_user["role"] != "admin":
        query = query.filter(Pedido.usuario_id == current_user["user"].id)
    return query.first()


ESTADOS_PEDIDO_VALIDOS = {"pendiente", "confirmado", "entregado", "cancelado"}
METODOS_PAGO_VALIDOS = {"efectivo", "nequi"}


@router.post("/crearPedidoManual", dependencies=[Depends(require_admin)])
def crear_pedido_manual(pedido: PedidoC, db: Session = Depends(get_db), current_user: Usuario = Depends(require_admin)):
    if pedido.total <= 0:
        raise HTTPException(status_code=400, detail="El total del pedido debe ser mayor que 0")
    if not pedido.pago_id:
        raise HTTPException(status_code=400, detail="El pedido debe incluir un pago")
    if pedido.estado not in ESTADOS_PEDIDO_VALIDOS:
        raise HTTPException(status_code=400, detail="Estado de pedido invalido")
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


@router.post("/crearPedido", dependencies=[Depends(require_cliente)])
def crear_pedido(
    payload: PedidoCheckoutRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_cliente)
):
    metodo_pago = payload.pago.metodopago.strip().lower()
    if metodo_pago not in METODOS_PAGO_VALIDOS:
        raise HTTPException(status_code=400, detail="Metodo de pago invalido")
    if metodo_pago == "nequi" and not payload.pago.referencia:
        raise HTTPException(status_code=400, detail="La referencia de Nequi es obligatoria")

    detalles_resueltos: list[dict] = []
    total_pedido = 0.0

    for detalle in payload.detalles:
        proteina = db.query(Proteina).filter(Proteina.id == detalle.proteinaid).first()
        if not proteina:
            raise HTTPException(status_code=404, detail="Proteina no encontrada")
        if not proteina.avaliable:
            raise HTTPException(status_code=400, detail="La proteina seleccionada no esta disponible")

        tipo_almuerzo = db.query(TipoAlmuerzo).filter(TipoAlmuerzo.id == detalle.tipalmuerzoid).first()
        if not tipo_almuerzo:
            raise HTTPException(status_code=404, detail="Tipo de almuerzo no encontrado")

        precio_unitario = float(tipo_almuerzo.precio or 0)
        total_detalle = precio_unitario * detalle.cantidad
        total_pedido += total_detalle
        detalles_resueltos.append(
            {
                "proteinaid": detalle.proteinaid,
                "tipalmuerzoid": detalle.tipalmuerzoid,
                "cantidad": detalle.cantidad,
                "precio_unitario": precio_unitario,
                "total": total_detalle,
            }
        )

    if total_pedido <= 0:
        raise HTTPException(status_code=400, detail="El total del pedido debe ser mayor que 0")

    pagodb = Pago(
        metodopago=metodo_pago,
        diadelpago=payload.pago.diadelpago,
        monto=total_pedido,
        referencia=payload.pago.referencia.strip() if payload.pago.referencia else None
    )
    db.add(pagodb)
    db.flush()

    pedidodb = Pedido(
        fecha_creacion=Pedido.fecha_creacion.default.arg,  # type: ignore
        estado="pendiente",
        sugerencia=payload.sugerencia,
        total=total_pedido,
        pago_id=pagodb.id,
        usuario_id=current_user.id
    )
    db.add(pedidodb)
    db.flush()

    for detalle in detalles_resueltos:
        db.add(
            DetallePedido(
                pedidoid=pedidodb.id,
                proteinaid=detalle["proteinaid"],
                tipalmuerzoid=detalle["tipalmuerzoid"],
                cantidad=detalle["cantidad"],
                precio_unitario=detalle["precio_unitario"],
                total=detalle["total"]
            )
        )

    db.commit()
    db.refresh(pedidodb)
    return {
        "mensaje": "Pedido agregado correctamente",
        "id": pedidodb.id,
        "total": total_pedido,
    }


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
        if nuevo_pedido.estado not in ESTADOS_PEDIDO_VALIDOS:
            raise HTTPException(status_code=400, detail="Estado de pedido invalido")
        pedidos.fecha_creacion = nuevo_pedido.fecha_creacion #type: ignore
        pedidos.estado = nuevo_pedido.estado #type: ignore
        pedidos.sugerencia = nuevo_pedido.sugerencia #type: ignore
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

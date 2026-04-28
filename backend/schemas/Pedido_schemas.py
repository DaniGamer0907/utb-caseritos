from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class PedidoC(BaseModel):
    fecha_creacion: Optional[datetime] = None
    estado: str # pendiente, confirmado, entregado, cancelado
    sugerencia: Optional[str] = None
    total: float
    pago_id: int

class PedidoCreate(PedidoC):
    pass

class PedidoResponse(PedidoC):
    id: int
    usuario_id: int
    pago_id: int

    class Config:
        from_attributes = True


class PedidoCheckoutDetalle(BaseModel):
    proteinaid: int
    tipalmuerzoid: int
    cantidad: int = Field(gt=0)


class PedidoCheckoutPago(BaseModel):
    metodopago: str
    diadelpago: date
    referencia: Optional[str] = None


class PedidoCheckoutRequest(BaseModel):
    sugerencia: Optional[str] = None
    pago: PedidoCheckoutPago
    detalles: list[PedidoCheckoutDetalle] = Field(min_length=1)

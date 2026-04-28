from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PedidoC(BaseModel):
    fecha_creacion: Optional[datetime] = None
    estado: str # nequi, efectivo, confirmado, entregado, cancelado
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
from pydantic import BaseModel
from datetime import date

class PedidoC(BaseModel):
    fecha_creacion: date
    estado: bool
    sugerencia: str

class PedidoCreate(PedidoC):
    pass

class PedidoResponse(PedidoC):
    id: int

    class Config:
        from_attributes = True
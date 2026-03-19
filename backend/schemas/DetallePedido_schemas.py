from pydantic import BaseModel

class DetallePedidoC(BaseModel):
    cantidad: int 
    precio_unitario: float
    total: float


class DetallePedidoCreate(DetallePedidoC):
    pass

class DetallePedidoResponse(DetallePedidoC):
    id: int

    class Config:
        from_attributes = True
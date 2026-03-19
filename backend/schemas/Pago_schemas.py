from pydantic import BaseModel
from datetime import date

class PagoC(BaseModel):
    metodopago: str
    diadelpago: date
    monto: float

class PagoCreate(PagoC):
    pass

class PagoResponse(PagoC):
    id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import date
from typing import Optional

class PagoC(BaseModel):
    metodopago: str
    diadelpago: date
    monto: float
    referencia: Optional[str] = None

class PagoCreate(PagoC):
    pass

class PagoResponse(PagoC):
    id: int

    class Config:
        from_attributes = True
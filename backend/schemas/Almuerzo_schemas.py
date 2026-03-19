from pydantic import BaseModel
from datetime import date

class AlmuerzoC(BaseModel):
    descripcion: str
    fecha: date


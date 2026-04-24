from pydantic import BaseModel
from datetime import date

class AlmuerzoC(BaseModel):
    fecha: date


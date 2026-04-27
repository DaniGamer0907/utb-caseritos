from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlmuerzoC(BaseModel):
    fecha: Optional[datetime] = None
    proteinaid: int
    tipalmuerzo: int

class AlmuerzoResponse(AlmuerzoC):
    id: int

    class Config:
        from_attributes = True

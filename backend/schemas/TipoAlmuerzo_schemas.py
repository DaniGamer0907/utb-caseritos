from pydantic import BaseModel

class TipoAlmuerzoC(BaseModel):
    nombre : str
    precio : float

class TipoAlmuerzoCreate(TipoAlmuerzoC):
    pass

class TipoAlmuerzoResponse(TipoAlmuerzoC):
    id: int

    class Config:
        from_attributes = True
    
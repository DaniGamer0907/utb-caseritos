from pydantic import BaseModel

class ProteinaC(BaseModel):
    nombre : str
    avaliable : int

class ProteinaCreate(ProteinaC):
    pass

class ProteinaResponse(ProteinaC):
    id: int

    class Config:
        from_attributes = True



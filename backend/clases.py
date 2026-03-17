from pydantic import BaseModel

class ClienteC(BaseModel):
    name: str
    lastname: str
    address: str
    phone: str
    email: str

class ProteinasC(BaseModel):
    nombre : str
    avaliable : int

class TipoAlmuerzoC(BaseModel):
    nombre : str
    precio : float
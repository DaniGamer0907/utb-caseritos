from pydantic import BaseModel

class Cliente(BaseModel):
    name: str
    lastname: str
    address: str
    phone: str
    email: str

class Proteinas2(BaseModel):
    nombre : str
    avaliable : int

class TipoAlmuerzo(BaseModel):
    id_tipo_almuerzo : int
    nom_tipo_almuerzo : str
    precio : float
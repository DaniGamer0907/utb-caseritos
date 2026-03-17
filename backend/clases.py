from datetime import date
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
    
class AlmuerzoC(BaseModel):
    descripcion: str
    fecha: date

class PedidosC(BaseModel):
    fecha_creacion: date
    estado: bool
    sugerencia: str

class DetallePedidosC(BaseModel):
    cantidad: int 
    precio_unitario: float
    total: float
    
class pago(BaseModel):
    metodopago: str
    diadelpago: str
    monto: float

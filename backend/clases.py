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
    fecha: str

class PedidosC(BaseModel):
    fecha_creacion: str
    estado: bool
    sugerencia: str

class DetallePedidosC(BaseModel):
    cantidad: int 
    precio_unitario: float
    total: float
    
class pago(BaseModel):
    id : int
    metodopago: str
    diadelpago: str
    monto: float

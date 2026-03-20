from pydantic import BaseModel

class UsuarioC(BaseModel):
    name: str
    lastname: str
    password: str
    address: str
    phone: str
    email: str

class UsuarioCreate(UsuarioC):
    pass

class UsuarioUpdate(UsuarioC):
    password:str
    address: str
    phone: str

class UsuarioResponse(UsuarioC):
    id: int

    class Config:
        from_attributes = True  

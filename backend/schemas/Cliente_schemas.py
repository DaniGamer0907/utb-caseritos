from pydantic import BaseModel

class ClienteC(BaseModel):
    name: str
    lastname: str
    address: str
    phone: str
    email: str

class ClienteCreate(ClienteC):
    pass

class ClienteUpdate(ClienteC):
    pass

class ClienteResponse(ClienteC):
    id: int

    class Config:
        from_attributes = True  

from pydantic import BaseModel

class token(BaseModel):
    access_token: str
    token_type: str
    role: str

class tokenData(BaseModel):
    user: str
    role: str

class loginRequest(BaseModel):
    email: str
    password: str
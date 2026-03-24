from datetime import datetime, timedelta,UTC
from jose import JWTError, jwt
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def create_access_token(user:str, role:str) -> str:
    payload = {
        "sub": user,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(minutes=int(getenv("EXPIRE_MINUTES")))
    }
    return jwt.encode(payload, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token,getenv("SECRET_KEY"),algorithms=[getenv("ALGORITHM")])
    except JWTError:
        return None
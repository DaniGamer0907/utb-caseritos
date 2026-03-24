from datetime import datetime, timedelta,UTC
from jose import JWTError, jwt

SECRET_KEY = 'ALW739362-2732jdkwllanq@jsndksdkeow0p2+30281'
ALGORITHM = 'HS256'
EXPIRE_MINUTES = 60

def create_access_token(user:str, role:str) -> str:
    payload = {
        "sub": user,
        "role": role,
        "exp": datetime.now(UTC) + timedelta(minutes=EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        return None
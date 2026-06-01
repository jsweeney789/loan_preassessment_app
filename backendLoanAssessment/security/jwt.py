from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

import os

SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET environment variable is not set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

def createJwtToken(data: dict):
    toEncode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    toEncode.update({"exp": expire})

    return jwt.encode(
        toEncode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decodeJwtToken(token: str):
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        return None
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# This checks the Authorization header and or if there is a value with a bearer token for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data.update({"exp": expire_time})
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception):
    try:
        # Check to see if the token was tampered with or not
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Get the user_id from the id field in the payload
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception=credentials_exception)

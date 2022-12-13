from passlib.context import CryptContext
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

while True:
    try:
        conn = psycopg2.connect(host=settings.database_hostname, user=settings.database_username, dbname=settings.database_name,
                                password=settings.database_password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print({"Error": error})
        time.sleep(2)


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(password: str, password_hashed: str):
    return pwd_context.verify(password, password_hashed)

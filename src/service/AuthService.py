from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from argon2 import PasswordHasher
import os
import hashlib

load_dotenv()
ph = PasswordHasher()

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def has_password(password: str): 
    # sha = hashlib.sha256(password.encode()).digest()
    return ph.hash(password)

def verify_password(plain: str, hashed: str):
    try:
        return ph.verify(hashed, plain)
    except Exception:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

def decode_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=os.getenv(["ALGORITHM"]))
        return payload
    except JWTError:
        return None

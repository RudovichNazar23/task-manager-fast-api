from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def is_hashed_password(password: str) -> bool:
    return pwd_context.identify(password) is not None

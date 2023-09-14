from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hashed(passowrd: str):
    return pwd_context.hash(passowrd)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

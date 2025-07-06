import secrets

from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def generate_random_value(length: int = 20):
    return secrets.token_hex(length)


def get_hash_from_password(password: str):
    return pwd_context.hash(password)


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

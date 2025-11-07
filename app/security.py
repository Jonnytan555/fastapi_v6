from passlib.context import CryptContext

# Pre-hash with SHA256, then bcrypt → avoids the 72-byte limit
_pwd = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return _pwd.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return _pwd.verify(plain, hashed)

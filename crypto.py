@"
import os
import base64
import secrets
import string
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

ph = PasswordHasher()

def hash_master_password(password: str) -> str:
    return ph.hash(password)

def verify_master_password(password: str, password_hash: str) -> bool:
    try:
        ph.verify(password_hash, password)
        return True
    except VerificationError:
        return False

def derive_encryption_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(master_password.encode())

def encrypt_data(data: str, master_password: str) -> tuple:
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_encryption_key(master_password, salt)
    
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data.encode(), None)
    
    return (
        base64.b64encode(ciphertext).decode(),
        base64.b64encode(nonce).decode(),
        base64.b64encode(salt).decode()
    )

def decrypt_data(ciphertext_b64: str, nonce_b64: str, salt_b64: str, master_password: str) -> str:
    ciphertext = base64.b64decode(ciphertext_b64)
    nonce = base64.b64decode(nonce_b64)
    salt = base64.b64decode(salt_b64)
    
    key = derive_encryption_key(master_password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
"@ | Out-File -FilePath crypto.py -Encoding utf8
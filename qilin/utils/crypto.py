import base64
import os
from cryptography.fernet import Fernet

def get_crypto_key():
    key = os.environ.get('QILIN_CRYPTO_KEY')
    # Check if key is a url-safe base64-encoded 32-byte key
    if key is not None:
        try:
            key_bytes = base64.urlsafe_b64decode(key.encode('utf-8'))
            if len(key_bytes) == 32:
                return key.encode('utf-8')
        except:
            pass
    if key is None: key = ''
    key_bytes = key.encode('utf-8')
    if len(key_bytes) < 32:
        key_bytes += b'\x00' * (32 - len(key_bytes))
    return base64.urlsafe_b64encode(key_bytes[:32])


def encrypt_string(plaintext: str) -> str:
    encoded = plaintext.encode('utf-8')
    f = Fernet(get_crypto_key())
    encrypted = f.encrypt(encoded)
    return base64.urlsafe_b64encode(encrypted).decode('utf-8')


def decrypt_string(secret: str) -> str:
    secret_bytes = base64.urlsafe_b64decode(secret.encode('utf-8'))
    f = Fernet(get_crypto_key())
    decrypted = f.decrypt(secret_bytes)
    return decrypted.decode('utf-8')


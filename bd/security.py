from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os

from dotenv import load_dotenv

load_dotenv()

KEY = base64.b64decode(os.getenv("AEG_KEY"))
aesgcm_engine = AESGCM(KEY)

def encrypt_data(api_key, secret_key):
    api_key = api_key.encode("UTF-8")
    secret_key = secret_key.encode("UTF-8")
    nonce_api = os.urandom(12)
    cipher_api = aesgcm_engine.encrypt(nonce=nonce_api, data=api_key, associated_data=None)

    nonce_secret = os.urandom(12)
    cipher_secret = aesgcm_engine.encrypt(nonce=nonce_secret, data=secret_key, associated_data=None)

    nonce_api = base64.b64encode(nonce_api).decode("UTF-8")
    cipher_api = base64.b64encode(cipher_api).decode("UTF-8")
    nonce_secret = base64.b64encode(nonce_secret).decode("UTF-8")
    cipher_secret = base64.b64encode(cipher_secret).decode("UTF-8")

    return {"nonce_api": nonce_api, "cipher_api": cipher_api, "nonce_secret": nonce_secret, "cipher_secret": cipher_secret}

def decrypt_data(nonce_api, cipher_api, nonce_secret, cipher_secret):
    nonce_api = base64.b64decode(nonce_api)
    cipher_api = base64.b64decode(cipher_api)
    nonce_secret = base64.b64decode(nonce_secret)
    cipher_secret = base64.b64decode(cipher_secret)

    api_key = aesgcm_engine.decrypt(nonce=nonce_api, data=cipher_api, associated_data=None)
    secret_key = aesgcm_engine.decrypt(nonce=nonce_secret, data=cipher_secret, associated_data=None)

    return {"api_key": api_key.decode("UTF-8"), "secret_key": secret_key.decode("UTF-8")}


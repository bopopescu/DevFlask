import os
from hashlib import sha256
from hmac import HMAC
import base64
s = 'asdwtgdu'
salt = bytes(s, encoding = "utf8")

def encrypt_password(password, salt=salt):
    """Hash password on the fly."""
    if salt is None:
        salt = os.urandom(8)  # 64 bits.

    assert 8 == len(salt)
    assert isinstance(salt, bytes)
    assert isinstance(password, str)
    
    if isinstance(password, str):
        password = password.encode('UTF-8')

    assert isinstance(password, bytes)

    result = password
    for i in range(10):
        result = HMAC(result, salt, sha256).digest()

    return base64.b64encode(salt + result)

def validate_password(hashed, input_password,salt=salt):

    return hashed == encrypt_password(input_password, salt)

if __name__ == "__main__":
    print(type(salt))
    hashed = encrypt_password('secret password')
    assert validate_password(hashed, 'secret password')
    print (hashed)
    
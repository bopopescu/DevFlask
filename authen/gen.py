import base64
import uuid
import os


def generate_token(username):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, username+os.getenv('TOKEN_SALT')))


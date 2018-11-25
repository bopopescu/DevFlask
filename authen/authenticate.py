from authen import TokenPool

def set_token(key,token, expire=3600, Pool = TokenPool):
    key = "user_token_%d"%key
    Pool.set(key, token, ex=expire)

def authen_token(key,token,Pool = TokenPool):
    res = Pool.get("user_token_%d"%key)
    if res == None or token == None:
        return False
    elif token == res:
        return True
    return False


def get_token(key,Pool=TokenPool):
    key = 'user_token_%d'%key
    Pool.get(key)

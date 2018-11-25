from authen.authenticate import *
from authen.gen import *

if __name__ == '__main__':
    token = generate_token('jack')
    print('gen token :',token)
    set_token(1,token, 300)
    print("test1:" ,authen_token(2,"asdasfadsa"))
    print("test2:", authen_token(1,token))

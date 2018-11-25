import redis

TokenPool = redis.Redis(host='localhost', port=6379, decode_responses=True)

from authen import authenticate
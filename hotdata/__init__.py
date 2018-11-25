import redis

DataPool = redis.Redis(host='localhost', port=6379, decode_responses=True)

from hotdata import codeInfo
from hotdata import codeInfo_delta
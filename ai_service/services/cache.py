import redis
import json
import hashlib

r = redis.Redis(host='localhost', port=6379, db=0)

def get_cache(key):
    data = r.get(key)
    return json.loads(data) if data else None

def set_cache(key, value, ttl=900):  # 15 min
    r.setex(key, ttl, json.dumps(value))

def increment_hit():
    r.incr("cache_hit")

def increment_miss():
    r.incr("cache_miss")
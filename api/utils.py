
import django_redis

def get_redis_connection():
    return django_redis.get_redis_connection("default")
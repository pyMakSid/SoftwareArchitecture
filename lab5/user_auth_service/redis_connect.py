import json

import redis

class RedisConnection:


    def __init__(self, host : str = 'redis',
        port: int = 6379,
        CACHE_EXPIRATION: int = 3600,
        charset: str = 'utf-8'):
        self.connection = redis.Redis(host=host,
                                    port=port,
                                    charset=charset,
                                    decode_responses=True)
        self.CACHE_EXPIRATION = CACHE_EXPIRATION


    def get_user_from_cache(self, user_login: str):
        """Read-through cache method to get user data from Redis"""
        cached_user = self.connection.get(f"user:{user_login}")
        if cached_user:
            return json.loads(cached_user)
        return None


    def set_user_to_cache(self, user_login: str, user_data: dict):
        """Write-through cache method to store user data in Redis"""
        self.connection.setex(f"user:{user_login}", self.CACHE_EXPIRATION, json.dumps(user_data))


    def delete_user_from_cache(self, user_login: str):
        """Delete user data from Redis cache"""
        self.connection.delete(f"user:{user_login}")


    def invalidate_users_list_cache(self):
        """Invalidate the users list cache"""
        self.connection.delete("users:list")


    def get_users_list_from_cache(self):
        """Get users list from cache"""
        cached_users = self.connection.get("users:list")
        if cached_users:
            return json.loads(cached_users)
        return None


    def set_users_list_to_cache(self, users_data: list):
        """Store users list in cache"""
        self.connection.setex("users:list", self.CACHE_EXPIRATION, json.dumps(users_data))

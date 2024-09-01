import json
from pymongo import MongoClient
import redis
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.use_json_cache = settings.use_json_cache
        self.use_mongo_cache = settings.use_mongo_cache
        
        if self.use_mongo_cache:
            self.mongo_client = MongoClient(settings.mongodb.uri)
            self.mongo_db = self.mongo_client[settings.mongodb.db_name]
            self.mongo_collection = self.mongo_db[settings.mongodb.collection_name]
        
        if settings.redis.enabled:
            self.redis_client = redis.Redis(
                host=settings.redis.host,
                port=settings.redis.port,
                db=settings.redis.db
            )

    async def get(self, key: str):
        if settings.redis.enabled:
            redis_result = self.redis_client.get(key)
            if redis_result:
                return json.loads(redis_result)
        
        if self.use_mongo_cache:
            mongo_result = self.mongo_collection.find_one({"_id": key})
            if mongo_result:
                return mongo_result["response"]
        
        if self.use_json_cache:
            try:
                with open(settings.json_cache_file, 'r') as f:
                    cache = json.load(f)
                    return cache.get(key)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        
        return None

    async def set(self, key: str, value: str, expire: int = 3600):
        if settings.redis.enabled:
            self.redis_client.setex(key, expire, json.dumps(value))
        
        if self.use_mongo_cache:
            self.mongo_collection.update_one(
                {"_id": key},
                {"$set": {"response": value}},
                upsert=True
            )
        
        if self.use_json_cache:
            try:
                with open(settings.json_cache_file, 'r') as f:
                    cache = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                cache = {}
            
            cache[key] = value
            
            with open(settings.json_cache_file, 'w') as f:
                json.dump(cache, f)

    async def delete(self, key: str):
        if settings.redis.enabled:
            self.redis_client.delete(key)
        
        if self.use_mongo_cache:
            self.mongo_collection.delete_one({"_id": key})
        
        if self.use_json_cache:
            try:
                with open(settings.json_cache_file, 'r') as f:
                    cache = json.load(f)
                
                if key in cache:
                    del cache[key]
                
                with open(settings.json_cache_file, 'w') as f:
                    json.dump(cache, f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
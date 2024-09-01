import os
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import yaml
from typing import Dict, List, Optional


from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl, Field
from typing import List, Dict, Optional

class LLMSchema(BaseModel):
    endpoint: HttpUrl
    headers: List[str]
    temperature_threshold: float

class MongoDBConfig(BaseModel):
    uri: str
    db_name: str
    collection_name: str

class RedisConfig(BaseModel):
    enabled: bool
    host: str
    port: int
    db: int

class Configs(BaseModel):
    llm_schemas: Dict[str, LLMSchema]
    mongodb: MongoDBConfig
    json_cache_file: str
    redis: RedisConfig
    current_llm_service: str
    use_json_cache: bool
    use_mongo_cache: bool

    @classmethod
    def load_from_yaml(cls, yaml_file: str):
        with open(yaml_file, "r") as f:
            config_data = yaml.safe_load(f)        
        return cls(**config_data)
    
    # class Config(SettingsConfigDict):
    #     env_file = ".env"  # Specify an environment file if needed
    #     env_file_encoding = 'utf-8'
    #     case_sensitive = True
    


settings = Configs.load_from_yaml("config.yaml")

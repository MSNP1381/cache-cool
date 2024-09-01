from pydantic import BaseModel, HttpUrl, Field, model_validator
from typing import Any, List, Optional, Dict

class Message(BaseModel):
    role: Optional[str]
    content: Optional[str]
    message:Optional[ str]
    
    @model_validator(mode='before')
    @classmethod
    def validate_input(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        # Check if the input is a simple string
        if isinstance(values, str):
            values = {"role": "user", "content": values, "message": values}
        elif isinstance(values, dict):
            # Ensure required fields are present
            if 'content' not in values:
                raise ValueError("Field 'content' is required.")
            if 'role' not in values:
                values['role'] = "user"  # Default role if not provided
            values['message'] = values.get('message', values['content'])  # Default message
            
        return values

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    n:Optional[int]=None 
    stop:Optional[str]=""

class LLMSchemaUpdate(BaseModel):
    endpoint: Optional[str] = None
    headers: Optional[List[str]] = None
    temperature_threshold: Optional[float] = None


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

class ConfigurationUpdate(BaseModel):
    llm_schemas: Dict[str, LLMSchema]
    mongodb: MongoDBConfig
    json_cache_file: str
    redis: RedisConfig
    current_llm_service: str
    use_json_cache: bool
    use_mongo_cache: bool

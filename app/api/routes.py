import json
from typing import Dict
from fastapi import APIRouter, HTTPException, Request
from app.core.config import Configs, settings
from app.services.llm_service import LLMService
from app.services.cache_service import CacheService
from app.api.models import ChatCompletionRequest, ConfigurationUpdate

router = APIRouter()


@router.post("/{schema_name}/chat/completions")
async def chat_completions(schema_name: str,request: Request):
    cache_service = CacheService()
    llm_service = LLMService.check_type(schema_name)
    request_body_json: Dict = await request.json()
    
    print(request_body_json)
    chat_request=ChatCompletionRequest(**request_body_json)
    # Access headers
    headers = request.headers
    api_key=headers.get("Authorization")
    if not api_key:
        raise HTTPException(status_code=401, detail="no key!?")

    # Check cache if temperature is below threshold
    if chat_request.temperature <= llm_service.get_temperature_threshold():
        cached_response = await cache_service.get(json.dumps(request_body_json))
        if cached_response:
            return cached_response
    # Make API call
    response = await llm_service.generate_response(chat_request,api_key)

    # Cache response if temperature is below threshold
    if chat_request.temperature <= llm_service.get_temperature_threshold():
        await cache_service.set(chat_request.model_dump_json(), response)

    return response

@router.get("/configure")
async def get_configuration():
    return settings


@router.put("/configure")
async def update_configuration(config: Configs):
    global settings  # Declare settings as global to modify the global settings object
    
    try:
        # Update settings using the `copy(update=...)` method
        updated_settings = settings.copy(update=config.dict(exclude_unset=True))
        
        # Apply the updated settings
        settings = updated_settings
    except Exception as e:
        # Return an error response if updating fails
        raise HTTPException(status_code=400, detail=f'Error in input validation: {e}')
    
    # Reinitialize services if certain keys are updated
    update_keys = config.dict(exclude_unset=True).keys()
    
    # Check if LLM service needs to be reinitialized
    if 'current_llm_service' in update_keys:
        LLMService().__init__()  # Reinitialize LLM service
    
    # Check if any cache-related settings were updated
    cache_related_keys = {'use_json_cache', 'use_mongo_cache', 'redis'}
    if cache_related_keys.intersection(update_keys):
        CacheService().__init__()  # Reinitialize Cache service
    
    return {"message": "Configuration updated successfully"}
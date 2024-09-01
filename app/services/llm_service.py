import requests
from fastapi.datastructures import Headers
import httpx
from app.core.config import settings
from app.api.models import ChatCompletionRequest

class LLMService:
    def __init__(self,service:str=None):
        self.current_service = service or settings.current_llm_service
        self.schema = settings.llm_schemas[self.current_service]

    async def generate_response(self, request: ChatCompletionRequest,api_key:str):
        request_json=request.model_dump_json()

        headers = {header.split(': ')[0]: header.split(': ')[1].format(api_key=api_key)
                for header in self.schema.headers}
        print(headers)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                str(self.schema.endpoint),
                headers=headers,
                content=request_json
            )
        print([i for i in response.iter_text()])
        response.raise_for_status()
        return response.json()

    def get_temperature_threshold(self):
        return self.schema.temperature_threshold
    @classmethod
    def check_type(cls, schema_name):
        if schema_name not in settings.llm_schemas:
            return None
        else: return cls(schema_name)
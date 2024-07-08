from typing import Optional, Union, Dict, List, Any
import time
import json
import asyncio

import httpx

from ._base_client import SyncAPIClient, AsyncAPIClient
from .models import ModelModel, GenerateModel, StatusModel


class FusionBrainAI(SyncAPIClient):
    api_key: str
    secret_key: str

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        *,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        custom_headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(timeout=timeout, custom_headers=custom_headers)

        self.api_key = api_key
        self.secret_key = secret_key

    def get_models(self) -> List[ModelModel]:
        response = self.get("/key/api/v1/models")
        data = response.json()
        return list(map(ModelModel.from_dict, data))

    def generate(
        self,
        prompt: str,
        *,
        model_id: int = 4,
        width: int = 1024,
        height: int = 1024,
    ) -> str:
        params = {
            "type": "GENERATE",
            "numImages": 1,
            "width": width,
            "height": height,
            "generateParams": {"query": prompt}
        }
        data = {
            "model_id": (None, str(model_id)),
            "params": (None, json.dumps(params), "application/json")
        }
        response = self.post("/key/api/v1/text2image/run", files=data)
        data = response.json()
        return GenerateModel.from_dict(data)

    def check_status(self, request_id: str) -> StatusModel:
        response = self.get(f"/key/api/v1/text2image/status/{request_id}")
        data = response.json()
        return StatusModel.from_dict(data)

    def wait_generation(self, request_id: str, attempts: int = 10, delay: int = 3):
        while attempts > 0:
            request_status = self.check_status(request_id)

            if request_status.status == "DONE":
                print("\r", end="\033[K", flush=True)
                return request_status

            print(
                f"\r[{attempts}] Waiting for image generation. "
                f"Status: {request_status.status}",
                end="\033[K",
                flush=True
            )
            attempts -= 1
            time.sleep(delay)

    @property
    def auth_headers(self) -> Dict[str, str]:
        return {
            "X-Key": f"Key {self.api_key}",
            "X-Secret": f"Secret {self.secret_key}"
        }


class AsyncFusionBrainAI(AsyncAPIClient):
    api_key: str
    secret_key: str

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        *,
        timeout: Optional[Union[float, httpx.Timeout]] = None,
        custom_headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(timeout=timeout, custom_headers=custom_headers)

        self.api_key = api_key
        self.secret_key = secret_key

    async def get_models(self) -> List[ModelModel]:
        response = await self.get("/key/api/v1/models")
        data = response.json()
        return list(map(ModelModel.from_dict, data))

    async def generate(
        self,
        prompt: str,
        *,
        model_id: int = 4,
        width: int = 1024,
        height: int = 1024,
    ) -> str:
        params = {
            "type": "GENERATE",
            "numImages": 1,
            "width": width,
            "height": height,
            "generateParams": {"query": prompt}
        }
        data = {
            "model_id": (None, str(model_id)),
            "params": (None, json.dumps(params), "application/json")
        }
        response = await self.post("/key/api/v1/text2image/run", files=data)
        data = response.json()
        return GenerateModel.from_dict(data)

    async def check_status(self, request_id: str) -> StatusModel:
        response = await self.get(f"/key/api/v1/text2image/status/{request_id}")
        data = response.json()
        return StatusModel.from_dict(data)

    async def wait_generation(self, request_id: str, attempts: int = 10, delay: int = 3):
        while attempts > 0:
            request_status = await self.check_status(request_id)

            if request_status.status == "DONE":
                print("\r", end="\033[K", flush=True)
                return request_status

            print(
                f"\r[{attempts}] Waiting for image generation. "
                f"Status: {request_status.status}",
                end="\033[K",
                flush=True
            )
            attempts -= 1
            await asyncio.sleep(delay)

    @property
    def auth_headers(self) -> Dict[str, str]:
        return {
            "X-Key": f"Key {self.api_key}",
            "X-Secret": f"Secret {self.secret_key}"
        }

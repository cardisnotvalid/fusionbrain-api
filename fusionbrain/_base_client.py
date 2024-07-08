from typing import TypeVar, Generic, Optional, Union, Dict, Any

import httpx
from httpx import URL, Timeout, Request, Response

from ._constants import DEFAULT_TIMEOUT


HttpxClientT = TypeVar("HttpxClientT", bound=[httpx.Client, httpx.AsyncClient])


class BaseClient(Generic[HttpxClientT]):
    _client: HttpxClientT
    _custom_headers: Dict[str, Any]

    timeout: Timeout
    base_url = URL("https://api-key.fusionbrain.ai")

    def __init__(
        self,
        *,
        timeout: Optional[Union[float, Timeout]] = None,
        custom_headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.timeout = timeout or DEFAULT_TIMEOUT
        self._custom_headers = custom_headers or {}

    def _prepare_url(self, url: Union[str, URL]) -> URL:
        return self.base_url.join(URL(url))

    def _prepare_headers(self, headers: Dict[str, Any]) -> Dict[str, Any]:
        return {**self.default_headers, **headers, **self.auth_headers}

    def _build_request(self, method: str, url: str, **kwargs) -> Request:
        headers = self._prepare_headers(kwargs.pop("headers", {}))
        return self._client.build_request(
            method=method,
            url=self._prepare_url(url),
            headers=headers,
            timeout=self.timeout,
            **kwargs
        )

    @property
    def auth_headers(self) -> Dict[str, str]:
        return {}

    @property
    def default_headers(self) -> Dict[str, str]:
        return {"Accept": "application/json", **self._custom_headers}


class SyncAPIClient(BaseClient[httpx.Client]):
    _client: httpx.Client

    def __init__(
        self,
        *,
        timeout: Optional[Union[float, Timeout]] = None,
        custom_headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(timeout=timeout, custom_headers=custom_headers)
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def close(self) -> None:
        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self) -> "SyncAPIClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def get(self, url: str, **kwargs) -> Response:
        return self._client.send(self._build_request("GET", url, **kwargs))

    def post(self, url: str, **kwargs) -> Response:
        return self._client.send(self._build_request("POST", url, **kwargs))


class AsyncAPIClient(BaseClient[httpx.AsyncClient]):
    _client: httpx.AsyncClient

    def __init__(
        self,
        *,
        timeout: Optional[Union[float, Timeout]] = None,
        custom_headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(timeout=timeout, custom_headers=custom_headers)
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def close(self) -> None:
        if hasattr(self, "_client"):
            await self._client.aclose()

    async def __aenter__(self) -> "AsyncAPIClient":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def get(self, url: str, **kwargs) -> Response:
        return await self._client.send(self._build_request("GET", url, **kwargs))

    async def post(self, url: str, **kwargs) -> Response:
        return await self._client.send(self._build_request("POST", url, **kwargs))


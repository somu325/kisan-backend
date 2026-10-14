from typing import Any, Dict, Optional
import httpx
from app.core.exceptions import ExternalServiceException
from app.core.logging import get_logger

logger = get_logger(__name__)


class BaseAsyncHTTPClient:
    """Production async HTTP client wrapper with timeouts and error handling."""

    def __init__(self, base_url: str = "", timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            try:
                response = await client.get(endpoint, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error("HTTP error from %s: %s", endpoint, e.response.text)
                raise ExternalServiceException(
                    message=f"External API returned error {e.response.status_code}",
                    details={"endpoint": endpoint, "status_code": e.response.status_code},
                )
            except httpx.RequestError as e:
                logger.error("Request error connecting to %s: %s", endpoint, str(e))
                raise ExternalServiceException(
                    message="Failed to connect to external service",
                    details={"endpoint": endpoint, "error": str(e)},
                )

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            try:
                response = await client.post(endpoint, data=data, json=json_data, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error("HTTP error from %s: %s", endpoint, e.response.text)
                raise ExternalServiceException(
                    message=f"External API returned error {e.response.status_code}",
                    details={"endpoint": endpoint, "status_code": e.response.status_code},
                )
            except httpx.RequestError as e:
                logger.error("Request error connecting to %s: %s", endpoint, str(e))
                raise ExternalServiceException(
                    message="Failed to connect to external service",
                    details={"endpoint": endpoint, "error": str(e)},
                )

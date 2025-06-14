import httpx
import logging
from typing import List, Optional
from api.config.settings import settings
from api.logging.logger import log_request  # <-- usando seu logger estruturado

logger = logging.getLogger(__name__)

BASE_URL = "https://api.thecatapi.com/v1"
HEADERS = {"x-api-key": settings.cat_api_key}

async def fetch_from_api(endpoint: str, params: dict = None, trace_id: str = "no-trace") -> Optional[List[dict]]:
    url = f"{BASE_URL}/{endpoint}"
    method = "GET"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=HEADERS, params=params)
            if response.status_code == 200:
                log_request(logging.INFO, method, endpoint, trace_id, f"Fetched {endpoint} successfully.")
                return response.json()
            else:
                log_request(logging.WARNING, method, endpoint, trace_id, f"Failed to fetch {endpoint}: {response.status_code} - {response.text}")
    except Exception as e:
        log_request(logging.ERROR, method, endpoint, trace_id, f"Exception while fetching {endpoint}: {e}")
    return None

async def get_all_breeds(trace_id: str = "no-trace") -> Optional[List[dict]]:
    return await fetch_from_api("breeds", trace_id=trace_id)

async def get_images_by_breed_name(breed_name: str, limit: int = 3, trace_id: str = "no-trace") -> Optional[List[str]]:
    breeds = await get_all_breeds(trace_id)
    if breeds is None:
        return None

    breed = next((b for b in breeds if b.get("name", "").lower() == breed_name.lower()), None)
    if not breed:
        log_request(logging.INFO, "GET", "breeds", trace_id, f"No breed found for name: {breed_name}")
        return None

    breed_id = breed.get("id")
    if not breed_id:
        return None

    params = {"limit": limit, "breed_ids": breed_id}
    data = await fetch_from_api("images/search", params=params, trace_id=trace_id)
    if data is None:
        return None

    return [item.get("url") for item in data if "url" in item]

async def get_all_categories(trace_id: str = "no-trace") -> Optional[List[dict]]:
    return await fetch_from_api("categories", trace_id=trace_id)

async def get_images_by_category_id(category_id: int, limit: int = 3, trace_id: str = "no-trace") -> Optional[List[str]]:
    params = {"limit": limit, "category_ids": category_id}
    data = await fetch_from_api("images/search", params=params, trace_id=trace_id)
    if data is None:
        return None
    return [item.get("url") for item in data if "url" in item]

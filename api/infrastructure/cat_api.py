import httpx
import logging
from typing import List, Optional
from api.config.settings import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://api.thecatapi.com/v1"
HEADERS = {"x-api-key": settings.cat_api_key}

async def fetch_from_api(endpoint: str, params: dict = None) -> Optional[List[dict]]:
    url = f"{BASE_URL}/{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=HEADERS, params=params)
            if response.status_code == 200:
                return response.json()
            logger.warning(f"Failed to fetch {endpoint}: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Exception while fetching {endpoint}: {e}")
    return None

async def get_all_breeds() -> Optional[List[dict]]:
    return await fetch_from_api("breeds")

async def get_images_by_breed_name(breed_name: str, limit: int = 3) -> Optional[List[str]]:
    # Primeiro, buscamos todas as raças para encontrar o ID da raça com base no nome
    breeds = await get_all_breeds()
    if breeds is None:
        return None

    # Procuramos a raça pelo nome informado (case insensitive)
    breed = next((b for b in breeds if b.get("name", "").lower() == breed_name.lower()), None)
    if not breed:
        return None

    breed_id = breed.get("id")
    if not breed_id:
        return None

    # Com o ID da raça, buscamos as imagens
    params = {"limit": limit, "breed_ids": breed_id}
    data = await fetch_from_api("images/search", params=params)
    if data is None:
        return None

    return [item.get("url") for item in data if "url" in item]

async def get_all_categories() -> Optional[List[dict]]:
    return await fetch_from_api("categories")

async def get_images_by_category_id(category_id: int, limit: int = 3) -> Optional[List[str]]:
    params = {"limit": limit, "category_ids": category_id}
    data = await fetch_from_api("images/search", params=params)
    if data is None:
        return None
    return [item.get("url") for item in data if "url" in item]


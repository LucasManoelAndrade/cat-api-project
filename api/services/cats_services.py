from typing import Optional, List
from api.infrastructure.cat_api import get_all_breeds, get_images_by_breed_name, get_all_categories, get_images_by_category_id

async def get_all_breeds_service() -> Optional[List[dict]]:
    return await get_all_breeds()

async def get_breeds_by_origin_service(origin: str) -> Optional[List[dict]]:
    breeds = await get_all_breeds()
    if breeds is None:
        return None
    return [b for b in breeds if b.get("origin", "").lower() == origin.lower()]

async def get_breeds_by_temperament_service(temperament: str) -> Optional[List[dict]]:
    breeds = await get_all_breeds()
    if breeds is None:
        return None
    return [b for b in breeds if temperament.lower() in b.get("temperament", "").lower()]

async def get_images_by_breed_name_service(breed_name: str, limit: int = 3) -> Optional[List[str]]:
    return await get_images_by_breed_name(breed_name, limit)

async def get_all_categories_service() -> Optional[List[dict]]:
    return await get_all_categories()

async def get_images_by_category_id_service(category_id: int, limit: int = 3) -> Optional[List[str]]:
    return await get_images_by_category_id(category_id, limit)

async def get_breed_by_name_service(name: str) -> Optional[dict]:
    breeds = await get_all_breeds()
    if breeds is None:
        return None

    for breed in breeds:
        if breed.get("name", "").lower() == name.lower():
            return breed

    return None

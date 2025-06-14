from fastapi import APIRouter, HTTPException
from typing import List, Optional
from api.services.cats_services import (
    get_all_breeds_service,
    get_breeds_by_origin_service,
    get_breeds_by_temperament_service,
    get_breed_by_name_service
)

router = APIRouter(prefix="/cats", tags=["Cats"])

@router.get("/breeds", response_model=Optional[List[dict]])
async def list_all_breeds():
    breeds = await get_all_breeds_service()
    if breeds is None:
        raise HTTPException(status_code=502, detail="Failed to fetch breeds from TheCatAPI")
    return breeds

@router.get("/breeds/origin/{origin}", response_model=Optional[List[dict]])
async def list_breeds_by_origin(origin: str):
    breeds = await get_breeds_by_origin_service(origin)
    if breeds is None:
        raise HTTPException(status_code=404, detail="No breeds found for this origin")
    return breeds

@router.get("/breeds/temperament/{temperament}", response_model=Optional[List[dict]])
async def list_breeds_by_temperament(temperament: str):
    breeds = await get_breeds_by_temperament_service(temperament)
    if breeds is None:
        raise HTTPException(status_code=404, detail="No breeds found with this temperament")
    return breeds

@router.get("/breeds/name/{name}", response_model=Optional[dict])
async def get_breed_by_name(name: str):
    breed = await get_breed_by_name_service(name)
    if breed is None:
        raise HTTPException(status_code=404, detail="Breed not found")
    return breed

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from api.routers import cats_routers
from fastapi import FastAPI

app = FastAPI()
app.include_router(cats_routers.router)

client = TestClient(app)

@pytest.mark.asyncio
@patch("api.routers.cats_routers.get_all_breeds_service", new_callable=AsyncMock)
async def test_list_all_breeds_success(mock_service):
    mock_service.return_value = [{"id": "abys", "name": "Abyssinian"}]

    response = client.get("/cats/breeds")
    assert response.status_code == 200
    assert response.json() == [{"id": "abys", "name": "Abyssinian"}]

@pytest.mark.asyncio
@patch("api.routers.cats_routers.get_all_breeds_service", new_callable=AsyncMock)
async def test_list_all_breeds_failure(mock_service):
    mock_service.return_value = None

    response = client.get("/cats/breeds")
    assert response.status_code == 502
    assert response.json() == {"detail": "Failed to fetch breeds from TheCatAPI"}

@pytest.mark.asyncio
@patch("api.routers.cats_routers.get_breeds_by_origin_service", new_callable=AsyncMock)
async def test_list_breeds_by_origin_success(mock_service):
    mock_service.return_value = [{"id": "abys", "origin": "Egypt"}]

    response = client.get("/cats/breeds/origin/Egypt")
    assert response.status_code == 200
    assert response.json() == [{"id": "abys", "origin": "Egypt"}]

@pytest.mark.asyncio
@patch("api.routers.cats_routers.get_breeds_by_origin_service", new_callable=AsyncMock)
async def test_list_breeds_by_origin_not_found(mock_service):
    mock_service.return_value = None

    response = client.get("/cats/breeds/origin/Unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "No breeds found for this origin"}

@pytest.mark.asyncio
@patch("api.routers.cats_routers.get_breeds_by_temperament_service", new_callable=AsyncMock)
async def test_list_breeds_by_temperament_success(mock_service):
    mock_service.return_value = [{"id": "abys", "temperament": "Active"}]

    response = client.get("/cats/breeds/temperament/Active")
    assert response.status_code == 200
    assert response.json() == [{"id": "abys", "temperament": "Active"}]

@pytest.mark.asyncio
@patch("api.routers.cats_routers.get_breeds_by_temperament_service", new_callable=AsyncMock)
async def test_list_breeds_by_temperament_not_found(mock_service):
    mock_service.return_value = None

    response = client.get("/cats/breeds/temperament/Unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "No breeds found with this temperament"}

@pytest.mark.asyncio
@patch("api.routers.cats_routers.get_breed_by_name_service", new_callable=AsyncMock)
async def test_get_breed_by_name_success(mock_service):
    mock_service.return_value = {"id": "abys", "name": "Abyssinian"}

    response = client.get("/cats/breeds/name/Abyssinian")
    assert response.status_code == 200
    assert response.json() == {"id": "abys", "name": "Abyssinian"}

@pytest.mark.asyncio
@patch("api.routers.cats_routers.get_breed_by_name_service", new_callable=AsyncMock)
async def test_get_breed_by_name_not_found(mock_service):
    mock_service.return_value = None

    response = client.get("/cats/breeds/name/Unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "Breed not found"}

import pytest
from unittest.mock import patch

from api.services import cats_services as service


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_breeds", return_value=[{"id": "abys", "name": "Abyssinian"}])
async def test_get_all_breeds_service(mock_get_all_breeds):
    result = await service.get_all_breeds_service()
    assert result == [{"id": "abys", "name": "Abyssinian"}]


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_breeds")
async def test_get_breeds_by_origin_service(mock_get_all_breeds):
    mock_get_all_breeds.return_value = [{"name": "Breed1", "origin": "Brazil"}]
    result = await service.get_breeds_by_origin_service("brazil")
    assert result == [{"name": "Breed1", "origin": "Brazil"}]


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_breeds", return_value=None)
async def test_get_breeds_by_origin_service_none(mock_get_all_breeds):
    result = await service.get_breeds_by_origin_service("brazil")
    assert result is None


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_breeds")
async def test_get_breeds_by_temperament_service(mock_get_all_breeds):
    mock_get_all_breeds.return_value = [{"name": "Breed1", "temperament": "Playful, Active"}]
    result = await service.get_breeds_by_temperament_service("playful")
    assert result == [{"name": "Breed1", "temperament": "Playful, Active"}]


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_breeds", return_value=None)
async def test_get_breeds_by_temperament_service_none(mock_get_all_breeds):
    result = await service.get_breeds_by_temperament_service("playful")
    assert result is None


@pytest.mark.asyncio
@patch("api.services.cats_services.get_images_by_breed_name")
async def test_get_images_by_breed_name_service(mock_get_images_by_breed_name):
    mock_get_images_by_breed_name.return_value = ["img1.jpg", "img2.jpg"]
    result = await service.get_images_by_breed_name_service("Abyssinian")
    assert result == ["img1.jpg", "img2.jpg"]


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_categories")
async def test_get_all_categories_service(mock_get_all_categories):
    mock_get_all_categories.return_value = [{"id": 1, "name": "funny"}]
    result = await service.get_all_categories_service()
    assert result == [{"id": 1, "name": "funny"}]


@pytest.mark.asyncio
@patch("api.services.cats_services.get_images_by_category_id")
async def test_get_images_by_category_id_service(mock_get_images_by_category_id):
    mock_get_images_by_category_id.return_value = ["img1.jpg"]
    result = await service.get_images_by_category_id_service(1)
    assert result == ["img1.jpg"]


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_breeds")
async def test_get_breed_by_name_service(mock_get_all_breeds):
    mock_get_all_breeds.return_value = [{"name": "Siamese"}]
    result = await service.get_breed_by_name_service("siamese")
    assert result == {"name": "Siamese"}


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_breeds", return_value=None)
async def test_get_breed_by_name_service_none(mock_get_all_breeds):
    result = await service.get_breed_by_name_service("siamese")
    assert result is None


@pytest.mark.asyncio
@patch("api.services.cats_services.get_all_breeds")
async def test_get_breed_by_name_service_not_found(mock_get_all_breeds):
    mock_get_all_breeds.return_value = [{"name": "Abyssinian"}]
    result = await service.get_breed_by_name_service("siamese")
    assert result is None

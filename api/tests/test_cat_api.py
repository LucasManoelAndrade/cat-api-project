import pytest
from unittest.mock import patch, Mock
from api.infrastructure import cat_api

@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.httpx.AsyncClient.get")
async def test_get_all_breeds(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "abys", "name": "Abyssinian"}]
    mock_get.return_value = mock_response

    result = await cat_api.get_all_breeds()
    assert result == [{"id": "abys", "name": "Abyssinian"}]

@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_breed_name(mock_fetch):
    # Simula resposta de get_all_breeds
    mock_fetch.side_effect = [
        [{"id": "abys", "name": "Abyssinian"}],  # breeds
        [{"url": "https://example.com/image.jpg"}]  # images
    ]

    result = await cat_api.get_images_by_breed_name("Abyssinian")
    assert result == ["https://example.com/image.jpg"]

@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_breed_name_not_found(mock_fetch):
    mock_fetch.side_effect = [
        [{"id": "abys", "name": "Abyssinian"}],  # breeds
    ]

    result = await cat_api.get_images_by_breed_name("Nonexistent")
    assert result is None

@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_all_categories(mock_fetch):
    mock_fetch.return_value = [{"id": 1, "name": "Funny"}]
    result = await cat_api.get_all_categories()
    assert result == [{"id": 1, "name": "Funny"}]

@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_category_id(mock_fetch):
    mock_fetch.return_value = [{"url": "https://example.com/cat.jpg"}]
    result = await cat_api.get_images_by_category_id(1)
    assert result == ["https://example.com/cat.jpg"]

@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.httpx.AsyncClient.get")
async def test_fetch_from_api_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "abys", "name": "Abyssinian"}]
    mock_get.return_value = mock_response

    result = await cat_api.fetch_from_api("breeds")
    assert result == [{"id": "abys", "name": "Abyssinian"}]

@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.httpx.AsyncClient.get")
async def test_fetch_from_api_failure(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.text = "Not Found"
    result = await cat_api.fetch_from_api("breeds")
    assert result is None

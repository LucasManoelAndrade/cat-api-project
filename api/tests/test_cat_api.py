import pytest
import logging
from unittest.mock import patch, Mock
from api.infrastructure import cat_api


# Testa constantes do módulo (linhas 19-20)
def test_module_level_constants():
    from api.infrastructure import cat_api
    assert cat_api.BASE_URL == "https://api.thecatapi.com/v1"
    assert "x-api-key" in cat_api.HEADERS


# fetch_from_api: response status != 200 (linhas 23-24)
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.httpx.AsyncClient.get")
@patch("api.infrastructure.cat_api.log_request")
async def test_fetch_from_api_status_not_200(mock_log_request, mock_get):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response

    result = await cat_api.fetch_from_api("breeds")
    assert result is None
    mock_log_request.assert_called_with(
        logging.WARNING, "GET", "breeds", "no-trace", "Failed to fetch breeds: 500 - Internal Server Error"
    )


# fetch_from_api: exceção lançada (linha 33)
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.httpx.AsyncClient.get", side_effect=Exception("connection error"))
@patch("api.infrastructure.cat_api.log_request")
async def test_fetch_from_api_raises_exception(mock_log_request, mock_get):
    result = await cat_api.fetch_from_api("breeds")
    assert result is None
    mock_log_request.assert_called()
    assert "Exception while fetching breeds: connection error" in mock_log_request.call_args[0][4]


# get_images_by_breed_name: nome não encontrado (linha 42)
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
@patch("api.infrastructure.cat_api.log_request")
async def test_get_images_by_breed_name_logs_not_found(mock_log_request, mock_fetch):
    mock_fetch.return_value = [{"id": "abys", "name": "Abyssinian"}]

    result = await cat_api.get_images_by_breed_name("Persian")
    assert result is None
    mock_log_request.assert_called_with(
        logging.INFO, "GET", "breeds", "no-trace", "No breed found for name: Persian"
    )


# get_images_by_breed_name: breed sem id (linha 33 e 47)
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_breed_name_breed_no_id(mock_fetch):
    mock_fetch.side_effect = [
        [{"name": "Abyssinian"}],  # breed without id
    ]

    result = await cat_api.get_images_by_breed_name("Abyssinian")
    assert result is None


# get_images_by_breed_name: fetch retorna None para imagens (linha 52)
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_breed_name_fetch_returns_none(mock_fetch):
    mock_fetch.side_effect = [
        [{"id": "abys", "name": "Abyssinian"}],  # get_all_breeds
        None  # fetch_from_api("images/search")
    ]
    result = await cat_api.get_images_by_breed_name("Abyssinian")
    assert result is None


# get_images_by_breed_name: retorna só URLs válidas (linha 52)
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_breed_name_with_url(mock_fetch):
    mock_fetch.side_effect = [
        [{"id": "abys", "name": "Abyssinian"}],
        [{"url": "https://example.com/img1.jpg"}, {"other": "x"}]
    ]
    result = await cat_api.get_images_by_breed_name("Abyssinian")
    assert result == ["https://example.com/img1.jpg"]


# get_images_by_category_id: ignora itens sem "url" (linha 58)
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_category_id_skips_items_without_url(mock_fetch):
    mock_fetch.return_value = [{"url": "https://cat1.jpg"}, {"no_url": "skip_this"}]

    result = await cat_api.get_images_by_category_id(1)
    assert result == ["https://cat1.jpg"]


# get_images_by_category_id: retorna só URLs válidas (linha 58)
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_category_id_partial_urls(mock_fetch):
    mock_fetch.return_value = [{"url": "https://example.com/img.jpg"}, {"x": "no-url"}]
    result = await cat_api.get_images_by_category_id(99)
    assert result == ["https://example.com/img.jpg"]


# Outros testes existentes para endpoints básicos e fetch
@pytest.mark.asyncio
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_all_breeds(mock_fetch):
    mock_fetch.return_value = [{"id": "abys", "name": "Abyssinian"}]
    result = await cat_api.get_all_breeds()
    assert result == [{"id": "abys", "name": "Abyssinian"}]

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
@patch("api.infrastructure.cat_api.fetch_from_api")
async def test_get_images_by_breed_name(mock_fetch):
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

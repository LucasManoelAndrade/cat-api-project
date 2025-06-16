import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from api.scripts.populate_db import (
    clear_database,
    populate_breeds,
    populate_images,
    populate_category_images,
    populate_database,
)

# Testa se clear_database chama os deletes e commit corretamente
def test_clear_database():
    session = MagicMock()

    clear_database(session)

    assert session.query.return_value.delete.call_count == 3
    session.commit.assert_called_once()

# Testa se populate_breeds adiciona e comita corretamente
def test_populate_breeds():
    session = MagicMock()
    breeds_data = [
        {"id": "abys", "name": "Abyssinian", "origin": "Egypt", "temperament": "Active", "description": "Desc"},
    ]

    populate_breeds(session, breeds_data)

    session.add.assert_called_once()
    session.commit.assert_called_once()

# Testa se populate_images adiciona e comita corretamente
def test_populate_images():
    session = MagicMock()
    breeds_data = [
        {"id": "abys", "image": {"url": "http://example.com/image.jpg"}},
        {"id": "beng", "image": None},  # deve ser ignorado
    ]

    populate_images(session, breeds_data)

    session.add.assert_called_once()
    session.commit.assert_called_once()

# Testa se populate_category_images insere corretamente
@pytest.mark.asyncio
@patch("api.scripts.populate_db.get_images_by_category_id", new_callable=AsyncMock)
async def test_populate_category_images(mock_get_images):
    session = MagicMock()
    categories = [{"id": 1, "name": "cute"}]
    mock_get_images.return_value = ["http://img1", "http://img2"]

    await populate_category_images(session, categories)

    assert session.add.call_count == 2
    session.commit.assert_called_once()

# Testa se populate_database executa o fluxo completo sem erros
@pytest.mark.asyncio
@patch("api.scripts.populate_db.get_all_breeds", new_callable=AsyncMock)
@patch("api.scripts.populate_db.get_all_categories", new_callable=AsyncMock)
@patch("api.scripts.populate_db.populate_category_images", new_callable=AsyncMock)
@patch("api.scripts.populate_db.populate_images")
@patch("api.scripts.populate_db.populate_breeds")
@patch("api.scripts.populate_db.clear_database")
@patch("api.scripts.populate_db.SessionLocal")
async def test_populate_database(
    mock_sessionlocal,
    mock_clear,
    mock_breeds,
    mock_images,
    mock_populate_categories,
    mock_get_categories,
    mock_get_breeds
):
    session = MagicMock()
    mock_sessionlocal.return_value = session
    mock_get_breeds.return_value = [{"id": "abys", "name": "Abyssinian"}]
    mock_get_categories.return_value = [{"id": 1, "name": "cute"}]

    await populate_database()

    mock_clear.assert_called_once_with(session)
    mock_breeds.assert_called_once()
    mock_images.assert_called_once()
    mock_populate_categories.assert_awaited_once()
    session.close.assert_called_once()

@pytest.mark.asyncio
async def test_populate_category_images_handles_exception():
    session = MagicMock()
    categories = [{"id": 123, "name": "funny"}]

    with patch("api.scripts.populate_db.get_images_by_category_id", side_effect=Exception("fail")) as mock_images:
        await populate_category_images(session, categories)
        session.add.assert_not_called()  # Nada deve ser adicionado por causa da exceção
        session.commit.assert_called_once()
        mock_images.assert_called_once()


@pytest.mark.asyncio
@patch("api.scripts.populate_db.get_all_breeds", new_callable=AsyncMock)
@patch("api.scripts.populate_db.get_all_categories", new_callable=AsyncMock)
async def test_populate_database_handles_empty_data(mock_get_categories, mock_get_breeds):
    mock_get_breeds.return_value = []
    mock_get_categories.return_value = []

    with patch("api.scripts.populate_db.clear_database"), \
         patch("api.scripts.populate_db.populate_breeds"), \
         patch("api.scripts.populate_db.populate_images"), \
         patch("api.scripts.populate_db.populate_category_images"):

        await populate_database()
        mock_get_breeds.assert_awaited_once()
        mock_get_categories.assert_awaited_once()


@pytest.mark.asyncio
@patch("api.scripts.populate_db.get_all_breeds", new_callable=AsyncMock)
@patch("api.scripts.populate_db.get_all_categories", new_callable=AsyncMock)
async def test_populate_database_handles_general_exception(mock_get_categories, mock_get_breeds):
    mock_get_breeds.side_effect = Exception("fail")
    mock_get_categories.return_value = []

    with patch("api.scripts.populate_db.clear_database"), \
         patch("api.scripts.populate_db.logger.error") as mock_logger:

        await populate_database()
        mock_logger.assert_any_call(
            "Error populating database: fail",
            extra={"method": "populate", "endpoint": "error", "trace_id": None}
        )

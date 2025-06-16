# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import patch, AsyncMock, MagicMock
# from api.main import app, lifespan

# client = TestClient(app)

# def test_health_check():
#     """Teste se a rota /healthz responde com status 200 e corpo esperado."""
#     response = client.get("/healthz")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}

# @pytest.mark.asyncio
# @patch("api.scripts.populate_db.populate_database", new_callable=AsyncMock)
# async def test_lifespan_startup_called(mock_populate):
#     """Testa se populate_database() é chamado no startup do lifespan."""
#     async with lifespan(app):
#         pass
#     assert mock_populate.await_count == 1

# @patch("api.metrics.prometheus.REQUEST_LATENCY")
# @patch("api.metrics.prometheus.REQUEST_COUNTER")
# @patch("api.metrics.prometheus.ERROR_COUNTER")
# def test_middleware_metrics(mock_error_counter, mock_request_counter, mock_latency):
#     """Testa se o middleware Prometheus chama os métodos corretos para métricas."""

#     dummy_context = MagicMock()
#     dummy_context.__enter__.return_value = None
#     dummy_context.__exit__.return_value = None
#     mock_latency.labels.return_value.time.return_value = dummy_context

#     mock_request_counter.labels.return_value.inc.return_value = None
#     mock_error_counter.labels.return_value.inc.return_value = None

#     response = client.get("/healthz")

#     assert response.status_code == 200

#     mock_latency.labels.assert_called_once_with(method="GET", endpoint="/healthz")
#     mock_latency.labels.return_value.time.assert_called_once()
#     mock_request_counter.labels.assert_called_once_with(method="GET", endpoint="/healthz")
#     mock_request_counter.labels.return_value.inc.assert_called_once()

#     mock_error_counter.labels.assert_not_called()

# def test_router_included():
#     """Testa se a rota /cats/breeds está disponível (status 200 ou 502)."""
#     response = client.get("/cats/breeds")
#     assert response.status_code in (200, 502)

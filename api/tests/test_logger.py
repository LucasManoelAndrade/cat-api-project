import logging
import pytest
from unittest.mock import patch, MagicMock
from api.logging import logger as logger_module

def test_configure_logging_adds_handlers_to_uvicorn_loggers():
    # Antes da configuração, verificamos os handlers existentes
    uvicorn_logger = logging.getLogger("uvicorn")
    original_handlers = uvicorn_logger.handlers.copy()

    try:
        logger_module.configure_logging()
        for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
            uv_logger = logging.getLogger(name)
            # Deve ter pelo menos os handlers do arquivo e console adicionados (2 handlers)
            handlers = uv_logger.handlers
            assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in handlers)
            assert any(isinstance(h, logging.StreamHandler) for h in handlers)
            assert uv_logger.level == logging.INFO
    finally:
        # Restaurar handlers originais para evitar side effects em outros testes
        for name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
            uv_logger = logging.getLogger(name)
            uv_logger.handlers = original_handlers

@patch.object(logger_module.logger, 'log')
def test_log_request_calls_logger_log(mock_log):
    level = logging.INFO
    method = "GET"
    endpoint = "/cats"
    trace_id = "1234"
    message = "Test message"

    logger_module.log_request(level, method, endpoint, trace_id, message)

    mock_log.assert_called_once_with(level, message, extra={
        'method': method,
        'endpoint': endpoint,
        'trace_id': trace_id
    })

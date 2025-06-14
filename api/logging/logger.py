import logging
import os
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

LOG_DIR = "/var/log/cat-api"
LOG_FILE = os.path.join(LOG_DIR, "cat-api.log")

os.makedirs(LOG_DIR, exist_ok=True)

# Lista dos campos padrão e adicionais
log_fields = [
    'asctime', 'levelname', 'name', 'message',
    'method', 'endpoint', 'trace_id'
]

# Usar placeholders compatíveis com o estilo de formatação do jsonlogger
log_format = ' '.join(f'%({field})s' for field in log_fields)

# Configura o formatador JSON
json_formatter = jsonlogger.JsonFormatter(log_format)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(json_formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

# Logger principal
logger = logging.getLogger("cat-api")

def configure_logging():
    # Enviar logs do uvicorn também para o mesmo arquivo
    for uvicorn_logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        uv_logger = logging.getLogger(uvicorn_logger_name)
        uv_logger.setLevel(logging.INFO)
        uv_logger.addHandler(file_handler)
        uv_logger.addHandler(console_handler)

def log_request(level, method, endpoint, trace_id, message):
    logger.log(level, message, extra={
        'method': method,
        'endpoint': endpoint,
        'trace_id': trace_id
    })

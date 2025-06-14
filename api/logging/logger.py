import logging
import os
from logging.handlers import RotatingFileHandler

# Novo diretório compartilhado entre o container da API e o Promtail
LOG_DIR = "/var/log/cat-api"
LOG_FILE = os.path.join(LOG_DIR, "cat-api.log")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Aplica ambos os handlers no logger raiz
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

def configure_logging():
    # Adiciona também aos loggers do Uvicorn (para logs de acesso e erro)
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.addHandler(file_handler)

    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_error_logger.addHandler(file_handler)

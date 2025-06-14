FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependência
COPY requirements.txt ./

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o container
COPY api/ ./api

# Define a variável de ambiente para FastAPI
ENV PYTHONUNBUFFERED=1

# Comando padrão para iniciar a aplicação
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
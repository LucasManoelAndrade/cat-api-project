from prometheus_client import Counter, Histogram

# Contador de requisições por rota e método
REQUEST_COUNTER = Counter(
    'cat_api_requests_total',
    'Número total de requisições por método e endpoint',
    ['method', 'endpoint']
)

# Contador de erros por rota e método
ERROR_COUNTER = Counter(
    'cat_api_errors_total',
    'Número total de erros por método e endpoint',
    ['method', 'endpoint', 'status_code']
)

# Histograma de latência por rota e método
REQUEST_LATENCY = Histogram(
    'cat_api_request_latency_seconds',
    'Latência da requisição em segundos por método e endpoint',
    ['method', 'endpoint']
)

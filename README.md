# Documentação do Projeto - Cat API

## a. Documentação do Projeto

Este projeto consiste em uma API que consome dados da TheCatAPI e os armazena em um banco de dados local. Além disso, a aplicação expõe esses dados via endpoints RESTful, permitindo a consulta por nome, origem e temperamento das raças de gatos. O projeto também inclui um ecossistema completo de observabilidade com Prometheus, Grafana, Loki, e métricas customizadas via middleware.

## b. Documentação das APIs

### Endpoints disponíveis

- `GET /cats/breeds`: Lista todas as raças disponíveis.
- `GET /cats/breeds/origin/{origin}`: Lista raças por origem.
- `GET /cats/breeds/temperament/{temperament}`: Lista raças por temperamento.
- `GET /cats/breeds/name/{name}`: Retorna informações detalhadas sobre uma raça específica.

Em caso de erro, os endpoints retornam os seguintes status:
- 404: Nenhuma raça encontrada para o critério informado.
- 502: Falha ao buscar dados da API externa.

## c. Documentação de Arquitetura

### Camadas principais

- **Routers**: Define as rotas e os contratos da API.
- **Services**: Contém a lógica de negócio e orquestra chamadas à camada de infraestrutura.
- **Infrastructure**: Faz a comunicação com a TheCatAPI.
- **Models**: Define os modelos de banco de dados com SQLAlchemy.
- **Database**: Conexão com o banco e configuração da engine.
- **Observabilidade**: Middleware Prometheus + Grafana + Loki.
- **Testes**: Divididos em unitários e de performance com Locust.

### Tecnologias utilizadas

- FastAPI
- SQLAlchemy
- SQLite (local)
- Prometheus, Grafana, Loki, Promtail
- Pytest, Locust

## d. Como subir uma cópia localmente

### Pré-requisitos

- Docker e Docker Compose
- Make (opcional)
- Python 3.11 (caso queira rodar localmente sem container)

### Subindo com Docker Compose

```bash
cd docker
docker compose up --build
```

A API estará disponível em: [http://localhost:8000](http://localhost:8000)

Grafana: [http://localhost:3000](http://localhost:3000)  
Usuário: admin  
Senha: Salvando@2025

Prometheus: [http://localhost:9090](http://localhost:9090)  
Consul: [http://localhost:8500](http://localhost:8500)

### Rodando testes unitários

```bash
pytest --cov=api
```

### Rodando testes de performance

```bash
cd api/tests/test_performance
locust -f locustfile.py
```

---

**Autor:** Lucas Manoel  
**Ano:** 2025
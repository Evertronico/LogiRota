# LogiRota MVP

Roteirização de entregas construída em Estrutura de Dados II: pontos de entrega, malha viária como grafo e, a partir do Projeto Final, persistência em banco de dados.

Branch de entrega: `Daniel-Soares-11032410168`. A documentação de cada semana está em [`docs/`](docs/).

## Como rodar

### Opção 1: PostgreSQL no Docker (recomendado)

Requer Docker Desktop (Windows ou macOS).

```bash
docker compose up -d db
docker compose run --rm app
docker compose run --rm app --pedido "Oficina Safira"
docker compose run --rm app
```

A segunda execução cadastra um pedido. A terceira mostra que ele continua lá. Os dados ficam no volume `logirota_dados` e sobrevivem a `docker compose down` e `up`. Só `docker compose down -v` apaga tudo.

### Opção 2: SQLite, sem Docker

Usa apenas a biblioteca padrão do Python e grava em `logirota.db`.

```bash
python main.py
python main.py --pedido "Oficina Safira"
python main.py
```

No Windows use `python`, e no macOS/Linux `python3`.

### Opção 3: Python local apontando para o Postgres do Docker

```bash
pip install -r requirements.txt
export DATABASE_URL=postgresql://logirota:logirota@localhost:5432/logirota
python3 main.py
```

No Windows (PowerShell): `$env:DATABASE_URL="postgresql://logirota:logirota@localhost:5432/logirota"`.

## Estrutura

```
main.py                 ponto de entrada: lê a malha e os pedidos do banco
docker-compose.yml      PostgreSQL 16 + container da aplicação
Dockerfile              imagem da aplicação
requirements.txt        psycopg (só para o PostgreSQL)
logirota/
  banco.py              Semana 1: camada de persistência (Postgres ou SQLite)
  ponto.py, grafo.py    domínio das aulas, sem alteração
  busca.py, fila.py, pilha.py, ...
docs/
  semana-1/             o que foi implementado na Semana 1 (PDF)
```

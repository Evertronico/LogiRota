"""
Camada de persistência do LogiRota — Semana 1.

Parte do banco.py fornecido na apostila (mesmas quatro tabelas, mesmo
contrato) e acrescenta um segundo motor de banco:

  PostgreSQL  quando a variável de ambiente DATABASE_URL está definida —
              o banco roda num container Docker (docker-compose.yml) e
              aceita várias conexões simultâneas, simulando uma aplicação
              que recebe múltiplas requisições.
  SQLite      quando DATABASE_URL não está definida — arquivo único
              logirota.db, biblioteca padrão, nenhuma instalação extra.

O resto do programa não sabe qual motor está em uso: cada função abre e
fecha a própria conexão e devolve dados simples (tuplas, listas). Este
módulo não importa ponto.py nem grafo.py — converter tupla em Ponto é
responsabilidade de quem chama, não da persistência.
"""

import os
import sqlite3
from contextlib import contextmanager

CAMINHO_BANCO = "logirota.db"
URL_POSTGRES = os.environ.get("DATABASE_URL")

SCHEMA_SQLITE = """
CREATE TABLE IF NOT EXISTS pontos (
    nome TEXT PRIMARY KEY,
    bairro TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS ruas (
    origem TEXT NOT NULL REFERENCES pontos(nome),
    destino TEXT NOT NULL REFERENCES pontos(nome),
    PRIMARY KEY (origem, destino)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destino TEXT NOT NULL REFERENCES pontos(nome),
    status TEXT NOT NULL DEFAULT 'pendente'
);

CREATE TABLE IF NOT EXISTS rotas_calculadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origem TEXT NOT NULL,
    sequencia TEXT NOT NULL,
    distancia_total REAL NOT NULL,
    criada_em TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

# Mesmas tabelas e colunas; muda só o que é sintaxe de cada motor
# (SERIAL no lugar de AUTOINCREMENT, TIMESTAMP no lugar de TEXT).
SCHEMA_POSTGRES = """
CREATE TABLE IF NOT EXISTS pontos (
    nome TEXT PRIMARY KEY,
    bairro TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS ruas (
    origem TEXT NOT NULL REFERENCES pontos(nome),
    destino TEXT NOT NULL REFERENCES pontos(nome),
    PRIMARY KEY (origem, destino)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    destino TEXT NOT NULL REFERENCES pontos(nome),
    status TEXT NOT NULL DEFAULT 'pendente'
);

CREATE TABLE IF NOT EXISTS rotas_calculadas (
    id SERIAL PRIMARY KEY,
    origem TEXT NOT NULL,
    sequencia TEXT NOT NULL,
    distancia_total REAL NOT NULL,
    criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def usando_postgres():
    return URL_POSTGRES is not None


def descrever_banco():
    """Texto curto dizendo onde os dados estão sendo gravados."""
    if usando_postgres():
        return "PostgreSQL (Docker)"
    return f"SQLite ({CAMINHO_BANCO})"


@contextmanager
def conectar():
    """Abre uma conexão, confirma (commit) ao final do bloco with e
    sempre fecha — mesmo se der erro no meio, nenhuma conexão fica
    aberta travando o banco."""
    if usando_postgres():
        import psycopg  # só é necessário quando o Postgres está em uso

        conexao = psycopg.connect(URL_POSTGRES)
    else:
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.execute("PRAGMA foreign_keys = ON")
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def _sql(comando):
    """As consultas são escritas com '?' (SQLite); o driver do Postgres
    espera '%s'. A troca acontece num único lugar."""
    if usando_postgres():
        return comando.replace("?", "%s")
    return comando


def _executar(conexao, comando, parametros=()):
    return conexao.execute(_sql(comando), parametros)


def inicializar():
    """Cria as tabelas se nao existirem. Chamar uma vez, no
    inicio do programa, antes de qualquer outra operacao."""
    with conectar() as conexao:
        if usando_postgres():
            conexao.execute(SCHEMA_POSTGRES)
        else:
            conexao.executescript(SCHEMA_SQLITE)


# --- inserção -----------------------------------------------------------
# ON CONFLICT DO NOTHING (aceito pelos dois motores) torna a gravação
# idempotente: rodar o programa duas vezes não duplica pontos nem ruas.

def salvar_ponto(nome, bairro, x, y):
    with conectar() as conexao:
        _executar(
            conexao,
            "INSERT INTO pontos (nome, bairro, x, y) VALUES (?, ?, ?, ?) "
            "ON CONFLICT (nome) DO NOTHING",
            (nome, bairro, x, y),
        )


def salvar_rua(origem, destino):
    with conectar() as conexao:
        _executar(
            conexao,
            "INSERT INTO ruas (origem, destino) VALUES (?, ?) "
            "ON CONFLICT (origem, destino) DO NOTHING",
            (origem, destino),
        )


def salvar_pedido(destino):
    """Cadastra um pedido pendente e devolve o id gerado pelo banco."""
    with conectar() as conexao:
        cursor = _executar(
            conexao,
            "INSERT INTO pedidos (destino) VALUES (?) RETURNING id",
            (destino,),
        )
        return cursor.fetchone()[0]


# --- consulta -----------------------------------------------------------

def listar_pontos():
    """Lista de tuplas (nome, bairro, x, y)."""
    with conectar() as conexao:
        return _executar(
            conexao, "SELECT nome, bairro, x, y FROM pontos ORDER BY nome"
        ).fetchall()


def listar_ruas():
    """Lista de tuplas (origem, destino)."""
    with conectar() as conexao:
        return _executar(
            conexao, "SELECT origem, destino FROM ruas ORDER BY origem, destino"
        ).fetchall()


def listar_pedidos_pendentes():
    """Lista de tuplas (id, destino, status), na ordem de chegada."""
    with conectar() as conexao:
        return _executar(
            conexao,
            "SELECT id, destino, status FROM pedidos "
            "WHERE status = 'pendente' ORDER BY id",
        ).fetchall()


def banco_vazio():
    """True se ainda não há nenhum ponto cadastrado — usado para popular
    a malha inicial só na primeira execução."""
    with conectar() as conexao:
        total = _executar(conexao, "SELECT COUNT(*) FROM pontos").fetchone()[0]
        return total == 0

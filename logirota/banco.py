"""
Camada de persistencia do LogiRota - fornecida pronta e ampliada na Semana 1.
"""

import sqlite3

CAMINHO_BANCO = "logirota.db"

SCHEMA = """
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


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar():
    """Cria as tabelas se nao existirem. Chamar uma vez no inicio."""
    with conectar() as conexao:
        conexao.executescript(SCHEMA)


def salvar_ponto(ponto):
    with conectar() as conexao:
        conexao.execute(
            "INSERT INTO pontos (nome, bairro, x, y) VALUES (?, ?, ?, ?)",
            (ponto.nome, ponto.bairro, ponto._x, ponto._y),
        )


def salvar_rua(origem, destino):
    with conectar() as conexao:
        conexao.execute(
            "INSERT INTO ruas (origem, destino) VALUES (?, ?)",
            (origem, destino),
        )


def salvar_pedido(destino):
    with conectar() as conexao:
        conexao.execute(
            "INSERT INTO pedidos (destino) VALUES (?)",
            (destino,),
        )


def listar_pontos():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT nome, bairro, x, y FROM pontos ORDER BY rowid"
        ).fetchall()


def listar_ruas():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT origem, destino FROM ruas ORDER BY rowid"
        ).fetchall()


def listar_pedidos_pendentes():
    with conectar() as conexao:
        return conexao.execute(
            "SELECT id, destino, status FROM pedidos "
            "WHERE status = 'pendente' ORDER BY id"
        ).fetchall()

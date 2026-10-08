"""
Camada de persistência do LogiRota - fornecida pronta.
"""

import sqlite3
from contextlib import closing

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
    """Cria as tabelas se nao existirem. Chamar uma vez, no
    inicio do programa, antes de qualquer outra operacao."""
    # with sozinho so faz commit, nao fecha; closing e quem fecha
    with closing(conectar()) as conexao, conexao:
        conexao.executescript(SCHEMA)


# ---------- inserts ----------
# padrao: closing fecha a conexao, "conexao" no with faz commit/rollback
# or ignore: se ja existe (chave repetida) pula em vez de dar erro

def salvar_ponto(ponto):
    # _x/_y porque Ponto ainda nao tem x/y publicos
    with closing(conectar()) as conexao, conexao:
        conexao.execute(
            "INSERT OR IGNORE INTO pontos (nome, bairro, x, y) VALUES (?, ?, ?, ?)",
            (ponto.nome, ponto.bairro, ponto._x, ponto._y),
        )


def salvar_rua(origem, destino):
    with closing(conectar()) as conexao, conexao:
        conexao.execute(
            "INSERT OR IGNORE INTO ruas (origem, destino) VALUES (?, ?)",
            (origem, destino),
        )


def salvar_pedido(destino):
    # status entra como 'pendente' pelo default da tabela
    with closing(conectar()) as conexao, conexao:
        cursor = conexao.execute(
            "INSERT INTO pedidos (destino) VALUES (?)", (destino,)
        )
        return cursor.lastrowid


# ---------- consultas ----------
# devolvem tuplas simples; virar Ponto e problema do main/dominio
# order by rowid = ordem em que foi inserido (importa pra ordem do grafo)

def listar_pontos():
    with closing(conectar()) as conexao:
        return conexao.execute(
            "SELECT nome, bairro, x, y FROM pontos ORDER BY rowid"
        ).fetchall()


def listar_ruas():
    with closing(conectar()) as conexao:
        return conexao.execute(
            "SELECT origem, destino FROM ruas ORDER BY rowid"
        ).fetchall()


def listar_pedidos_pendentes():
    with closing(conectar()) as conexao:
        return conexao.execute(
            "SELECT id, destino FROM pedidos WHERE status = 'pendente' ORDER BY id"
        ).fetchall()
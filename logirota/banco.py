import sqlite3

CAMINHO_BANCO = "logirota.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS pontos (
    nome   TEXT PRIMARY KEY,
    bairro TEXT NOT NULL,
    x      REAL NOT NULL,
    y      REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS ruas (
    origem  TEXT NOT NULL REFERENCES pontos(nome),
    destino TEXT NOT NULL REFERENCES pontos(nome),
    PRIMARY KEY (origem, destino)
);
CREATE TABLE IF NOT EXISTS pedidos (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    destino TEXT NOT NULL REFERENCES pontos(nome),
    status  TEXT NOT NULL DEFAULT 'pendente'
);
CREATE TABLE IF NOT EXISTS rotas_calculadas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    origem          TEXT NOT NULL,
    sequencia       TEXT NOT NULL,
    distancia_total REAL NOT NULL,
    criada_em       TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar():
    conexao = conectar()
    try:
        with conexao:
            conexao.executescript(SCHEMA)
    finally:
        conexao.close()


def _executar(sql, parametros=()):
    conexao = conectar()
    try:
        with conexao:  # commit/rollback automatico
            conexao.execute(sql, parametros)
    finally:
        conexao.close()


def _consultar(sql, parametros=()):
    conexao = conectar()
    try:
        return conexao.execute(sql, parametros).fetchall()
    finally:
        conexao.close()


def salvar_ponto(nome, bairro, x, y):
    _executar(
        "INSERT OR IGNORE INTO pontos (nome, bairro, x, y) VALUES (?, ?, ?, ?)",
        (nome, bairro, x, y),
    )


def salvar_rua(origem, destino):
    _executar(
        "INSERT OR IGNORE INTO ruas (origem, destino) VALUES (?, ?)",
        (origem, destino),
    )


def salvar_pedido(destino):
    _executar("INSERT INTO pedidos (destino) VALUES (?)", (destino,))

def listar_pontos():
    return _consultar("SELECT nome, bairro, x, y FROM pontos ORDER BY nome")

def listar_ruas():
    return _consultar("SELECT origem, destino FROM ruas ORDER BY origem, destino")


def listar_pedidos_pendentes():
    return _consultar(
        "SELECT id, destino, status FROM pedidos WHERE status = 'pendente' ORDER BY id"
    )

def banco_vazio():
    return _consultar("SELECT COUNT(*) FROM pontos")[0][0] == 0

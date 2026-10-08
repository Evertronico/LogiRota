"""
Camada de persistencia do LogiRota (SQLite).

Contrato: cada funcao abre e fecha a propria conexao e devolve dados
simples (tuplas, listas). Nenhum SQL vaza para o resto do programa, e
este modulo NAO importa ponto.py nem grafo.py - converter tupla em Ponto
e responsabilidade de quem chama (main.py), nao da persistencia.
"""

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
    """Cria as tabelas se nao existirem. Chamar uma vez, no inicio do
    programa, antes de qualquer outra operacao."""
    conexao = conectar()
    try:
        with conexao:
            conexao.executescript(SCHEMA)
    finally:
        conexao.close()


def _executar(sql, parametros=()):
    """Roda um INSERT/UPDATE e fecha a conexao. Devolve o id da linha."""
    conexao = conectar()
    try:
        with conexao:  # confirma (commit) ou desfaz (rollback)
            cursor = conexao.execute(sql, parametros)
            return cursor.lastrowid
    finally:
        conexao.close()  # o `with` NAO fecha a conexao, so faz o commit


def _consultar(sql, parametros=()):
    conexao = conectar()
    try:
        return conexao.execute(sql, parametros).fetchall()
    finally:
        conexao.close()


# ---------- insercao ----------

def salvar_ponto(ponto):
    """Grava um ponto. INSERT OR IGNORE: se o nome ja existe, nao duplica.

    Recebe qualquer objeto com nome, bairro, x e y - sem importar Ponto.
    """
    _executar(
        "INSERT OR IGNORE INTO pontos (nome, bairro, x, y) VALUES (?, ?, ?, ?)",
        (ponto.nome, ponto.bairro, ponto.x, ponto.y),
    )


def salvar_rua(origem, destino):
    """Grava uma rua entre dois pontos ja cadastrados."""
    _executar(
        "INSERT OR IGNORE INTO ruas (origem, destino) VALUES (?, ?)",
        (origem, destino),
    )


def salvar_pedido(destino):
    """Cria um pedido pendente. Devolve o id gerado.

    Levanta sqlite3.IntegrityError se `destino` nao for um ponto cadastrado.
    """
    return _executar("INSERT INTO pedidos (destino) VALUES (?)", (destino,))


def salvar_rota_calculada(origem, sequencia, distancia_total):
    """Usada na Semana 2. `sequencia` e uma lista de nomes."""
    return _executar(
        "INSERT INTO rotas_calculadas (origem, sequencia, distancia_total) "
        "VALUES (?, ?, ?)",
        (origem, " -> ".join(sequencia), distancia_total),
    )


# ---------- consulta ----------

def listar_pontos():
    """[(nome, bairro, x, y), ...]"""
    return _consultar("SELECT nome, bairro, x, y FROM pontos ORDER BY rowid")


def listar_ruas():
    """[(origem, destino), ...]"""
    return _consultar("SELECT origem, destino FROM ruas ORDER BY rowid")


def listar_pedidos_pendentes():
    """[(id, destino, status), ...]"""
    return _consultar(
        "SELECT id, destino, status FROM pedidos "
        "WHERE status = 'pendente' ORDER BY id"
    )
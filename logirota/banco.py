"""
Camada de persistencia do LogiRota (SQLite).

Regra de ouro: cada funcao abre e fecha a PROPRIA conexao e devolve dados simples
(tuplas e listas). Nenhum SQL vaza para o resto do programa, e este modulo NAO
importa ponto.py / grafo.py - quem converte tupla -> Ponto e o dominio/servico.
"""
import os
import sqlite3
from contextlib import contextmanager

# O arquivo fica na pasta do projeto, nao importa de onde o programa e executado.
CAMINHO_BANCO = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "LogiRota.db")
)

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

CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    preco REAL NOT NULL CHECK (preco >= 0),
    endereco TEXT NOT NULL REFERENCES pontos(nome),
    status TEXT NOT NULL DEFAULT 'disponivel'
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destino TEXT NOT NULL REFERENCES pontos(nome),
    status TEXT NOT NULL DEFAULT 'pendente',
    livro_id INTEGER REFERENCES livros(id)
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


@contextmanager
def _sessao():
    """Uso: with _sessao() as conexao:

    Faz commit se tudo der certo (ou rollback se der erro) e SEMPRE fecha a conexao.
    Atencao: 'with sqlite3.connect(...)' sozinho so faz commit/rollback, NAO fecha.
    """
    conexao = conectar()
    try:
        with conexao:
            yield conexao
    finally:
        conexao.close()


def inicializar():
    """Cria as tabelas se nao existirem. Chamar uma vez, no inicio do programa."""
    with _sessao() as conexao:
        conexao.executescript(SCHEMA)


# ---------- pontos e ruas ----------

def salvar_ponto(ponto):
    """Grava um ponto (qualquer objeto com nome, bairro, x, y). Devolve False se o nome ja existia."""
    with _sessao() as conexao:
        cursor = conexao.execute(
            "INSERT OR IGNORE INTO pontos (nome, bairro, x, y) VALUES (?, ?, ?, ?)",
            (ponto.nome, ponto.bairro, ponto.x, ponto.y),
        )
        return cursor.rowcount == 1


def salvar_rua(origem, destino):
    """Grava uma rua entre dois nomes de pontos ja cadastrados. Devolve False se ja existia."""
    with _sessao() as conexao:
        cursor = conexao.execute(
            "INSERT OR IGNORE INTO ruas (origem, destino) VALUES (?, ?)",
            (origem, destino),
        )
        return cursor.rowcount == 1


def listar_pontos():
    with _sessao() as conexao:
        return conexao.execute("SELECT nome, bairro, x, y FROM pontos ORDER BY nome").fetchall()


def listar_ruas():
    with _sessao() as conexao:
        return conexao.execute("SELECT origem, destino FROM ruas ORDER BY origem, destino").fetchall()


def contar_pontos():
    with _sessao() as conexao:
        return conexao.execute("SELECT COUNT(*) FROM pontos").fetchone()[0]


# ---------- livros ----------

def salvar_livro(titulo, autor, preco, endereco):
    """Cadastra um livro a venda em 'endereco' (nome de um ponto existente). Devolve o id."""
    with _sessao() as conexao:
        cursor = conexao.execute(
            "INSERT INTO livros (titulo, autor, preco, endereco) VALUES (?, ?, ?, ?)",
            (titulo, autor, preco, endereco),
        )
        return cursor.lastrowid


def listar_livros(somente_disponiveis=False):
    """Tuplas (id, titulo, autor, preco, endereco, status)."""
    sql = "SELECT id, titulo, autor, preco, endereco, status FROM livros"
    if somente_disponiveis:
        sql += " WHERE status = 'disponivel'"
    with _sessao() as conexao:
        return conexao.execute(sql + " ORDER BY id").fetchall()


# ---------- pedidos de entrega ----------

def salvar_pedido(destino, livro_id=None):
    """Cria um pedido pendente. Se vier um livro, ele precisa estar disponivel e passa a 'em_entrega'.

    Devolve o id do pedido. Levanta ValueError se o livro nao existir ou nao estiver disponivel.
    """
    with _sessao() as conexao:
        if livro_id is not None:
            linha = conexao.execute("SELECT status FROM livros WHERE id = ?", (livro_id,)).fetchone()
            if linha is None:
                raise ValueError(f"Livro {livro_id} nao existe.")
            if linha[0] != "disponivel":
                raise ValueError(f"Livro {livro_id} nao esta disponivel (status: {linha[0]}).")
            conexao.execute("UPDATE livros SET status = 'em_entrega' WHERE id = ?", (livro_id,))

        cursor = conexao.execute(
            "INSERT INTO pedidos (destino, livro_id) VALUES (?, ?)", (destino, livro_id)
        )
        return cursor.lastrowid


def listar_pedidos_pendentes():
    """Tuplas (id, destino, status) - o formato usado na apostila."""
    with _sessao() as conexao:
        return conexao.execute(
            "SELECT id, destino, status FROM pedidos WHERE status = 'pendente' ORDER BY id"
        ).fetchall()


def listar_entregas_pendentes():
    """Tuplas (pedido_id, titulo, endereco_da_venda, destino) dos pedidos pendentes com livro."""
    with _sessao() as conexao:
        return conexao.execute(
            """
            SELECT p.id, l.titulo, l.endereco, p.destino
            FROM pedidos p JOIN livros l ON l.id = p.livro_id
            WHERE p.status = 'pendente'
            ORDER BY p.id
            """
        ).fetchall()


def marcar_pedido_entregue(pedido_id):
    """Fecha o pedido e o livro. Devolve False se nao havia pedido pendente com esse id."""
    with _sessao() as conexao:
        cursor = conexao.execute(
            "UPDATE pedidos SET status = 'entregue' WHERE id = ? AND status = 'pendente'",
            (pedido_id,),
        )
        if cursor.rowcount == 0:
            return False
        conexao.execute(
            "UPDATE livros SET status = 'entregue' WHERE id = (SELECT livro_id FROM pedidos WHERE id = ?)",
            (pedido_id,),
        )
        return True

"""
Prova de fogo da Semana 1: os dados gravados por UM processo Python aparecem
em OUTRO processo Python (como fechar e reabrir o programa).

    python teste_persistencia.py
"""
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.abspath(__file__))


def rodar(caminho_db, codigo):
    """Executa 'codigo' num processo novo, apontando o banco para caminho_db."""
    preparo = (
        "import sys; sys.path.insert(0, %r)\n"
        "from LogiRota import banco, servico\n"
        "banco.CAMINHO_BANCO = %r\n"
        "banco.inicializar()\n" % (RAIZ, caminho_db)
    )
    resultado = subprocess.run([sys.executable, "-c", preparo + codigo],
                               capture_output=True, text=True, cwd=RAIZ)
    if resultado.returncode != 0:
        raise AssertionError(resultado.stderr)
    return resultado.stdout.strip()


class TestPersistencia(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.pasta.name, "teste.db")

    def tearDown(self):
        self.pasta.cleanup()

    def test_dados_sobrevivem_a_um_novo_processo(self):
        rodar(self.db, (
            "from main import PONTOS, RUAS\n"
            "servico.semear_se_vazio(PONTOS, RUAS)\n"
            "livro = banco.salvar_livro('Dom Casmurro', 'Machado de Assis', 29.9, 'Posto Central')\n"
            "banco.salvar_pedido('Loja Boa Familia', livro)\n"
        ))
        saida = rodar(self.db, (
            "print(len(banco.listar_pontos()), len(banco.listar_ruas()))\n"
            "print(banco.listar_entregas_pendentes())\n"
        ))
        linhas = saida.splitlines()
        self.assertEqual(linhas[0], "8 8")
        self.assertIn("Dom Casmurro", linhas[1])

    def test_rodar_duas_vezes_nao_duplica_dados_iniciais(self):
        semear = ("from main import PONTOS, RUAS\n"
                  "print(servico.semear_se_vazio(PONTOS, RUAS), banco.contar_pontos())\n")
        self.assertEqual(rodar(self.db, semear), "True 8")
        self.assertEqual(rodar(self.db, semear), "False 8")

    def test_livro_so_pode_ser_pedido_uma_vez(self):
        saida = rodar(self.db, (
            "from main import PONTOS, RUAS\n"
            "servico.semear_se_vazio(PONTOS, RUAS)\n"
            "livro = banco.salvar_livro('A', 'B', 10, 'Posto Central')\n"
            "banco.salvar_pedido('Loja Boa Familia', livro)\n"
            "try:\n"
            "    banco.salvar_pedido('Escola Norte', livro)\n"
            "except ValueError as erro:\n"
            "    print('recusado')\n"
        ))
        self.assertEqual(saida, "recusado")

    def test_endereco_inexistente_e_recusado_pelo_banco(self):
        saida = rodar(self.db, (
            "import sqlite3\n"
            "try:\n"
            "    banco.salvar_livro('A', 'B', 10, 'Rua que nao existe')\n"
            "except sqlite3.IntegrityError:\n"
            "    print('recusado')\n"
        ))
        self.assertEqual(saida, "recusado")

    def test_menor_caminho_e_erro_de_rota(self):
        saida = rodar(self.db, (
            "from main import PONTOS, RUAS\n"
            "servico.semear_se_vazio(PONTOS, RUAS)\n"
            "caminho, km = servico.caminho_entre('Posto Central', 'Loja Boa Familia')\n"
            "print(caminho, round(km, 2))\n"
            "try:\n"
            "    servico.caminho_entre('Posto Central', 'Farmacia Ilha')\n"
            "except servico.SemRotaError:\n"
            "    print('sem rota')\n"
        ))
        self.assertEqual(saida.splitlines(), [
            "['Posto Central', 'Padaria Distrito', 'Loja Boa Familia'] 10.3", "sem rota"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

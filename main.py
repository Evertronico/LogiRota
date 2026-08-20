"""
LogiRota - versão 5 (Aula 05).

A Aula 03 já tinha mostrado o problema: os mesmos 7 pontos,
inseridos em ordem alfabética, produzem uma ABB de altura 6 -
praticamente uma lista encadeada. Esta versão resolve o 
problema com uma única operação nova, a rotação, aplicada
logo após cada inserção.
"""
from logirota.abb import construir_indice
from logirota.arvore import altura, desenhar, total_nos
from logirota.balanceamento import constuir_indice_balanceado
from logirota.ponto import Ponto

# Os mesmos 7 pontos de entrega das aulas 03 e 04.
PONTOS = [
    Ponto("Mercado da Barra", "Barra", 2, 8),
    Ponto("Farmácia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Distrito", 12, 1),
    Ponto("Loja Boa Família", "Boa Família", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9)
]

def main():
    print("LogiRota - indice degenerado x indice balanceado\n")

    """A mesma sequência de inserção, já em ordem alfabética - 
    o pior cado identificado na Aula 03 - construída por
    dois algoritmos
    """
    ordem_alfabetica = sorted(PONTOS, key=lambda p: p.nome)

    degenerado = construir_indice(ordem_alfabetica)
    balanceado = constuir_indice_balanceado(ordem_alfabetica)

    print("\nindice SEM balanceamento:")
    desenhar(degenerado)
    print(f"total de pontos: {total_nos(degenerado)}")
    print(f"altura ........: {altura(degenerado)}")

    print("\nindice COM balanceamento:")
    desenhar(balanceado)
    print(f"total de pontos: {total_nos(balanceado)}")
    print(f"altura ........: {altura(balanceado)}")

    print(f"\n mesmos {total_nos(balanceado)} pontos.")
    print(f"\n mesma ordem de inserção:")
    print(f"altura sem balanceamento: {altura(degenerado)}")
    print(f"altura com balanceamento: {altura(balanceado)}")

if __name__ == "__main__":
      main();

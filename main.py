from logirota.abb import buscar, construir_indice
from logirota.arvore import altura, desenhar, total_nos
from logirota.ponto import Ponto

# pontos de entrega da malha de muriaé
# a ordem dessa lista é a ordem de inserção no indice, não é alfabética
PONTOS = [
    Ponto("Mercado da Barra", "Barra", 2, 8),
    Ponto("Farmácia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Dstrito", 12, 1),
    Ponto("Loja Boa Família", "Boa Família", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9)
]

def main():
    print("LogiRota - indice alfabetico de pontos\n")

    # constrói e exibe visualmente a árvore
    indice = construir_indice(PONTOS)
    desenhar(indice)

    print(f"\ntotal de pontos ...: {total_nos(indice)}")
    print(f"\naltura do indice ..: {altura(indice)}")

    print(f"\nbuscas:")
    for nome in ("Oficina Safira", "Padaria Distrito", "Padaria Inexistente"):
            achado = buscar(indice, nome)
            print(f"    buscar('{nome}') -> {achado}")

    ordem_alfabetica = sorted(PONTOS, key=lambda p: p.nome)
    degenerado = construir_indice(ordem_alfabetica)
    print(f"\nmesmos {total_nos(degenerado)} pontos, inseridos em ordem alfabética")
    print(f"\naltura do indice ....: {altura(indice)}")
    print(f"\naltura do degenerado ....: {altura(degenerado)}")

if __name__ == "__main__":
      main();

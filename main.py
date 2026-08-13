"""
LogiRota - versão 4 (Aula 04).

Os percursos tornam a árvore auditável. Em-ordem prova que o índice de
pontos (Aula 03) mantém os nomes em ordem alfabética. Pré-ordem e
pós-ordem geram dois relatórios diferentes sobre a mesma hierarquia ze 
zonas (Aula 02) - um do topo para os bairros, outro dos bairros para o
topo.
"""
from logirota.abb import construir_indice
from logirota.arvore import No
from logirota.percurso import em_ordem, pos_ordem, pre_ordem
from logirota.ponto import Ponto

# pontos de entrega da malha de muriaé
PONTOS = [
    Ponto("Mercado da Barra", "Barra", 2, 8),
    Ponto("Farmácia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Distrito", 12, 1),
    Ponto("Loja Boa Família", "Boa Família", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9)
]

# A hierarquia de zonas da Aula 02, reaproveitada para os relatórios
# de pré-ordem e pós-ordem
ZONAS = No(
    "CD Muriaé",
    esquerda=No("Zona Norte", No("Barra"), No("Bela Vista")),
    direita=No("Zona Sul",No("Safira"),No("Distrito", No("Boa Família")))
)

def main():
    print("LogiRota - relatórios por percursos\n")

    # Em-ordem: esquerda, raiz, direita -> prova que ABB fica ordenada.
    indice = construir_indice(PONTOS)
    print("indice em-ordem (alfabética por nome)")
    for ponto in em_ordem(indice):
        print(f"    {ponto}")

    # Pre-ordem: raiz, esquerda, direita -> manifesto do topo aos bairros
    print(f"\nrelatorio de zonas - pre-ordem (do topo para os bairros):")
    for zona in pre_ordem(ZONAS):
         print(f"    {zona}")

    # Pos-ordem: esquerda, direta, raiz -> zona só fecha após as subzonas.
    print(f"\nrelatorio de zonas - pos-ordem (bairro fecha antes da zona):")
    for zona in pos_ordem(ZONAS):
         print(f"    {zona}")

    # Os tres percursos leem os mesmos nós, em ordens diferentes:
    # a estrutura nao muda, so muda a pergunta que se faz a ela.

if __name__ == "__main__":
      main();

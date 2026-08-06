from logirota.arvore import No, altura, desenhar, folhas, total_nos
from logirota.fila import FilaDePedidos

# árvore montada à mão. A raiz é o centro de distribuição; cada nível
# divide a cidade em duas. As folhas são os bairros atendidos.
ZONAS = No(
    "CD Muriae",
    esquerda=No(
        "Zona Norte",
        esquerda=No("Barra"),
        direita=No("Bela Vista"),
    ),
    direita=No(
        "Zona Sul",
        esquerda=No("Safira"),
        direita=No(
            "Distrito",
            esquerda=No("Boa Familia"),
        ),
    ),
)

def main():
    print("LogiRota - Hierarquia de zonas e bairros\n")
    desenhar(ZONAS)

    print(f"\nraiz ...........: {ZONAS}")
    print(f"altura ...........: {altura(ZONAS)}")
    print(f"total de nós .....: {total_nos(ZONAS)}")
    print(f"bairros ..........: {', '.join(folhas(ZONAS))}")

    # a fila de pedidos
    fila = FilaDePedidos()
    for bairro in folhas(ZONAS):
        fila.enfileirar(bairro)
    print(f"\n{len(fila)} bairros na fila: {fila.frente()}")

if __name__ == "__main__":
    main()
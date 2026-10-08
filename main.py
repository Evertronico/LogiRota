from logirota import banco
from logirota.busca import bfs, componentes_conexos, dfs
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

DADOS_PONTOS_PADRAO = [
    Ponto("Mercado Barra", "Barra", 2, 8),
    Ponto("Farmacia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Distrito", 12, 1),
    Ponto("Loja Boa Familia", "Boa Familia", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9),
    Ponto("Farmacia Ilha", "Ilha", 25, 25),
]

DADOS_RUAS_PADRAO = [
    ("Escola Norte", "Mercado Barra"),
    ("Mercado Barra", "Farmacia Bela Vista"),
    ("Mercado Barra", "Posto Central"),
    ("Farmacia Bela Vista", "Posto Central"),
    ("Posto Central", "Oficina Safira"),
    ("Posto Central", "Padaria Distrito"),
    ("Oficina Safira", "Padaria Distrito"),
    ("Padaria Distrito", "Loja Boa Familia"),
]

def verificar_e_popular_base():
    if not banco.listar_pontos():
        for item_ponto in DADOS_PONTOS_PADRAO:
            banco.salvar_ponto(item_ponto)
            
    if not banco.listar_ruas():
        for origem, destino in DADOS_RUAS_PADRAO:
            banco.salvar_rua(origem, destino)

def carregar_pontos_armazenados():
    return [
        Ponto(nome, bairro, pos_x, pos_y)
        for nome, bairro, pos_x, pos_y in banco.listar_pontos()
    ]

def construir_rede_viaria(lista_pontos):
    rede_grafo = GrafoLista(lista_pontos)
    
    conexoes = banco.listar_ruas()
    pos = 0
    while pos < len(conexoes):
        ponto_a, ponto_b = conexoes[pos]
        rede_grafo.adicionar_rua(ponto_a, ponto_b)
        pos += 1
        
    return rede_grafo

def main():
    banco.inicializar()
    
    verificar_e_popular_base()

    print("LogiRota - Sistema de Gestão Viária e Pedidos\n")

    pontos = carregar_pontos_armazenados()
    grafo_malha = construir_rede_viaria(pontos)
    ponto_inicial = "Posto Central"

    percurso_largura = bfs(grafo_malha, ponto_inicial)
    percurso_profundidade = dfs(grafo_malha, ponto_inicial)

    print(f"partindo de '{ponto_inicial}':\n")
    print(f"  BFS (fila) .: {' -> '.join(percurso_largura)}")
    print(f"  DFS (pilha) : {' -> '.join(percurso_profundidade)}")
    print("\n  Nota técnica: a diferença de ordem ocorre devido à estrutura auxiliar utilizada.")

    relacao_nomes = [p.nome for p in pontos]
    componentes = componentes_conexos(grafo_malha, relacao_nomes)

    print(f"\ncomponentes conexos da malha ({len(componentes)}):")
    for bloco in componentes:
        print(f"    {{{', '.join(bloco)}}}")

    if len(componentes) > 1:
        isolados = [bloco[0] for bloco in componentes if len(bloco) == 1]
        print(f"\n  Atenção: o ponto {', '.join(isolados)} está isolado -")
        print("  nenhuma rota cadastrada permite alcançá-lo.")

    pedidos_atuais = banco.listar_pedidos_pendentes()
    print(f"\nPedidos pendentes na fila ({len(pedidos_atuais)}):")
    for id_ped, destino_ped, status_ped in pedidos_atuais:
        print(f"   #{id_ped} -> Destino: {destino_ped} ({status_ped})")

    entrada_usuario = input("\nCadastrar novo pedido - Informe o destino (ou pressione Enter para sair): ").strip()
    
    if entrada_usuario in relacao_nomes:
        codigo_gerado = banco.salvar_pedido(entrada_usuario)
        print(f"   Sucesso! Pedido #{codigo_gerado} registrado para: {entrada_usuario}")
    elif entrada_usuario:
        print("   Erro: O destino informado não consta nos pontos cadastrados.")


if __name__ == "__main__":
    main()
"""
LogiRota — entrega de livros (Semana 1: persistência em SQLite).

Cadastre livros à venda com o endereço da venda, peça a entrega para outro
endereço e veja a localização e a rota no mapa. Tudo fica gravado em
logirota.db: feche o programa, abra de novo e os dados continuam lá.

    python main.py
"""

from LogiRota import banco, servico
from LogiRota.ponto import Ponto

# Cadastro fixo das aulas anteriores. Só é gravado no banco na PRIMEIRA execução
# (banco vazio); depois disso, o banco é a única fonte de verdade.
PONTOS = [
    Ponto("Mercado Barra", "Barra", 2, 8),
    Ponto("Farmacia Bela Vista", "Bela Vista", 6, 3),
    Ponto("Oficina Safira", "Safira", 9, 5),
    Ponto("Padaria Distrito", "Distrito", 12, 1),
    Ponto("Loja Boa Familia", "Boa Familia", 14, 0),
    Ponto("Posto Central", "Centro", 5, 5),
    Ponto("Escola Norte", "Zona Norte", 3, 9),
    # Cadastrado, mas nenhuma rua liga este ponto aos demais.
    Ponto("Farmacia Ilha", "Ilha", 25, 25),
]

RUAS = [
    ("Escola Norte", "Mercado Barra"),
    ("Mercado Barra", "Farmacia Bela Vista"),
    ("Mercado Barra", "Posto Central"),
    ("Farmacia Bela Vista", "Posto Central"),
    ("Posto Central", "Oficina Safira"),
    ("Posto Central", "Padaria Distrito"),
    ("Oficina Safira", "Padaria Distrito"),
    ("Padaria Distrito", "Loja Boa Familia"),
]


# ---------- entrada de dados ----------

def ler_texto(pergunta):
    while True:
        texto = input(pergunta).strip()
        if texto:
            return texto
        print("  Este campo nao pode ficar vazio.")


def ler_numero(pergunta, minimo=None):
    while True:
        try:
            valor = float(input(pergunta).strip().replace(",", "."))
        except ValueError:
            print("  Digite um numero (ex.: 12,5).")
            continue
        if minimo is not None and valor < minimo:
            print(f"  O valor minimo e {minimo}.")
            continue
        return valor


def escolher(opcoes, titulo, formatar=str):
    """Mostra uma lista numerada e devolve o item escolhido (None se o usuario digitar 0)."""
    print(titulo)
    for i, item in enumerate(opcoes, start=1):
        print(f"  {i}. {formatar(item)}")
    print("  0. Cancelar")
    while True:
        escolha = input("Numero: ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return opcoes[int(escolha) - 1]
        print("  Opcao invalida.")


def escolher_ponto(titulo):
    return escolher(servico.carregar_pontos(), titulo, lambda p: f"{p} - posicao ({p.x:g}, {p.y:g}) km")


# ---------- mapa ----------

def abrir_mapa(rota=None, destaque=None, titulo="LogiRota - Malha Viaria"):
    try:
        from LogiRota.visualizacao import mostrar_mapa
    except ImportError:
        print("  tkinter nao esta instalado neste Python; nao e possivel abrir o mapa.")
        return
    print("  Abrindo o mapa... feche a janela para voltar ao menu.")
    mostrar_mapa(servico.carregar_pontos(), servico.carregar_ruas(),
                 rota=rota, destaque=destaque, titulo=titulo)


# ---------- opcoes do menu ----------

def cadastrar_ponto():
    print("\n== Novo endereco ==")
    nome = ler_texto("Endereco (ex.: Rua das Flores, 120): ")
    bairro = ler_texto("Bairro: ")
    print("Posicao no mapa, em km (veja a posicao dos outros enderecos na opcao 2).")
    x = ler_numero("x: ")
    y = ler_numero("y: ")
    if servico.cadastrar_ponto(nome, bairro, x, y):
        print(f"  Endereco '{nome}' cadastrado.")
        print("  Dica: use a opcao 7 para ligar este endereco a outro por uma rua.")
    else:
        print(f"  Ja existe um endereco chamado '{nome}'.")


def listar_enderecos():
    print("\n== Enderecos e ruas ==")
    for p in servico.carregar_pontos():
        print(f"  {p} - posicao ({p.x:g}, {p.y:g}) km")
    print("Ruas:")
    for a, b in servico.carregar_ruas():
        print(f"  {a} <-> {b}")


def cadastrar_rua():
    print("\n== Nova rua (liga dois enderecos) ==")
    a = escolher_ponto("Primeiro endereco:")
    if a is None:
        return
    b = escolher_ponto("Segundo endereco:")
    if b is None:
        return
    try:
        if servico.cadastrar_rua(a.nome, b.nome):
            print(f"  Rua cadastrada: {a.nome} <-> {b.nome} ({a.distancia_ate(b):.2f} km).")
        else:
            print("  Essa rua ja estava cadastrada.")
    except ValueError as erro:
        print(f"  {erro}")


def cadastrar_livro():
    print("\n== Cadastrar livro para venda ==")
    titulo = ler_texto("Titulo: ")
    autor = ler_texto("Autor: ")
    preco = ler_numero("Preco (R$): ", minimo=0)
    local = escolher_ponto("Endereco da venda (onde o livro esta):")
    if local is None:
        print("  Cadastro cancelado.")
        return
    livro_id = banco.salvar_livro(titulo, autor, preco, local.nome)
    print(f"  Livro #{livro_id} cadastrado: '{titulo}' em {local.nome}.")


def listar_livros():
    print("\n== Livros ==")
    livros = banco.listar_livros()
    if not livros:
        print("  Nenhum livro cadastrado ainda.")
    for livro_id, titulo, autor, preco, endereco, status in livros:
        print(f"  #{livro_id} '{titulo}' - {autor} - R$ {preco:.2f} - {endereco} [{status}]")


def solicitar_entrega():
    print("\n== Solicitar entrega ==")
    disponiveis = banco.listar_livros(somente_disponiveis=True)
    if not disponiveis:
        print("  Nao ha livros disponiveis. Cadastre um livro na opcao 3.")
        return
    livro = escolher(disponiveis, "Livro a entregar:",
                     lambda l: f"#{l[0]} '{l[1]}' ({l[4]})")
    if livro is None:
        return
    destino = escolher_ponto("Endereco de entrega:")
    if destino is None:
        return
    if destino.nome == livro[4]:
        print("  O livro ja esta nesse endereco.")
        return
    try:
        pedido_id = banco.salvar_pedido(destino.nome, livro[0])
    except ValueError as erro:
        print(f"  {erro}")
        return
    print(f"  Pedido #{pedido_id} criado: '{livro[1]}' de {livro[4]} para {destino.nome}.")


def listar_pedidos():
    print("\n== Pedidos pendentes ==")
    entregas = banco.listar_entregas_pendentes()
    if not entregas:
        print("  Nenhum pedido pendente.")
    for pedido_id, titulo, origem, destino in entregas:
        print(f"  Pedido #{pedido_id}: '{titulo}'  {origem}  ->  {destino}")


def ver_entrega_no_mapa():
    print("\n== Rota de uma entrega ==")
    entregas = banco.listar_entregas_pendentes()
    if not entregas:
        print("  Nenhum pedido pendente.")
        return
    pedido = escolher(entregas, "Pedido:", lambda e: f"#{e[0]} '{e[1]}': {e[2]} -> {e[3]}")
    if pedido is None:
        return
    pedido_id, titulo, origem, destino = pedido
    try:
        caminho, km = servico.caminho_entre(origem, destino)
    except servico.SemRotaError as erro:
        print(f"  Sem rota possivel: {erro}")
        print("  Cadastre uma rua que ligue os dois lados (opcao 7).")
        return
    except ValueError as erro:
        print(f"  {erro}")
        return
    print(f"  Caminho: {' -> '.join(caminho)}")
    print(f"  Distancia total: {km:.2f} km")
    abrir_mapa(rota=caminho, titulo=f"Entrega de '{titulo}' - {km:.2f} km")


def ver_livro_no_mapa():
    print("\n== Localizacao de um livro ==")
    livros = banco.listar_livros()
    if not livros:
        print("  Nenhum livro cadastrado ainda.")
        return
    livro = escolher(livros, "Livro:", lambda l: f"#{l[0]} '{l[1]}' ({l[4]})")
    if livro is None:
        return
    print(f"  '{livro[1]}' esta em: {livro[4]}")
    abrir_mapa(destaque=livro[4], titulo=f"'{livro[1]}' - {livro[4]}")


def marcar_entregue():
    print("\n== Marcar entrega como concluida ==")
    entregas = banco.listar_entregas_pendentes()
    if not entregas:
        print("  Nenhum pedido pendente.")
        return
    pedido = escolher(entregas, "Pedido entregue:", lambda e: f"#{e[0]} '{e[1]}': {e[2]} -> {e[3]}")
    if pedido is None:
        return
    banco.marcar_pedido_entregue(pedido[0])
    print(f"  Pedido #{pedido[0]} marcado como entregue.")


MENU = [
    ("Cadastrar endereco", cadastrar_ponto),
    ("Ver enderecos e ruas", listar_enderecos),
    ("Cadastrar livro para venda", cadastrar_livro),
    ("Listar livros", listar_livros),
    ("Solicitar entrega de um livro", solicitar_entrega),
    ("Ver pedidos pendentes", listar_pedidos),
    ("Cadastrar rua entre dois enderecos", cadastrar_rua),
    ("Ver rota de uma entrega no mapa", ver_entrega_no_mapa),
    ("Ver localizacao de um livro no mapa", ver_livro_no_mapa),
    ("Marcar entrega como concluida", marcar_entregue),
]


def main():
    banco.inicializar()
    if servico.semear_se_vazio(PONTOS, RUAS):
        print("Primeira execucao: banco criado com os enderecos das aulas.")

    print("LogiRota - entrega de livros")
    while True:
        print("\n--- Menu ---")
        for i, (descricao, _) in enumerate(MENU, start=1):
            print(f"  {i:>2}. {descricao}")
        print("   0. Sair")
        opcao = input("Opcao: ").strip()
        if opcao == "0":
            print("Ate logo! Seus dados ficaram salvos em logirota.db.")
            return
        if opcao.isdigit() and 1 <= int(opcao) <= len(MENU):
            MENU[int(opcao) - 1][1]()
        else:
            print("  Opcao invalida.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrado.")

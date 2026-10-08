import math
import tkinter as tk

_MARGEM = 60
_RAIO_PONTO = 22
_LADOS_CIRCULO = 24

def _linha(canvas, x1, y1, x2, y2, largura, cor):
    comprimento = math.hypot(x2 - x1, y2 - y1) or 1
    ox = -(y2 - y1) / comprimento * largura / 2
    oy = (x2 - x1) / comprimento * largura / 2
    canvas.create_polygon(x1 + ox, y1 + oy, x2 + ox, y2 + oy,
                           x2 - ox, y2 - oy, x1 - ox, y1 - oy,
                           fill=cor, outline=cor)

def _circulo(canvas, cx, cy, raio, fill, outline, largura):
    pontos = []
    for i in range(_LADOS_CIRCULO):
        angulo = 2 * math.pi * i / _LADOS_CIRCULO
        pontos.append(cx + raio * math.cos(angulo))
        pontos.append(cy + raio * math.sin(angulo))
    canvas.create_polygon(*pontos, fill=fill, outline=outline, width=largura)

def _calcular_transformacao(pontos, largura, altura):
    xs = [p.x for p in pontos]
    ys = [p.y for p in pontos]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    largura_util = largura - 2 * _MARGEM
    altura_util = altura - 2 * _MARGEM
    escala_x = largura_util / (x_max - x_min) if x_max != x_min else 1
    escala_y = altura_util / (y_max - y_min) if y_max != y_min else 1
    escala = min(escala_x, escala_y)

    def transformar(x, y):
        px = _MARGEM + (x - x_min) * escala
        py = altura - _MARGEM - (y - y_min) * escala
        return px, py

    return transformar

def _desenhar(canvas, pontos, ruas, rota=None, destaque=None):
    largura = int(canvas["width"])
    altura = int(canvas["height"])
    transformar = _calcular_transformacao(pontos, largura, altura)
    por_nome = {p.nome: p for p in pontos}

    arestas_da_rota = set()
    if rota:
        arestas_da_rota = {frozenset((a, b)) for a, b in zip(rota, rota[1:])}

    for nome_a, nome_b in ruas:
        xa, ya = transformar(por_nome[nome_a].x, por_nome[nome_a].y)
        xb, yb = transformar(por_nome[nome_b].x, por_nome[nome_b].y)
        na_rota = frozenset((nome_a, nome_b)) in arestas_da_rota
        cor = "#0D9488" if na_rota else "#B0B0B0"
        largura_linha = 4 if na_rota else 2
        _linha(canvas, xa, ya, xb, yb, largura_linha, cor)

    for ponto in pontos:
        px, py = transformar(ponto.x, ponto.y)
        em_destaque = ponto.nome == destaque or (rota and ponto.nome in rota)
        cor_borda = "#0D9488" if em_destaque else "#1A1A1A"
        _circulo(canvas, px, py, _RAIO_PONTO, "white", cor_borda, 2)
        canvas.create_text(px, py + _RAIO_PONTO + 14, text=ponto.nome,
                            font=("Helvetica", 11))

def mostrar_mapa(pontos, ruas, rota=None, destaque=None,
                  titulo="LogiRota — Malha Viária"):
    janela = tk.Tk()
    janela.title(titulo)
    canvas = tk.Canvas(janela, width=900, height=560, bg="white")
    canvas.pack()
    _desenhar(canvas, pontos, ruas, rota=rota, destaque=destaque)

    janela.update_idletasks()
    largura_janela = janela.winfo_width()
    altura_janela = janela.winfo_height()
    janela.geometry(f"{largura_janela + 1}x{altura_janela + 1}")
    janela.update_idletasks()
    janela.geometry(f"{largura_janela}x{altura_janela}")

    janela.lift()
    janela.attributes("-topmost", True)
    janela.after(200, lambda: janela.attributes("-topmost", False))
    janela.focus_force()

    janela.mainloop()
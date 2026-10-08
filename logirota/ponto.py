
class Ponto:

    def __init__(self, nome, bairro, x, y):
        self._nome = nome
        self._bairro = bairro
        self._x = x
        self._y = y

    @property
    def nome(self):
        return self._nome

    @property
    def bairro(self):
        return self._bairro

    def distancia_ate(self, outro):

        dx = self._x - outro._x
        dy = self._y - outro._y
        return round((dx * dx + dy * dy) ** 0.5, 2)

    def __str__(self):
        return f"{self._nome} ({self._bairro})"


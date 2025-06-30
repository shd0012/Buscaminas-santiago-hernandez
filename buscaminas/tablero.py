import random
from casillas import Mina, Vacia

class Tablero:
    def __init__(self, filas, columnas, dificultad):
        self.filas = filas
        self.columnas = columnas
        self.dificultad = dificultad
        self.casillas = [[Vacia() for _ in range(columnas)] for _ in range(filas)]
        self._colocar_minas()
        self._contar_adyacentes()

    def _colocar_minas(self):
        total = int(self.filas * self.columnas * self.dificultad)
        posiciones = random.sample(range(self.filas * self.columnas), total)
        for p in posiciones:
            f, c = divmod(p, self.columnas)
            self.casillas[f][c] = Mina()

    def _contar_adyacentes(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                if not self.casillas[f][c].es_mina():
                    self.casillas[f][c].minas_alrededor = self._contar_minas_cercanas(f, c)

    def _contar_minas_cercanas(self, fila, col):
        total = 0
        for df in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nf, nc = fila + df, col + dc
                if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                    if self.casillas[nf][nc].es_mina():
                        total += 1
        return total

    def revelar(self, fila, col):
        if self.casillas[fila][col].revelada:
            return True
        self.casillas[fila][col].revelada = True
        if self.casillas[fila][col].es_mina():
            return False
        if self.casillas[fila][col].minas_alrededor == 0:
            for df in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nf, nc = fila + df, col + dc
                    if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                        if not self.casillas[nf][nc].revelada:
                            self.revelar(nf, nc)
        return True

    def completado(self):
        for fila in self.casillas:
            for casilla in fila:
                if not casilla.revelada and not casilla.es_mina():
                    return False
        return True

    def mostrar_tablero(self):
        print("\n   " + " ".join([f"{i}" for i in range(self.columnas)]))
        for idx, fila in enumerate(self.casillas):
            print(f"{idx:2} " + " ".join([c.mostrar() for c in fila]))

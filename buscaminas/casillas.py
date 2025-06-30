from abc import ABC, abstractmethod

class Casilla(ABC):
    def __init__(self):
        self.revelada = False
        self.marcada = False

    @abstractmethod
    def es_mina(self):
        pass

    @abstractmethod
    def mostrar(self):
        pass

class Mina(Casilla):
    def es_mina(self):
        return True

    def mostrar(self):
        return "*" if self.revelada else "■"

class Vacia(Casilla):
    def __init__(self):
        super().__init__()
        self.minas_alrededor = 0

    def es_mina(self):
        return False

    def mostrar(self):
        if self.revelada:
            return str(self.minas_alrededor) if self.minas_alrededor > 0 else " "
        return "■"

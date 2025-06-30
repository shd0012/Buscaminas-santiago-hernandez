import json
import time
import os
from tablero import Tablero

class Juego:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(self.base_path, "config.json")

        with open(config_path) as f:
            self.config = json.load(f)

        self.leaderboard_file = os.path.join(self.base_path, "leaderboard.json")
        try:
            with open(self.leaderboard_file) as f:
                self.leaderboard = json.load(f)
        except FileNotFoundError:
            self.leaderboard = []

        self.nombre = input("Nombre: ")
        self.apellido = input("Apellido: ")
        self.dificultad = self._elegir_dificultad()
        self.board_size = self.config["global"]["board_size"]
        self.proporcion_minas = self.config["global"]["quantity_of_mines"][self.dificultad]
        self.tablero = Tablero(self.board_size[0], self.board_size[1], self.proporcion_minas)

    def _elegir_dificultad(self):
        opciones = list(self.config["global"]["quantity_of_mines"].keys())
        while True:
            print("\nDificultades:", ", ".join(opciones))
            dificultad = input("Elige dificultad: ").lower()
            if dificultad in opciones:
                return dificultad
            print("Opción inválida.")

    def jugar(self):
        inicio = time.time()
        while True:
            self.tablero.mostrar_tablero()
            try:
                fila, col = map(int, input("Selecciona casilla (fila,col): ").split(','))
            except:
                print("Entrada inválida. Usa el formato fila,col")
                continue

            if not (0 <= fila < self.board_size[0] and 0 <= col < self.board_size[1]):
                print("Coordenadas fuera de rango.")
                continue

            if not self.tablero.revelar(fila, col):
                self.tablero.mostrar_tablero()
                print("💥 Has perdido.")
                return

            if self.tablero.completado():
                self.tablero.mostrar_tablero()
                duracion = round(time.time() - inicio, 2)
                print(f"🎉 ¡Ganaste en {duracion} segundos!")
                self._registrar_resultado(duracion)
                self._mostrar_top3()
                return

    def _registrar_resultado(self, duracion):
        self.leaderboard.append({
            "first_name": self.nombre,
            "last_name": self.apellido,
            "time": duracion,
            "difficulty": self.dificultad
        })
        with open(self.leaderboard_file, "w") as f:
            json.dump(self.leaderboard, f, indent=2)

    def _mostrar_top3(self):
        print("\n🏆 Mejores tiempos:")
        mejores = sorted(self.leaderboard, key=lambda x: x["time"])[:3]
        for i, jugador in enumerate(mejores, 1):
            nombre = f"{jugador['first_name']} {jugador['last_name']}"
            print(f"{i}. {nombre} - {jugador['time']}s ({jugador['difficulty']})")

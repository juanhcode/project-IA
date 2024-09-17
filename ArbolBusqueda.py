from collections import deque
from Node import Nodo
import time

class ArbolBusqueda:
    def __init__(self, canvas, maze_canvas, cell_size):
        self.search_canvas = canvas
        self.maze_canvas = maze_canvas
        self.cell_size = cell_size
        self.x_positions = {}
        self.y_positions = {}
        self.level = 0

    def busqueda_por_amplitud(self, matriz, estado_inicial, limite_expansiones=2):
        cola = deque()
        cola.append(Nodo(estado_inicial, None, None, matriz[estado_inicial[0]][estado_inicial[1]]))
        expansions = 0

        while cola and expansions < limite_expansiones:
            node = cola.popleft()
            print("Padre", node)
            fila, columna = node.estado

            if node.valor == 2:
                print("Encontrado")
                break

            # Expandir
            hijos = []
            for movimiento, (df, dc) in {
                "arriba": (-1, 0),
                "abajo": (1, 0),
                "izquierda": (0, -1),
                "derecha": (0, 1)
            }.items():
                nuevo_fila, nuevo_columna = fila + df, columna + dc
                if 0 <= nuevo_fila < len(matriz) and 0 <= nuevo_columna < len(matriz[0]):
                    if matriz[nuevo_fila][nuevo_columna] != 1:
                        expansions += 1
                        nuevo_nodo = Nodo((nuevo_fila, nuevo_columna), node, movimiento, matriz[nuevo_fila][nuevo_columna])
                        cola.append(nuevo_nodo)
                        hijos.append(nuevo_nodo)

            self.pintar_nodos_y_aristas(node, hijos)
            time.sleep(1)

        if expansions >= limite_expansiones:
            print("Límite de expansiones alcanzado")
        return "No Encontrado"

    def pintar_nodos_y_aristas(self, padre, hijos):
        if padre.estado not in self.x_positions:
            self.x_positions[padre.estado] = 200
            self.y_positions[padre.estado] = 50 + self.level * 100

        x1, y1 = self.x_positions[padre.estado], self.y_positions[padre.estado]
        self.search_canvas.create_oval(x1 - 15, y1 - 15, x1 + 15, y1 + 15, fill="blue")
        self.search_canvas.create_text(x1, y1, text=str(padre.estado), fill="white")

        fila, columna = padre.estado
        self.maze_canvas.create_rectangle(
            columna * self.cell_size, fila * self.cell_size,
            (columna + 1) * self.cell_size, (fila + 1) * self.cell_size,
            fill="blue", outline='black'
        )

        espacio_horiz = 200
        if len(hijos) > 1:
            espacio_horiz = 200 // len(hijos)

        start_x = x1 - ((len(hijos) - 1) * espacio_horiz // 2)

        for i, hijo in enumerate(hijos):
            self.x_positions[hijo.estado] = start_x + i * espacio_horiz
            self.y_positions[hijo.estado] = y1 + 100

            x2, y2 = self.x_positions[hijo.estado], self.y_positions[hijo.estado]
            self.search_canvas.create_oval(x2 - 15, y2 - 15, x2 + 15, y2 + 15, fill="red")
            self.search_canvas.create_text(x2, y2, text=str(hijo.estado), fill="white")

            fila, columna = hijo.estado
            self.maze_canvas.create_rectangle(
                columna * self.cell_size, fila * self.cell_size,
                (columna + 1) * self.cell_size, (fila + 1) * self.cell_size,
                fill="red", outline='black'
            )

            self.search_canvas.create_line(x1, y1, x2, y2, fill="black")

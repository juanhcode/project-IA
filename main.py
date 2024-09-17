import tkinter as tk
from ArbolBusqueda import ArbolBusqueda
from Interface import InterfazLaberinto
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Búsqueda en Laberinto")

    maze = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Laberinto vacío

    canvas_busqueda = tk.Canvas(root, width=400, height=400, bg='white')
    canvas_busqueda.grid(row=1, column=0)

    arbol_busqueda = ArbolBusqueda(canvas_busqueda, None, 50)  # Proveer canvas del laberinto más tarde

    interfaz = InterfazLaberinto(root, maze, arbol_busqueda)

    root.mainloop()

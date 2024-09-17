import tkinter as tk
from PIL import Image, ImageTk
from collections import deque
from Node import Nodo
import time
import random
import subprocess

# Definir el laberinto predefinido
maze = [
    [0, 0, 0, 0],
    [0, 1, 1, 2],
    [3, 1, 0, 0],
    [0, 0, 0, 1]
]


estado = None
mouse_position = None
wall_count = 0
place_mouse = False
place_wall = False
place_cheese = False

# Variables globales para el dibujo del árbol
x_positions = {}
y_positions = {}
level = 0

def set_estado(value):
    global estado
    estado = value

def busquedaPorAmplitud(matriz, estado_inicial, limite_expansiones=2):
    print("estado inicial", estado_inicial)
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
                    print("nuevo nodo", nuevo_nodo)
                    cola.append(nuevo_nodo)
                    hijos.append(nuevo_nodo)

        pintar_nodos_y_aristas(node, hijos)
        root.update()
        time.sleep(1)  # Esperar 1 segundo antes de continuar

    if expansions >= limite_expansiones:
        print("Límite de expansiones alcanzado")
        print("expansiones", expansions)
    else:
        print("expansiones", expansions)
    return "No Encontrado"


def busquedaEnProfundidad(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda en profundidad")
    stack = deque()
    stack.append(Nodo(estado_inicial, None, None, matriz[estado_inicial[0]][estado_inicial[1]]))
    expansions = 0

    while stack and expansions < limite_expansiones:
        node = stack.pop()
        print("Padre", node)
        fila, columna = node.estado

        if node.valor == 2:
            print("Encontrado")
            break

        # Expandir
        hijos = []
        for movimiento, (df, dc) in {
            "izquierda": (0, -1),
            "arriba": (-1, 0),
            "derecha": (0, 1),
            "abajo": (1, 0)
        }.items():
            nuevo_fila, nuevo_columna = fila + df, columna + dc
            if 0 <= nuevo_fila < len(matriz) and 0 <= nuevo_columna < len(matriz[0]):
                if matriz[nuevo_fila][nuevo_columna] != 1:
                    expansions += 1
                    nuevo_nodo = Nodo((nuevo_fila, nuevo_columna), node, movimiento, matriz[nuevo_fila][nuevo_columna])
                    print("nuevo nodo", nuevo_nodo)
                    stack.append(nuevo_nodo)
                    hijos.append(nuevo_nodo)

        pintar_nodos_y_aristas(node, hijos)
        root.update()
        time.sleep(1)  # Esperar 1 segundo antes de continuar

    if expansions >= limite_expansiones:
        print("Límite de expansiones alcanzado")
        print("expansiones", expansions)
    else:
        print("expansiones", expansions)
    return "No Encontrado"


def busquedaPorCostoUniforme(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda por costo uniforme")
    pass

def busquedaLimitadaPorProfundidad(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda limitada por profundidad")
    pass

def busquedaProfundidadIterativa(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda en profundidad iterativa")
    pass

def busquedaAvara(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda avara")
    pass

def on_click(event):
    global place_mouse, place_wall, place_cheese, mouse_position, wall_count
    
    row = event.y // cell_size
    column = event.x // cell_size
    
    if place_mouse:
        if mouse_position:
            update_cell(mouse_position[0], mouse_position[1], 'white')
            maze[mouse_position[0]][mouse_position[1]] = 0  # Reset previous mouse position
        mouse_position = (row, column)
        update_cell(row, column, None, mouse_image)  # No pasamos un color, solo la imagen del ratón
        maze[row][column] = 3
        place_mouse = False
        update_controls()

    elif place_wall:
        if maze[row][column] == 0:
            maze[row][column] = 1
            wall_count += 1
            update_cell(row, column, 'black')  # Color de pared
            update_controls()
    
    elif place_cheese:
        if maze[row][column] == 0:
            maze[row][column] = 2
            update_cell(row, column, 'yellow')  # Color de queso
            place_cheese = False
            update_controls()
    
    print_matrix()

def update_controls():
    if mouse_position and wall_count > 1:
        start_button.config(state='normal')
    else:
        start_button.config(state='disabled')

def print_matrix():
    for row in maze:
        print(row)
    print()

def update_cell(row, column, color, image=None):
    x1 = column * cell_size
    y1 = row * cell_size
    x2 = (column + 1) * cell_size
    y2 = (row + 1) * cell_size

    # Si se proporciona un color, se pinta la celda
    if color:
        maze_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black') 
    # Dibujar la imagen si se proporciona
    if image:
        image_resized = image.resize((cell_size, cell_size), Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image_resized)
        maze_canvas.create_image(x1, y1, anchor='nw', image=image_tk)
        # Necesario para mantener la referencia de la imagen en memoria
        maze_canvas.image = image_tk

##Lista de funciones de búsqueda disponibles
busquedas = [busquedaPorAmplitud, busquedaEnProfundidad]
busquedas_realizadas = []

def iniciar_busqueda():
    global busquedas_realizadas

    if len(busquedas_realizadas) == len(busquedas):
        print("Todas las búsquedas han sido realizadas")
        return

    limite_expansiones = int(expansions_entry.get())
    if mouse_position:
        # Seleccionar una búsqueda al azar que no haya sido realizada
        busqueda = random.choice([b for b in busquedas if b not in busquedas_realizadas])
        busquedas_realizadas.append(busqueda)
        busqueda(maze, mouse_position, limite_expansiones)
    else:
        print("No se ha colocado el ratón")

# def iniciar_busqueda():
#     limite_expansiones = int(expansions_entry.get())
#     if mouse_position:
#         busquedaEnProfundidad(maze, mouse_position, limite_expansiones)
#     else:
#         print("No se ha colocado el ratón")

def pintar_nodos_y_aristas(padre, hijos):
    global level, mouse_position

    # Borrar la imagen del ratón de la celda actual
    if mouse_position:
        update_cell(mouse_position[0], mouse_position[1], 'white')

    # Mover el ratón a la nueva posición
    fila, columna = padre.estado
    update_cell(fila, columna, None, mouse_image)  # Usar la imagen del ratón
    mouse_position = (fila, columna)

    # Dibujar las aristas en el canvas de búsqueda
    if padre.estado not in x_positions:
        x_positions[padre.estado] = 200
        y_positions[padre.estado] = 50 + level * 150  # Aumentar la distancia vertical entre niveles

    x1, y1 = x_positions[padre.estado], y_positions[padre.estado]
    search_canvas.create_oval(x1 - 15, y1 - 15, x1 + 15, y1 + 15, fill="blue")
    search_canvas.create_text(x1, y1, text=str(padre.estado), fill="white")

    # Dibujar hijos y sus aristas
    espacio_horiz = 200
    if len(hijos) > 1:
        espacio_horiz = 200 // len(hijos)

    start_x = x1 - ((len(hijos) - 1) * espacio_horiz // 2)

    for i, hijo in enumerate(hijos):
        x_positions[hijo.estado] = start_x + i * espacio_horiz
        y_positions[hijo.estado] = y1 + 150  # Aumentar la distancia vertical entre niveles

        x2, y2 = x_positions[hijo.estado], y_positions[hijo.estado]
        search_canvas.create_oval(x2 - 15, y2 - 15, x2 + 15, y2 + 15, fill="purple")
        search_canvas.create_text(x2, y2, text=str(hijo.estado), fill="white")
        search_canvas.create_line(x1, y1, x2, y2, fill="black")

    # Ajustar el scroll region del canvas
    search_canvas.config(scrollregion=search_canvas.bbox("all"))

    root.update()
    time.sleep(1)  # Pausa de 1 segundo entre cada movimiento

def initialize_maze_canvas():
    global mouse_position, wall_count, place_mouse, place_cheese

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            value = maze[row][col]
            color = 'white'
            if value == 1:
                color = 'black'
                wall_count += 1
            elif value == 2:
                color = 'yellow'
                place_cheese = False
            elif value == 3:
                color = 'red'
                mouse_position = (row, col)
                place_mouse = False
            update_cell(row, col, color)

    update_controls()

def set_place_mode(mode):
    global place_mouse, place_wall, place_cheese
    place_mouse = (mode == 'mouse')
    place_wall = (mode == 'wall')
    place_cheese = (mode == 'cheese')

def export_tree_as_image():
    # Obtener el área del canvas que contiene el árbol
    x0, y0, x1, y1 = search_canvas.bbox("all")
    # Crear una imagen en blanco con el tamaño del área del canvas
    image = Image.new("RGB", (x1 - x0, y1 - y0), "white")
    # Dibujar el contenido del canvas en la imagen
    ps_file = "/Users/juanhoyos/Desktop/tree.ps"
    png_file = "/Users/juanhoyos/Desktop/tree.png"
    search_canvas.postscript(file=ps_file, colormode='color')
    
    # Convertir el archivo PostScript a PNG usando Ghostscript
    try:
        subprocess.run(["gs", "-sDEVICE=pngalpha", "-o", png_file, "-r144", ps_file], check=True)
        print("Árbol exportado como tree.png")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Ghostscript: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Laberinto")

cell_size = 70  # Tamaño de la celda en píxeles

# Canvas para el laberinto
maze_canvas = tk.Canvas(root, width=cell_size*len(maze[0]), height=cell_size*len(maze), bg='white')
maze_canvas.grid(row=1, column=1, padx=10, pady=10)

# Frame y canvas para el árbol de búsqueda con scroll
search_frame = tk.Frame(root)
search_frame.grid(row=1, column=0, padx=100, pady=100)

search_canvas = tk.Canvas(search_frame, width=650, height=650, bg='white')
search_canvas.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(search_frame, orient=tk.VERTICAL, command=search_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

search_canvas.config(yscrollcommand=scrollbar.set)

# Añadir el scrollbar horizontal debajo del canvas
scrollbar_horizontal = tk.Scrollbar(search_frame, orient=tk.HORIZONTAL, command=search_canvas.xview)
scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

search_canvas.config(xscrollcommand=scrollbar_horizontal.set)

search_canvas.config(yscrollcommand=scrollbar.set)

# Cargar la imagen del ratón
mouse_image = Image.open('raton.png')  # Asegúrate de usar una ruta válida

# Configuración de controles
frame_controls = tk.Frame(root)
frame_controls.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

expansions_label = tk.Label(frame_controls, text="Límite de Expansiones:")
expansions_label.grid(row=2, column=0, padx=5, pady=5)

expansions_entry = tk.Entry(frame_controls)
expansions_entry.grid(row=2, column=1, padx=5, pady=5)

start_button = tk.Button(frame_controls, text="Iniciar", command=iniciar_busqueda, state='disabled')
start_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

place_mouse_button = tk.Button(frame_controls, text="Colocar Ratón", command=lambda: set_place_mode('mouse'))
place_mouse_button.grid(row=4, column=0, padx=5, pady=5)

place_wall_button = tk.Button(frame_controls, text="Colocar Pared", command=lambda: set_place_mode('wall'))
place_wall_button.grid(row=4, column=1, padx=5, pady=5)

place_cheese_button = tk.Button(frame_controls, text="Colocar Queso", command=lambda: set_place_mode('cheese'))
place_cheese_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

export_button = tk.Button(frame_controls, text="Exportar Árbol", command=export_tree_as_image)
export_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

initialize_maze_canvas()
maze_canvas.bind("<Button-1>", on_click)

root.mainloop()

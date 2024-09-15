import tkinter as tk
from PIL import Image, ImageTk
from collections import deque
from Node import Nodo
import time

# Definir el laberinto predefinido
maze = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
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

def on_click(event):
    global place_mouse, place_wall, place_cheese, mouse_position, wall_count
    
    row = event.y // cell_size
    column = event.x // cell_size
    
    if place_mouse:
        if mouse_position:
            update_cell(mouse_position[0], mouse_position[1], 'white')
        mouse_position = (row, column)
        update_cell(row, column, 'red', mouse_image)  # Mostrar la imagen del ratón
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
    
    # Borrar el contenido actual de la celda
    maze_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
    
    # Dibujar la imagen si se proporciona
    if image:
        # Redimensionar la imagen para que se ajuste a la celda
        image_resized = image.resize((cell_size, cell_size), Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image_resized)
        maze_canvas.create_image(x1, y1, anchor='nw', image=image_tk)
        # Necesario para mantener la referencia de la imagen en memoria
        maze_canvas.image = image_tk

def iniciar_busqueda():
    limite_expansiones = int(expansions_entry.get())
    if mouse_position:
        busquedaPorAmplitud(maze, mouse_position, limite_expansiones)
    else:
        print("No se ha colocado el ratón")

def pintar_nodos_y_aristas(padre, hijos):
    global level
    if padre.estado not in x_positions:
        x_positions[padre.estado] = 200
        y_positions[padre.estado] = 50 + level * 100

    x1, y1 = x_positions[padre.estado], y_positions[padre.estado]
    search_canvas.create_oval(x1 - 15, y1 - 15, x1 + 15, y1 + 15, fill="blue")
    search_canvas.create_text(x1, y1, text=str(padre.estado), fill="white")

    fila, columna = padre.estado
    maze_canvas.create_rectangle(
        columna * cell_size, fila * cell_size,
        (columna + 1) * cell_size, (fila + 1) * cell_size,
        fill="blue", outline='black'  # Borde negro
    )

    espacio_horiz = 200
    if len(hijos) > 1:
        espacio_horiz = 200 // len(hijos)

    start_x = x1 - ((len(hijos) - 1) * espacio_horiz // 2)

    for i, hijo in enumerate(hijos):
        x_positions[hijo.estado] = start_x + i * espacio_horiz
        y_positions[hijo.estado] = y1 + 100

        x2, y2 = x_positions[hijo.estado], y_positions[hijo.estado]
        search_canvas.create_oval(x2 - 15, y2 - 15, x2 + 15, y2 + 15, fill="red")
        search_canvas.create_text(x2, y2, text=str(hijo.estado), fill="white")

        fila, columna = hijo.estado
        maze_canvas.create_rectangle(
            columna * cell_size, fila * cell_size,
            (columna + 1) * cell_size, (fila + 1) * cell_size,
            fill="red", outline='black'  # Borde negro
        )

        search_canvas.create_line(x1, y1, x2, y2, fill="black")

    root.update()

def initialize_maze_canvas():
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            value = maze[row][col]
            color = 'white'
            if value == 1:
                color = 'black'
            elif value == 2:
                color = 'yellow'
            elif value == 3:
                color = 'red'
            update_cell(row, col, color)

def set_place_mode(mode):
    global place_mouse, place_wall, place_cheese
    place_mouse = (mode == 'mouse')
    place_wall = (mode == 'wall')
    place_cheese = (mode == 'cheese')

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Laberinto")

cell_size = 50  # Tamaño de la celda en píxeles

# Canvas para el laberinto
maze_canvas = tk.Canvas(root, width=cell_size*len(maze[0]), height=cell_size*len(maze), bg='white')
maze_canvas.grid(row=1, column=1, padx=10, pady=10)

# Canvas para el árbol de búsqueda
search_canvas = tk.Canvas(root, width=400, height=400, bg='white')
search_canvas.grid(row=1, column=0, padx=10, pady=10)

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

initialize_maze_canvas()
maze_canvas.bind("<Button-1>", on_click)

root.mainloop()

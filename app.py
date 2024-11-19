import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from collections import deque
from Node import Nodo
import time
import random
import numpy as np
import heapq

# Definir el laberinto predefinido
maze = np.zeros((3, 3))


estado = None
mouse_position = None
wall_count = 0
place_wall = False
expanded_nodes = []

# Variables globales para el dibujo del árbol
x_positions = {}
y_positions = {}
level = 0

def set_estado(value):
    global estado
    estado = value

def busquedaPorAmplitud(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda por amplitud")
    print("estado inicial", estado_inicial)
    cola = deque()
    cola.append(Nodo(estado_inicial, None, None, matriz[estado_inicial[0]][estado_inicial[1]]))

    while cola and len(expanded_nodes) < limite_expansiones:
        node = cola.popleft()
        print("Padre", node)
        expanded_nodes.append(node)
        print(len(expanded_nodes))
        fila, columna = node.estado

        if node.valor == 2:
            print("Encontrado")
            mostrar_modal_queso_encontrado()
            root.destroy()
            break

        # Expandir
        hijos = []
        for movimiento, (df, dc) in {
            "arriba": (-1, 0),
            "derecha": (0, 1),
            "abajo": (1, 0),
            "izquierda": (0, -1)         
        }.items():
            nuevo_fila, nuevo_columna = fila + df, columna + dc
            if 0 <= nuevo_fila < len(matriz) and 0 <= nuevo_columna < len(matriz[0]):
                if matriz[nuevo_fila][nuevo_columna] != 1:
                    nuevo_nodo = Nodo((nuevo_fila, nuevo_columna), node, movimiento, matriz[nuevo_fila][nuevo_columna])
                    print("nuevo nodo", nuevo_nodo)
                    cola.append(nuevo_nodo)
                    hijos.append(nuevo_nodo)

        pintar_nodos_y_aristas(node, hijos)
        root.update()
        time.sleep(1)  # Esperar 1 segundo antes de continuar

    if len(expanded_nodes) >= limite_expansiones:
        print("Límite de expansiones alcanzado")
        print("expansiones", len(expanded_nodes))
        mostrar_modal_no_encontrado()
        expanded_nodes.clear()

def busquedaEnProfundidad(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda en profundidad")
    stack = []
    stack.append(Nodo(estado_inicial, None, None, matriz[estado_inicial[0]][estado_inicial[1]]))

    while stack and len(expanded_nodes) < limite_expansiones:
        node = stack.pop()
        print("Padre", node)
        fila, columna = node.estado
        expanded_nodes.append(node)

        if node.valor == 2:
            print("Encontrado")
            mostrar_modal_queso_encontrado()
            root.destroy()
            break

        # Expandir
        hijos = []
        for movimiento, (df, dc) in {
            "arriba": (-1, 0),
            "derecha": (0, 1),
            "abajo": (1, 0),
            "izquierda": (0, -1),
        }.items():
            nuevo_fila, nuevo_columna = fila + df, columna + dc
            if 0 <= nuevo_fila < len(matriz) and 0 <= nuevo_columna < len(matriz[0]):
                if matriz[nuevo_fila][nuevo_columna] != 1:
                    nuevo_nodo = Nodo((nuevo_fila, nuevo_columna), node, movimiento, matriz[nuevo_fila][nuevo_columna])
                    print("nuevo nodo", nuevo_nodo)
                    stack.append(nuevo_nodo)
                    hijos.append(nuevo_nodo)

        pintar_nodos_y_aristas(node, hijos)
        root.update()
        time.sleep(1)  # Esperar 1 segundo antes de continuar

    if len(expanded_nodes) >= limite_expansiones:
        print("Límite de expansiones alcanzado")
        print("expansiones", len(expanded_nodes))
        mostrar_modal_no_encontrado()
        expanded_nodes.clear()

#Busqueda por costo uniforme
def busquedaPorCostoUniforme(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda por costo uniforme")
    stack = []
    heapq.heappush(stack, (0, Nodo(estado_inicial, None, None, matriz[estado_inicial[0]][estado_inicial[1]])))

    while stack and len(expanded_nodes) < limite_expansiones:
        cost, node = heapq.heappop(stack)
        print("costo", cost)
        print("Padre", node)
        fila, columna = node.estado
        expanded_nodes.append(node)

        if node.valor == 2:
            print("Encontrado")
            mostrar_modal_queso_encontrado()
            root.destroy()
            break

        # Expandir
        hijos = []
        for movimiento, (df, dc) in {
            "arriba": (-1, 0),
            "derecha": (0, 1),
            "abajo": (1, 0),
            "izquierda": (0, -1),
        }.items():
            nuevo_fila, nuevo_columna = fila + df, columna + dc
            # print("nuevo_fila", nuevo_fila)
            # print("nuevo_columna", nuevo_columna)
            if 0 <= nuevo_fila < len(matriz) and 0 <= nuevo_columna < len(matriz[0]):
                if matriz[nuevo_fila][nuevo_columna] != 1:
                    nuevo_nodo = Nodo((nuevo_fila, nuevo_columna), node, movimiento, matriz[nuevo_fila][nuevo_columna])
                    print("nuevo nodo", nuevo_nodo)
                    heapq.heappush(stack, (cost + 1, nuevo_nodo))
                    hijos.append(nuevo_nodo)

        pintar_nodos_y_aristas(node, hijos)
        root.update()
        time.sleep(1)  # Esperar 1 segundo antes de continuar

    if len(expanded_nodes) >= limite_expansiones:
        print("Límite de expansiones alcanzado")
        print("expansiones", len(expanded_nodes))
        mostrar_modal_no_encontrado()
        expanded_nodes.clear()

def busquedaLimitadaPorProfundidad(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda limitada por profundidad")
    profundidad = obtener_profundidad()
    stack = []
    stack.append(Nodo(estado_inicial, None, None, matriz[estado_inicial[0]][estado_inicial[1]]))

    while stack and len(expanded_nodes) < limite_expansiones:
        node = stack.pop()
        #print("Padre", node)
        fila, columna = node.estado
        expanded_nodes.append(node)

        if node.valor == 2:
            #print("Encontrado")
            mostrar_modal_queso_encontrado()
            root.destroy()
            break

        #print(Nodo.profundidad(node), "--profundidad del nodo--")

        if Nodo.profundidad(node) < profundidad:
            # Expandir
            hijos = []
            for movimiento, (df, dc) in {
                "arriba": (-1, 0),
                "derecha": (0, 1),
                "abajo": (1, 0),
                "izquierda": (0, -1),
            }.items():
                nuevo_fila, nuevo_columna = fila + df, columna + dc
                if 0 <= nuevo_fila < len(matriz) and 0 <= nuevo_columna < len(matriz[0]):
                    if matriz[nuevo_fila][nuevo_columna] != 1:
                        nuevo_nodo = Nodo((nuevo_fila, nuevo_columna), node, movimiento, matriz[nuevo_fila][nuevo_columna])
                        print("nuevo nodo", nuevo_nodo)
                        stack.append(nuevo_nodo)
                        hijos.append(nuevo_nodo)
        
        
        pintar_nodos_y_aristas(node, hijos)
        root.update()
        time.sleep(1)  # Esperar 1 segundo antes de continuar
    
    if len(expanded_nodes) >= limite_expansiones:
        #print("Límite de expansiones alcanzado")
        #print("expansiones", len(expanded_nodes))
        mostrar_modal_no_encontrado()
        expanded_nodes.clear()

    
    

def busquedaProfundidadIterativa(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda en profundidad iterativa")
    
    # Obtener la profundidad máxima permitida
    profundidad_maxima = obtener_profundidad()
    print("Profundidad máxima:", profundidad_maxima)
    
    expanded_nodes.clear()  # Reiniciar la lista de nodos expandidos

    # Bucle para incrementar el límite de profundidad
    for limite in range(profundidad_maxima + 1):
        print(f"Profundidad límite: {limite}")
        visitados = set()  # Reiniciar nodos visitados para cada nivel de profundidad
        stack = [(Nodo(estado_inicial, None, None, matriz[estado_inicial[0]][estado_inicial[1]]), 0)]
        
        while stack:
            # Revisar si se ha alcanzado el límite de expansiones
            if len(expanded_nodes) >= limite_expansiones:
                print("Límite de expansiones alcanzado")
                mostrar_modal_no_encontrado()
                expanded_nodes.clear()
                return "No Encontrado"
            
            node, profundidad_actual = stack.pop()
            fila, columna = node.estado

            # Si el estado ya fue visitado en este límite, continuar
            if (fila, columna) in visitados:
                continue

            print("Padre:", node)
            visitados.add((fila, columna))
            expanded_nodes.append(node)

            # Verificar si se encontró el queso
            if node.valor == 2:
                print("Encontrado")
                mostrar_modal_queso_encontrado()
                root.destroy()
                break

            # Expandir nodos hijos si no se ha alcanzado el límite de profundidad
            if profundidad_actual < limite:
                hijos = []
                for movimiento, (df, dc) in {
                    "arriba": (-1, 0),
                    "derecha": (0, 1),
                    "abajo": (1, 0),
                    "izquierda": (0, -1)
                }.items():
                    nuevo_fila, nuevo_columna = fila + df, columna + dc
                    
                    # Verifica si la nueva posición es válida y no es una pared
                    if 0 <= nuevo_fila < len(matriz) and 0 <= nuevo_columna < len(matriz[0]):
                        if matriz[nuevo_fila][nuevo_columna] != 1 and (nuevo_fila, nuevo_columna) not in visitados:
                            nuevo_nodo = Nodo((nuevo_fila, nuevo_columna), node, movimiento, matriz[nuevo_fila][nuevo_columna])
                            print("Nuevo nodo:", nuevo_nodo)
                            stack.append((nuevo_nodo, profundidad_actual + 1))
                            hijos.append(nuevo_nodo)

                # Pintar nodos y aristas en la interfaz
                pintar_nodos_y_aristas(node, hijos)
                root.update()
                time.sleep(1)  # Pausa para visualizar el proceso

    if len(expanded_nodes) >= limite_expansiones:
        #print("Límite de expansiones alcanzado")
        #print("expansiones", len(expanded_nodes))
        mostrar_modal_no_encontrado()
        expanded_nodes.clear()


def busquedaAvara(matriz, estado_inicial, limite_expansiones=2):
    print("Ejecutando búsqueda avara")
    #Obtener la meta de la matriz
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 2:  # Suponiendo que el valor 2 representa la meta
                meta = (i,j)
    
    stack = []
    heapq.heappush(stack, (0, Nodo(estado_inicial, None, None, matriz[estado_inicial[0]][estado_inicial[1]])))

    while stack and len(expanded_nodes) < limite_expansiones:
        heuristic, node = heapq.heappop(stack)
        #print("Padre", node)
        fila, columna = node.estado
        expanded_nodes.append(node)

        if node.valor == 2:
            #print("Encontrado")
            mostrar_modal_queso_encontrado()
            root.destroy()
            break

        # Expandir
        hijos = []

        for movimiento, (df, dc) in {
            "arriba": (-1, 0),
            "derecha": (0, 1),
            "abajo": (1, 0),
            "izquierda": (0, -1),
        }.items():
            nuevo_fila, nuevo_columna = fila + df, columna + dc
            if 0 <= nuevo_fila < len(matriz) and 0 <= nuevo_columna < len(matriz[0]):
                if matriz[nuevo_fila][nuevo_columna] != 1:
                    nuevo_nodo = Nodo((nuevo_fila, nuevo_columna), node, movimiento, matriz[nuevo_fila][nuevo_columna])
                    #print("nuevo nodo", nuevo_nodo)
                    heuristic = abs(nuevo_fila - meta[0]) + abs(nuevo_columna - meta[1])
                    #print("heuristica", heuristic)
                    heapq.heappush(stack, (heuristic, nuevo_nodo))
                    hijos.append(nuevo_nodo)
        
        pintar_nodos_y_aristas(node, hijos)
        root.update()
        time.sleep(1)  # Esperar 1 segundo antes de continuar

    if len(expanded_nodes) >= limite_expansiones:
        #print("Límite de expansiones alcanzado")
        #print("expansiones", len(expanded_nodes))
        mostrar_modal_no_encontrado()
        expanded_nodes.clear()



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
            place_cheese += 1
            update_controls()
    
    print_matrix()

#
def update_controls():
    global place_cheese
    print("place_cheese", place_cheese)
    if mouse_position and place_cheese > 1:
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
busquedas = [busquedaPorAmplitud, busquedaEnProfundidad, busquedaPorCostoUniforme, busquedaLimitadaPorProfundidad, busquedaProfundidadIterativa, busquedaAvara]
busquedas_realizadas = []

def iniciar_busqueda():
    global busquedas_realizadas

    if len(busquedas_realizadas) == len(busquedas):
        print("Todas las búsquedas han sido realizadas")
        mostrar_modal_limite_alcanzado()
        return

    limite_expansiones = int(expansions_entry.get())
    if mouse_position:
        # Seleccionar una búsqueda al azar que no haya sido realizada
        busqueda = random.choice([b for b in busquedas if b not in busquedas_realizadas])
        busquedas_realizadas.append(busqueda)
        # Actualizar la etiqueta con el nombre del algoritmo de búsqueda
        algoritmo_label.config(text=f"Algoritmo de búsqueda: {busqueda.__name__}")
        busqueda(maze, mouse_position, limite_expansiones)

    else:
        print("No se ha colocado el ratón")

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
        espacio_horiz = max(200 // len(hijos), 200)  # Ajustar el espacio mínimo entre nodos

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

# Función para mostrar el modal y obtener la profundidad
def obtener_profundidad():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    profundidad = simpledialog.askinteger("Profundidad", "Ingrese la profundidad:")
    root.destroy()
    return profundidad

# Función para mostrar el modal
def mostrar_modal_queso_encontrado():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    messagebox.showinfo("Información", "Queso encontrado")
    root.destroy()

def mostrar_modal_limite_alcanzado():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    messagebox.showinfo("Información", "El queso no pudo ser encontrado. Límite de expansiones alcanzado")
    root.destroy()

def mostrar_modal_no_encontrado():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    messagebox.showinfo("Información", "El queso no pudo ser encontrado, cambio de busqueda")
    root.destroy()

def initialize_maze_canvas(rows=None, columns=None):
    global maze, mouse_position, wall_count, place_mouse, place_cheese

    if rows and columns:
        maze = np.zeros((rows, columns))
    
    mouse_position = None
    wall_count = 0
    place_cheese = False
    

    maze_canvas.config(width=cell_size*len(maze[0]), height=cell_size*len(maze))
    maze_canvas.delete("all")

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

def generate_maze(rows, columns):
    initialize_maze_canvas(rows, columns)

def set_place_mode(mode):
    global place_mouse, place_wall, place_cheese
    place_mouse = (mode == 'mouse')
    place_wall = (mode == 'wall')
    place_cheese = (mode == 'cheese')



# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Laberinto")

cell_size = 70  # Tamaño de la celda en píxeles

# Canvas para el laberinto sin scrollbar
maze_canvas = tk.Canvas(root, width=cell_size*len(maze[0]), height=cell_size*len(maze), bg='white')
maze_canvas.grid(row=1, column=1, padx=10, pady=10)

# Frame y canvas para el árbol de búsqueda con scroll
search_frame = tk.Frame(root)
search_frame.grid(row=1, column=0, padx=10, pady=10)

# Crear una etiqueta para mostrar el algoritmo de búsqueda
algoritmo_label = tk.Label(root, text="Algoritmo de búsqueda: Ninguno")
algoritmo_label.grid(row=2, column=0, padx=10, pady=10)

search_canvas = tk.Canvas(search_frame, width=650, height=650, bg='white')
search_canvas.grid(row=0, column=0)

# Scrollbar vertical
scrollbar = tk.Scrollbar(search_frame, orient=tk.VERTICAL, command=search_canvas.yview)
scrollbar.grid(row=0, column=1, sticky='ns')

search_canvas.config(yscrollcommand=scrollbar.set)

# Scrollbar horizontal
scrollbar_x = tk.Scrollbar(search_frame, orient=tk.HORIZONTAL, command=search_canvas.xview)
scrollbar_x.grid(row=1, column=0, sticky='ew')

search_canvas.config(xscrollcommand=scrollbar_x.set)

# Cargar la imagen del ratón
mouse_image = Image.open('raton.png')  # Asegúrate de usar una ruta válida

# Configuración de controles
frame_controls = tk.Frame(root)
frame_controls.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Agregar entradas para filas y columnas
rows_label = tk.Label(frame_controls, text="Filas:")
rows_label.grid(row=0, column=0, padx=5, pady=5)

rows_entry = tk.Entry(frame_controls)
rows_entry.grid(row=0, column=1, padx=5, pady=5)

columns_label = tk.Label(frame_controls, text="Columnas:")
columns_label.grid(row=1, column=0, padx=5, pady=5)

columns_entry = tk.Entry(frame_controls)
columns_entry.grid(row=1, column=1, padx=5, pady=5)

# Botón para generar el laberinto
generate_maze_button = tk.Button(frame_controls, text="Generar Laberinto", command=lambda: generate_maze(int(rows_entry.get()), int(columns_entry.get())))
generate_maze_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

expansions_label = tk.Label(frame_controls, text="Límite de Expansiones:")
expansions_label.grid(row=2, column=0, padx=5, pady=5)

expansions_entry = tk.Entry(frame_controls)
expansions_entry.grid(row=2, column=1, padx=5, pady=5)

start_button = tk.Button(frame_controls, text="Iniciar", command=iniciar_busqueda, state='disabled')
start_button.grid(row=3, column=0, padx=5, pady=5)

place_mouse_button = tk.Button(frame_controls, text="Colocar Ratón", command=lambda: set_place_mode('mouse'))
place_mouse_button.grid(row=4, column=0, padx=5, pady=5)

place_wall_button = tk.Button(frame_controls, text="Colocar Pared", command=lambda: set_place_mode('wall'))
place_wall_button.grid(row=4, column=1, padx=5, pady=5)

place_cheese_button = tk.Button(frame_controls, text="Colocar Queso", command=lambda: set_place_mode('cheese'))
place_cheese_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

initialize_maze_canvas()
maze_canvas.bind("<Button-1>", on_click)

root.mainloop()

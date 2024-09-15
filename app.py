import tkinter as tk
import time

# Dimensiones iniciales de la matriz
ROWS = 4
COLS = 4
CELL_SIZE = 50
TREE_X_START = 200  # Ajustar la posición inicial del árbol
TREE_Y_START = 100
NODE_RADIUS = 15  # Reducir el tamaño de los nodos

# Definición inicial del laberinto (0 = camino, 1 = pared)
maze = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# Crear la ventana principal
root = tk.Tk()
root.title("Laberinto Dinámico y Árbol Binario")

# Crear el lienzo donde se dibujarán el laberinto y el árbol
canvas = tk.Canvas(root, width=1000, height=600)
canvas.pack()

# Crear etiquetas y entradas de texto para fila y columna
label_row = tk.Label(root, text="Fila:")
label_row.place(x=500, y=10)
entry_row = tk.Entry(root, width=5)
entry_row.place(x=550, y=10)

label_col = tk.Label(root, text="Columna:")
label_col.place(x=610, y=10)
entry_col = tk.Entry(root, width=5)
entry_col.place(x=670, y=10)

label_expansions = tk.Label(root, text="N. de expansiones:")
label_expansions.place(x=500, y=40)
entry_expansions = tk.Entry(root, width=10)
entry_expansions.place(x=650, y=40)

# Crear un botón centrado debajo del laberinto
button_width = 80  # Ancho del botón
maze_x_start = 500  # Posición inicial del laberinto
button_x = maze_x_start + (COLS * CELL_SIZE - button_width) / 2

def create_maze():
    """Dibuja el laberinto en el lado derecho del lienzo."""
    for i in range(ROWS):
        for j in range(COLS):
            x1 = maze_x_start + j * CELL_SIZE
            y1 = i * CELL_SIZE + 70  # Ajustar la posición y para dejar espacio para las entradas de texto
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            if maze[i][j] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill="black")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

def on_button_click():
    global ROWS, COLS, maze
    try:
        ROWS = int(entry_row.get())
        COLS = int(entry_col.get())
    except ValueError:
        print("Por favor, ingrese valores válidos para filas y columnas.")
        return

    # Crear un nuevo laberinto con las dimensiones especificadas
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            maze[i][j] = 1 if (i + j) % 2 == 0 else 0  # Ejemplo de generación de laberinto

    # Limpiar el lienzo y redibujar el laberinto
    canvas.delete("all")
    create_maze()
    draw_tree()  # Redibujar el árbol después de limpiar el lienzo

    # Recalcular la posición del botón después de redibujar el laberinto
    button_y = ROWS * CELL_SIZE + 80 + 70
    button.place(x=button_x, y=button_y)

button = tk.Button(root, text="Iniciar", command=on_button_click)
button.place(x=button_x, y=ROWS * CELL_SIZE + 80 + 70)  # Ajustar la posición y para dejar espacio para las entradas de texto

def draw_node(x, y, value):
    """Dibuja un nodo del árbol en las coordenadas (x, y) con el valor dado."""
    # Color del nodo basado en el valor
    color = "lightblue" if value % 2 == 0 else "lightgreen"
    
    # Dibuja el nodo y el valor
    canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill=color)
    canvas.create_text(x, y, text=str(value), font=("Arial", 10, "bold"))

def draw_edge(x1, y1, x2, y2):
    """Dibuja una arista entre dos nodos."""
    canvas.create_line(x1, y1, x2, y2)

def draw_tree():
    """Dibuja un árbol binario simple en tiempo real, conectando los nodos con aristas."""
    nodes = [(TREE_X_START, TREE_Y_START, 1)]  # Lista de nodos: (x, y, valor)
    offset_x = 75  # Reducir el desplazamiento x para un árbol más compacto
    offset_y = 75  # Reducir el desplazamiento y

    current_value = 1  # Valor inicial del primer nodo

    while nodes:
        x, y, _ = nodes.pop(0)
        draw_node(x, y, current_value)
        canvas.update()
        time.sleep(1)  # Espera 1 segundo entre la creación de nodos

        # Actualizar el valor para el siguiente nodo
        current_value += 1

        # Dibujar los hijos del nodo actual
        if current_value <= 7:  # Máximo valor de un nodo en este ejemplo
            left_child = (x - offset_x, y + offset_y, current_value)  # Hijo izquierdo
            current_value += 1
            right_child = (x + offset_x, y + offset_y, current_value)  # Hijo derecho
            
            # Conectar con aristas
            draw_edge(x, y, left_child[0], left_child[1])
            draw_edge(x, y, right_child[0], right_child[1])
            canvas.update()

            nodes.append(left_child)
            nodes.append(right_child)

        offset_x /= 2  # Reducir el desplazamiento x para niveles más profundos

# Llamar a la función para crear el laberinto
create_maze()

# Dibujar el árbol binario
draw_tree()

# Ejecutar la aplicación
root.mainloop()

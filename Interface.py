import tkinter as tk
from PIL import Image, ImageTk

class InterfazLaberinto:
    def __init__(self, root, maze, arbol_busqueda=None):
        self.root = root
        self.maze = maze
        self.arbol_busqueda = arbol_busqueda
        self.mouse_position = None
        self.wall_count = 0
        self.place_mouse = False
        self.place_wall = False
        self.place_cheese = False

        self.cell_size = 50  # Tamaño de la celda en píxeles

        # Crear canvas del laberinto
        self.maze_canvas = tk.Canvas(root, width=self.cell_size * len(maze[0]), height=self.cell_size * len(maze), bg='white')
        self.maze_canvas.grid(row=1, column=0, padx=10, pady=10)  # Columna 0 para el laberinto

        # Crear un frame para el árbol de búsqueda (canvas independiente)
        self.search_canvas_frame = tk.Frame(root)
        self.search_canvas_frame.grid(row=1, column=1, padx=10, pady=10)  # Columna 1 para el árbol de búsqueda
        
        if arbol_busqueda:
            self.asignar_arbol_busqueda(arbol_busqueda)

        self.mouse_image = Image.open('raton.png')  # Imagen del ratón
        self.crear_controles()
        self.inicializar_laberinto()

    def crear_controles(self):
        frame_controls = tk.Frame(self.root)
        frame_controls.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(frame_controls, text="Límite de Expansiones:").grid(row=2, column=0, padx=5, pady=5)
        self.expansions_entry = tk.Entry(frame_controls)
        self.expansions_entry.grid(row=2, column=1, padx=5, pady=5)

        self.start_button = tk.Button(frame_controls, text="Iniciar", command=self.iniciar_busqueda, state='disabled')
        self.start_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        tk.Button(frame_controls, text="Colocar Ratón", command=lambda: self.set_place_mode('mouse')).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(frame_controls, text="Colocar Pared", command=lambda: self.set_place_mode('wall')).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(frame_controls, text="Colocar Queso", command=lambda: self.set_place_mode('cheese')).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def inicializar_laberinto(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                self.actualizar_celda(row, col, 'white')

        self.maze_canvas.bind("<Button-1>", self.on_click)

    def set_place_mode(self, mode):
        self.place_mouse = (mode == 'mouse')
        self.place_wall = (mode == 'wall')
        self.place_cheese = (mode == 'cheese')

    def on_click(self, event):
        row = event.y // self.cell_size
        column = event.x // self.cell_size

        if self.place_mouse:
            if self.mouse_position:
                self.actualizar_celda(self.mouse_position[0], self.mouse_position[1], 'white')
            self.mouse_position = (row, column)
            self.actualizar_celda(row, column, None, self.mouse_image)
            self.maze[row][column] = 3
            self.place_mouse = False

        elif self.place_wall:
            if self.maze[row][column] == 0:
                self.maze[row][column] = 1
                self.wall_count += 1
                self.actualizar_celda(row, column, 'black')

        elif self.place_cheese:
            if self.maze[row][column] == 0:
                self.maze[row][column] = 2
                self.actualizar_celda(row, column, 'yellow')
                self.place_cheese = False

        self.actualizar_controles()

    def actualizar_controles(self):
        if self.mouse_position and self.wall_count > 1:
            self.start_button.config(state='normal')
        else:
            self.start_button.config(state='disabled')

    def actualizar_celda(self, row, column, color, image=None):
        x1 = column * self.cell_size
        y1 = row * self.cell_size
        x2 = (column + 1) * self.cell_size
        y2 = (row + 1) * self.cell_size

        if color:
            self.maze_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
        elif image:
            img = ImageTk.PhotoImage(self.mouse_image.resize((self.cell_size, self.cell_size)))
            self.maze_canvas.create_image(x1, y1, anchor=tk.NW, image=img)
            self.mouse_img_cache = img  # Necesario para que no se borre la imagen

    def iniciar_busqueda(self):
        limite_expansiones = int(self.expansions_entry.get())
        self.arbol_busqueda.busqueda_por_amplitud(self.maze, self.mouse_position, limite_expansiones)

    def asignar_arbol_busqueda(self, arbol_busqueda):
        """Asigna el arbol de búsqueda después de la inicialización."""
        self.arbol_busqueda = arbol_busqueda
        self.search_canvas = arbol_busqueda.search_canvas
        self.search_canvas.pack(in_=self.search_canvas_frame, fill=tk.BOTH, expand=True)  # Añadir el canvas del árbol de búsqueda dentro del frame
        self.search_canvas_frame.update()  # Actualizar el frame para que se ajuste al tamaño del canvas
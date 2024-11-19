class Nodo:
    def __init__(self, estado, padre=None, operador=None, valor=None):
        self.estado = estado
        self.padre = padre
        self.operador = operador
        self.valor = valor

    def __repr__(self):
        return f"(estado={self.estado}, Padre={self.padre}, Operador={self.operador}, valor={self.valor})"

    # Para comparar nodos    
    def __lt__(self, other):
        return self.valor < other.valor
    
    #Saber profundidad del nodo
    def profundidad(self):
        if self.padre == None:
            return 0
        else:
            return 1 + self.padre.profundidad()


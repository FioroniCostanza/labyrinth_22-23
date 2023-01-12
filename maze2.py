from collections import defaultdict
from PIL import Image

def dfs(maze, start, end):
    # Crea una matrice per tracciare se una cella è stata visitata
    visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    # Crea una pila per tenere traccia dei nodi da visitare
    stack = [start]
    # Crea un dizionario per tenere traccia dei percorsi
    paths = defaultdict(list)
    paths[start] = []
    # Fai un ciclo finché la pila non è vuota
    while stack:
        node = stack.pop()
        x, y = node
        # Se il nodo corrente è il punto di arrivo, aggiungi il percorso corrente al dizionario dei percorsi
        if node == end:
            paths[end] = paths[node] + [end]
            continue
        # Marcamos la celula come visitata
        visited[x][y] = True
        # Visitiamo i nodi non visitati adiacenti
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if is_valid_move(maze, x+dx, y+dy, visited):
                stack.append((x+dx, y+dy))
                paths[(x+dx, y+dy)] = paths[node] + [(x+dx, y+dy)]           
    return paths[end]

def is_valid_move(maze, x, y, visited):
    # Controlla se la mossa è valida (non fuori dai confini del labirinto e non è una parete)
    return (0 <= x < len(maze)) and (0 <= y < len(maze[0])) and (maze[x][y] != "#") and (not visited[x][y])

def image_to_maze(filepath):
    # Apre l'immagine del labirinto
    image = Image.open(filepath)
    # Converte l'immagine in una matrice di pixel
    pixels = image.load()
    # Crea una matrice vuota per il labirinto
    maze = [] 
    # Scansiona i pixel dell'immagine per creare la matrice del labirinto
    # S = inizio, E = fine, # = muro, . = cammino
    for i in range(image.height):
        maze_row = []
        for j in range(image.width):
            pixel = pixels[j, i]
            if pixel == (255, 255, 255): # Pixel bianco
                maze_row.append(".") # cammino
            elif pixel == (0, 0, 0): # Pixel nero
                maze_row.append("#") # muro
            elif pixel == (255, 0, 0): # Pixel rosso
                maze_row.append("E") # inizio
                end = (i, j)
            elif pixel == (0, 255, 0): # Pixel verde
                maze_row.append("S") # fine
                start = (i, j)
        maze.append(maze_row)
    return maze, start, end


def draw_path(filepath, path):
    # Apre l'immagine del labirinto
    image = Image.open(filepath)
    pixels = image.load()
    # Disegna il percorso sul labirinto
    for x, y in path[1,(len(path)-1)]:
        pixels[y, x] = (0, 0, 255) # Assegniamo un colore blu
    # Salva l'immagine con il percorso
    image.save("path_maze.tiff")
    
# Esempio di utilizzo
filepath = "maze.tiff"
maze, start, end = image_to_maze(filepath)
path = dfs(maze, start, end)
draw_path(drawpath, path)

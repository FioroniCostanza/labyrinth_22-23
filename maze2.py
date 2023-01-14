from collections import defaultdict
from PIL import Image

def find_all_paths(maze, start, end):
    # Creiamo una pila vuota per tener traccia dei percorsi
    stack = []
    # Iniziamo con un percorso vuoto
    stack.append([start])
    # Creiamo una lista vuota per tener traccia dei percorsi completi
    paths = []
    # Continuiamo a cercare percorsi finché la pila non è vuota
    while stack:
        # Prendiamo il primo percorso dalla pila
        path = stack.pop()
        # Otteniamo la posizione corrente dal percorso
        curr_pos = path[-1]
        # Se la posizione corrente è uguale alla posizione di arrivo, aggiungiamo il percorso alla lista dei percorsi completi
        if curr_pos == end:
            paths.append(path)
        # Altrimenti, esploriamo le posizioni adiacenti
        else:
            # Per ogni posizione adiacente alla posizione corrente
            for next_pos in get_adjacent_positions(maze, curr_pos):
                # Se la posizione adiacente non è già stata visitata
                if next_pos not in path:
                    # Creiamo un nuovo percorso che include la posizione adiacente
                    new_path = list(path)
                    new_path.append(next_pos)
                    # Aggiungiamo il nuovo percorso alla pila
                    stack.append(new_path)
    # Restituiamo tutti i percorsi completi
    return paths

def get_adjacent_positions(maze, pos):
    x, y = pos
    adjacent_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    valid_positions = []
    for i,j in adjacent_positions:
        if i>=0 and j>=0 and i<len(maze) and j<len(maze[0]) and maze[i][j]=='.':
            valid_positions.append((i,j))
    return valid_positions

def image_to_maze(filepath):
    # Apre l'immagine del labirinto
    image = Image.open(filepath)
    # Converte l'immagine in una matrice di pixel
    pixels = image.load()
    # Crea una matrice vuota per il labirinto
    maze = [] 
    start = []
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
                maze_row.append(".") # inizio
                end = (i, j)
            elif pixel == (0, 255, 0): # Pixel verde
                maze_row.append(".") # fine
                start.append((i, j))
            else:
                maze_row.append(".") # fine
        maze.append(maze_row)
    return maze, start, end


def draw_path(filepath, paths,index):
    colors = [(0,255,255),(255,0,255),(0,128,0),(128,0,128),(255,255,0),(192,192,192)]
    name = filepath.split('.')[0] + '_start_' + str(index)
    for i,path in zip(range(len(paths)),paths):
        # Apre l'immagine del labirinto
        image = Image.open(filepath)
        pixels = image.load()
        # Disegna il percorso sul labirinto
        for x, y in path[1:(len(path)-1)]:
            pixels[y, x] = colors[index] # Assegniamo un colore blu
            # Salva l'immagine con il percorso
        image.save(f'./Percorsi/{name}_path_{i+1}.tiff')
    
# Esempio di utilizzo
filepath = "maze3.tiff"
maze, start, end = image_to_maze(filepath)
paths = []
for i in range(len(start)):
    paths.append(find_all_paths(maze, start[i], end))
    draw_path(filepath, paths[i],i)



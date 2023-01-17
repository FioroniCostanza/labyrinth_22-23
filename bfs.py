from PIL import Image
from collections import deque
import os

def image_to_mazes(filepath):
    """
    Questa funzione trasforma l'immagine in ingresso in una matrice
    costituita da:

        - 0 se il colore RGB dei pixel è bianco, verde o rosso.

        - 1 se il colore RGB dei pixel è nero, quindi rappresenta il muro del
          labirinto

        - un numero da 1 a 15 se il colore RGB è una tonalità di grigio, rappresentando in questo
          modo il peso di una casella

    Parameters
    ----------
    filepath : str

    Returns
    -------
    maze : list
        È una matrice che rappresenta l'immagine di partenza.
    start : list
        È una lista delle coordinate di tutte le caselle verdi (punti di partenza)
        N.B. Si utilizza una lista e non una tupla per considerare la possibilità di molteplici punti di partenza

    end : tuple
        È una tupla contenente le coordinate della casella rossa (punto di arrivo)

    """
    # Apre l'immagine del labirinto e converte l'immagine in una matrice di pixel
    image = Image.open(filepath)
    pixels = image.load()
    # Inizializziamo il labirinto e la matrice contenente le posizioni di partenza
    maze = []
    start = []
    # Scansiona i pixel dell'immagine per creare la matrice del labirinto
    for i in range(image.height):
        # Inizializzo per ogni riga una matrice di 0 e -1 a seconda che il pixel sia percorribile o meno
        maze_row = []
        for j in range(image.width):
            pixel = pixels[j, i]
            if pixel == (255, 255, 255):  # Pixel bianco
                maze_row.append(0)
            elif pixel == (0, 0, 0):  # Pixel nero
                maze_row.append(-1)
            elif pixel == (0, 255, 0):  # Pixel verde
                maze_row.append(0)
                start.append((i, j))
            elif pixel == (255, 0, 0):  # Pixel rosso
                maze_row.append(0)
                end = (i, j)
            else:
                # utilizziamo il valore dei pixel grigi come peso di tali pixel
                maze_row.append(pixel[0] // 16)
        maze.append(maze_row)
    return maze, start, end

def find_shortest_path(maze, start, end, max_search_depth=None):
    """
   Questa funzione svolge una ricerca del percorso più breve all'interno del 
   labirinto, utilizzando l'algoritmo bread-first search.
   Dando in ingresso il labirinto, il punto di partenza e il punto di arrivo, 
   la funzione restituirà il percorso più breve possibile. 
   
   Parameters
   ----------
   maze : list
       È una matrice che rappresenta l'immagine di partenza.
   start : tuple
       Indica la posizione di partenza.
   end : tuple
       Indica la posizione di arrivo.
   max_search_depth : int
       È una soglia per limitare la ricerca del percorso, se un percorso supera 500
       caselle di lunghezza smette di analizzarlo, in quanto, per i casi in esame, sicuramente non sarà il più breve.
       
   Returns
   -------
   paths : list 
       Restituisce il percorso trovato tra partenza e arrivo.
   """

    # Creiamo una coda e la inizializziamo con la posizione di partenza
    queue = deque()
    queue.append([start])
    # Creiamo una lista vuota per tener traccia dei percorsi completi
    paths = []
    # Creiamo un dizionario per tener traccia delle posizioni visitate e segniamo subito la partenza come posizione visitata
    visited = {start: True}
    # Continuiamo a cercare percorsi finché la coda non è vuota
    while queue:
        # Prendiamo il primo percorso dalla coda, poiché la coda è una lista di liste, il primo elemento sarà l'intero percorso, per cui
        # il percorso viene salvato nella variabile path e queue diventa una variabile deque contenente una lista vuota
        path = queue.popleft()
        # Otteniamo la posizione corrente dal percorso
        curr_pos = path[-1]
        # Se la posizione corrente è uguale alla posizione di arrivo, aggiungiamo il percorso alla lista dei percorsi completi
        if curr_pos == end:
            paths.append(path)
        # Altrimenti, esploriamo le posizioni adiacenti
        else:
            # Se la profondità massima della ricerca è stata raggiunta, non esploriamo ulteriormente
            if max_search_depth and len(path) >= max_search_depth:
                continue
            # Per ogni posizione adiacente alla posizione corrente
            for next_pos in get_adjacent_positions(maze, curr_pos):
                # Se la posizione adiacente non è già stata visitata segniamo la posizione adiacente come visitata
                if next_pos not in visited:
                    visited[next_pos] = True
                    # Creiamo un nuovo percorso che include la posizione adiacente e lo inseriamo come nuova coda
                    new_path = list(path)
                    new_path.append(next_pos)
                    queue.append(new_path)
    return paths

def get_adjacent_positions(maze, pos):
    """
    Questa funzione verifica che le 4 posizioni vicine alla posizione corrente 
    siano uno spazio percorribile e non un muro. 
    Parameters
    ----------
    maze : list
        È una matrice che rappresenta l'immagine di partenza.
    pos : tuple
        Rappresenta la casella di cui valutare le posizioni adiacenti.
    Returns
    -------
    valid_positions : list
        Restituisce tutte le caselle in cui è possibile spostarsi.
    """
    x, y = pos
    adjacent_positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    valid_positions = []
    for i,j in adjacent_positions:
        if i>=0 and j>=0 and i<len(maze) and j<len(maze[0]) and maze[i][j]!=-1:
            valid_positions.append((i,j))
    return valid_positions

def draw_path(filepath, paths, index, maze):
    """
    Questa funzione colora sull'immagine del labirinto di partenza i percorsi possibili, colorandoli
    in maniera differente per ogni punto di partenza e salvandoli in immagini
    diverse per ogni percorso.
    
    Parameters
    ----------
    filepath : str
        
    paths : list
        Lista di tutte i percorsi che partono da una stessa casella di partenza.
        
    index : int
        Un intero che rappresenta a quale casella di partenza fà riferimento il percorso.
    Returns
    -------
    None.
    """
    colors = [(0,255,255),(255,0,255),(0,128,0),(128,0,128),(255,255,0),(192,192,192)]
    peso = []
    name = filepath.split('.')[0] + '_start_' + str(index)
    for i,path in zip(range(len(paths)),paths):
        peso.append(weight(maze,path))
        image = Image.open(filepath)
        pixels = image.load()
        # Disegna il percorso sul labirinto (si prende da 1 a len(path)-1 per evitare di cambiare colore a partenza e arrivo)
        for x, y in path[1:(len(path)-1)]:
            pixels[y, x] = colors[index] # Assegniamo un colore ai pixel che compongono il percorso (a seconda della posizione di partenza)
        if not os.path.exists('Percorsi'):
            os.makedirs('Percorsi')
        os.path.join('Percorsi', f'{name}_path_{i+1}.tiff')
    return peso
        
def weight(maze, path):
    """
   Questa funzione calcola il costo totale per ogni percorso possibile, 
   sommando il peso di ogni casella percorsa.
   Parameters
   ----------
   maze : list
       E' una matrice che rappresenta l'immagine di partenza.
   paths : list
       Lista di tutte le caselle da visitare per completare il percorso.
   Returns
   -------
   weight : int
       Un intero che rappresenta il peso del percorso.
   """
    weight = 0
    for pos in path:
        x, y = pos
        weight += maze[x][y]
    return weight


filepath = "20-10_marked.tiff"
maze, start, end = image_to_mazes(filepath)
paths = []
peso = []
for i in range(len(start)):
    paths.append(find_shortest_path(maze, start[i], end, 500))
    peso.append(draw_path(filepath, paths[i], i, maze))

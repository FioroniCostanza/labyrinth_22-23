from PIL import Image
import heapq, os

def find_shortest_path_by_weight(maze, start, end):
    """
   Questa funzione svolge una ricerca del percorso a peso minimo all'interno del 
   labirinto, utilizzando l'algoritmo di Dijkstra.
   Dando in ingresso il labirinto, il punto di partenza e il punto di arrivo, 
   la funzione restituirà una lista con tutte le tuple da percorrere tra Start
   ed end. 
   
   Parameters
   ----------
   maze : list
       E' una matrice che rappresenta l'immagine di partenza.
   start : list
       Indica la posizione di partenza.
   end : tuple
       Indica la posizione di arrivo.
   Returns
   -------
   paths : list 
       Restituisce il percorso a peso minimo trovati tra partenza e arrivo.
   """
    # Creiamo una coda vuota per tener traccia dei percorsi
    queue = []
    # Iniziamo l'algoritmo con il primo nodo e un peso di 0
    # Iniziamo anche la lista del percorso con solo il primo nodo
    heapq.heappush(queue, (0, start, [start]))
    
    # Creiamo un dizionario per tenere traccia dei nodi visitati con il loro peso minimo
    visited = {start: 0}
    
    # Creiamo una variabile per tener traccia del peso totale del percorso
    weight_tot = None
    
    # Fintanto che ci sono nodi nella coda
    while queue:
        # Prendiamo l'elemento a peso minimo dalla coda e lo assegniamo alle variabili curr_weight, curr_pos e path
        curr_weight, curr_pos, path = heapq.heappop(queue)
        # Se il nodo corrente è quello finale
        if curr_pos == end:
            # Assegniamo il peso totale e ritorniamo il percorso
            weight_tot = curr_weight
            return path, weight_tot
        # Per ogni posizione adiacente al nodo corrente 
        for next_pos, weight in get_adjacent_positions_with_weight(maze, curr_pos):
            # Se la posizione adiacente non è stata visitata
            if next_pos not in visited:
                # Calcoliamo il nuovo peso totale
                new_weight = curr_weight + weight
                # Aggiungiamo la posizione adiacente al dizionario dei nodi visitati
                visited[next_pos] = new_weight
                # Creiamo una nuova lista del percorso con la posizione adiacente
                new_path = list(path)
                new_path.append(next_pos)
                # Inseriamo la posizione adiacente con il nuovo peso totale e il nuovo percorso nella coda
                heapq.heappush(queue, (new_weight, next_pos, new_path))
    # Se non ci sono stati percorsi validi, ritorniamo None
    return None, weight_tot

def get_adjacent_positions_with_weight(maze, pos):
    """
    Questa funzione verifica che le 4 posizioni vicine alla posizione corrente 
    siano uno spazio percorribile e non un muro. 
    Parameters
    ----------
    maze : list
        E' una matrice che rappresenta l'immagine di partenza.
    pos : tuple
        Rappresenta la casella di cui valutare le adiacenti.
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
            valid_positions.append(((i,j),maze[i][j]))
    return valid_positions
            
def image_to_mazes(filepath):
    """
    Questa funzione trasforma l'immagine in ingresso in una matrice 
    cositituita da:
        
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
        E' una matrice che rappresenta l'immagine di partenza.
    start : list
        E' una lista delle coordinate di tutte le caselle verdi (punti di partenza)
    end : list
        E' una lista con le coordinate di tutte le caselle rosse (punti di arrivo)
    """
    # Apre l'immagine del labirinto
    image = Image.open(filepath)
    # Converte l'immagine in una matrice di pixel
    pixels = image.load()
    # Crea una matrice vuota per il labirinto
    maze = [] 
    # Inizializziamo start come lista vuota
    start = []
    end = ()
    # Scansiona i pixel dell'immagine per creare la matrice del labirinto
    for i in range(image.height):
        maze_row = []
        for j in range(image.width):
            pixel = pixels[j, i]
            # convertiamo il pixel in un numero
            if pixel == (255, 255, 255): # Pixel bianco
                maze_row.append(0) # cammino
            elif pixel == (0, 0, 0): # Pixel nero
                maze_row.append(-1) # muro
            elif pixel == (0, 255, 0): # Pixel verde
                maze_row.append(0) # inizio
                start.append((i, j))
            elif pixel == (255, 0, 0): # Pixel rosso
                maze_row.append(0) # fine
                end = (i, j)
            else:
                # utilizziamo il valore del pixel come peso
                maze_row.append(pixel[0] // 16)
        maze.append(maze_row)
    return maze, start, end

def draw_path(filepath, paths,index,maze):
    """
    Questa funzione colora sull' immagine del labirinto di partenza i percorsi possibili, colorandoli
    in maniera differente per ogni punto di partenza e salvandoli in immagini
    diverse per ogni percorso.
    
    Parameters
    ----------
    filepath : str
        
    paths : list
        Lista di tutte i percorsi che partono da una stessa casella di partenza.
        
    index : list
        Un intero che rappresenta a quale casella di partenza fà riferimento il percorso.
    Returns
    -------
    None.
    """
    colors = [(0,255,255),(255,0,255),(0,128,0),(128,0,128),(255,255,0),(192,192,192)]
    name = filepath.split('.')[0] + '_start_' + str(index)
    # peso.append(weight(maze,path))
    # Apre l'immagine del labirinto
    image = Image.open(filepath)
    pixels = image.load()
    # Disegna il percorso sul labirinto
    for x, y in path[1:(len(path)-1)]:
        pixels[y, x] = colors[index] # Assegniamo un colore blu
        # Salva l'immagine con il percorso
    if not os.path.exists('Percorsi'):
        os.makedirs('Percorsi')
    image.save(f'./Percorsi/{name}_path_{i+1}_dijkstra.tiff')
    
    
# Esempio di utilizzo
filepath = "./indata/20-10_marked.tiff"
maze, start, end = image_to_mazes(filepath)
paths = []
peso = []
for i in range(len(start)):
    path, weight = find_shortest_path_by_weight(maze, start[i], end)
    paths.append(path)
    peso.append(weight)

for i in range(len(start)):
    draw_path(filepath, paths[i],i,maze)        
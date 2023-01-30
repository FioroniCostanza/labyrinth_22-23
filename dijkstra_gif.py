from PIL import Image
import heapq
import json
import os
import copy
import imageio

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
   # Iniziamo l'algoritmo con il primo nodo, con un peso pari a 0
   # e inizializziamo il percorso inserendo al suo interno solo il primo nodo
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
            # Assegniamo il peso totale e restituiamo il percorso ottenuto
            weight_tot = curr_weight
            return path, weight_tot
        # Altrimenti, per ogni posizione adiacente al nodo corrente si verifica se esse siano state già visitate
        for next_pos, weight in get_adjacent_positions(maze, curr_pos):
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
    # Se non ci sono percorsi validi, ritorna un valore nullo (None)
    return None, weight_tot

def get_adjacent_positions(maze, pos):
    """
    Questa funzione verifica quali tra le 4 posizioni adiacenti alla posizione corrente 
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
            
def image_to_maze(image):
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
    image : image file
    
    Returns
    -------
    maze : list
        E' una matrice che rappresenta l'immagine di partenza.
    start : list
        E' una lista delle coordinate di tutte le caselle verdi (punti di partenza)
    end : tuple
        E' una lista con le coordinate di tutte le caselle rosse (punti di arrivo)
    image: TiffImageFile
        E' l'immagine ottenuta da filepath.
    """
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
            # convertiamo il pixel in un numero, -1 se è un muro, 0 altrimenti
            if pixel == (255, 255, 255):
                maze_row.append(0) # cammino
            elif pixel == (0, 0, 0): # Pixel nero
                maze_row.append(-1) # muro
            elif pixel == (0, 255, 0): # Pixel verde
                maze_row.append(0) # inizio
                start.append((i, j))
            elif pixel == (255, 0, 0): # Pixel rosso
            # il rosso viene importato come (254,0,0) nel caso di una jpg
                maze_row.append(0) # fine
                end = (i, j)
            elif pixel[0] == pixel[1] == pixel[2]:
                # in tal caso utilizziamo il valore del pixel come peso
                # infatti i pixel grigi sono sempre nella forma (x,x,x)
                maze_row.append(pixel[0] // 16)
        maze.append(maze_row)
    return maze, start, end, image

def json_to_maze(data):
    """
    Questa funzione trasforma il Json in ingresso in una matrice 
    costituita da:
        
        - 0 se la casella è percorribile.
        
        - -1 se la casella non è percorribile, quindi rappresenta il muro del 
          labirinto
          
        - un numero da 1 a 15 se la casella è una tonalità di grigio, rappresentando in questo
          modo il peso di una casella
          
    Parameters
    ----------
    data : dict
        Dizionario contenente le informazioni per convertire il json in una 
        matrice rappresentante il labirinto
    
    Returns
    -------
    maze : list
        E' una matrice che rappresenta l'immagine di partenza.
    start : list
        E' una lista delle coordinate di tutte le caselle verdi (punti di partenza)
    end : tuple
        E' una lista con le coordinate di tutte le caselle rosse (punti di arrivo)
    image: TiffImageFile
        E' l'immagine Tiff del labirinto descritto dal Json
    """

    # Crea una matrice vuota per il labirinto
    maze = []
    start = []
    end = ()
    for i in range(data["altezza"]):
        maze_row = []
        for j in range(data["larghezza"]):
            maze_row.append(0)
        maze.append(maze_row)

    # Popola la matrice con le pareti
    for wall in data["pareti"]:
        if wall["orientamento"] == "H":
            for i in range(wall["lunghezza"]):
                maze[wall["posizione"][0]][wall["posizione"][1] + i] = -1
        elif wall["orientamento"] == "V":
            for i in range(wall["lunghezza"]):
                maze[wall["posizione"][0] + i][wall["posizione"][1]] = -1
                
    # Popola con le posizioni iniziali      
    for iniziale in data["iniziali"]:
        i = iniziale[0]
        j = iniziale[1]
        start.append((i, j))
    
    # Popola con la posizione di arrivo
    i = data["finale"][0][0]
    j = data["finale"][0][1]
    end = (i,j)
    
    # Popolo con le caselle in scala di grigi
    for costo in data["costi"]:
        i = costo[0]
        j = costo[1]
        peso = costo[2]
        maze[i][j] = peso
    
    # Si richiama la funzione maze_to_image in modo da avere l'immagine del labirinto appena generato
    image = maze_to_image(maze,start,end)
    
    return maze, start, end, image


def draw_path(image, path,index,ext=".tiff"):
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
    
    ext : str
        Stringa che contiene l'estensione in cui salvare l'uscita, di default 
        è impostata su ".tiff" 
        
    Returns
    -------
    None.
    """
    # Serve creare una nuova immagine uguale a image e non solo un riferimento a questa
    new_image = copy.deepcopy(image)
    colors = [(0,255,255),(255,0,255),(0,128,0),(128,0,128),(255,255,0),(192,192,192)]
    name = filepath.split('.')[0] + '_start_' + str(index)
    # Apre l'immagine del labirinto e disegna il percorso
    pixels = new_image.load()
    # Disegna il percorso sul labirinto
    for x, y in path[1:(len(path)-1)]:
        pixels[y, x] = colors[index]  # Il colore del percorso in tal modo varia a seconda della posizione di partenza
        # Salva il labirinto risolto
    new_image.save(f'./Percorsi/{name}_path_{i+1}_dijkstra{ext}',format='PNG')
   

def load_maze(filepath,file_extension):
    '''
    Questa funzione prende in ingresso il path del file in input e richiama
    la funzione corretta per la conversione in matrice facendo un check sulla
    estensione del file.

    Parameters
    ----------
    filepath : str
        Path del file di input
        
    file_extension : str
        Stringa che contiene l'estensione in cui salvare l'uscita, di default 
        è impostata su ".tiff" 
    

    Returns
    -------
    None

    '''
    # Se è un file immagine diverso da .tiff richiama la funzione image_to_maze
    # solo dopo aver convertito l'immagine in RGB
    if file_extension == ".png":
        img = Image.open(filepath)
        img = img.convert("RGB")
        return image_to_maze(img)
    if file_extension in [".tiff",".jpg",".jpeg"]:
        # Apre l'immagine del labirinto
        image = Image.open(filepath)
        return image_to_maze(image)
    # Se è un file .json richiama la funzione json_to_maze
    elif file_extension == ".json":
        # Legge il file JSON
        with open(filepath) as json_file:
            data = json.load(json_file)
        return json_to_maze(data)
    # In qualsiasi altro caso, genera un errore in quanto il formato non è supportato
    else:
        raise ValueError("Formato file non supportato")


def maze_to_image(maze,start,end):
    '''
    Questa funzione prende in ingresso la matrice rappresentante il labirinto
    generata da json_to_maze e genera un'immagine Tiff ad essa associata.

    Parameters
    ----------
    maze : list
        E' una matrice che rappresenta l'immagine di partenza.
    start : list
        Lista delle posizioni di partenza del labirinto
    end : tuple
        Posizione di arrivo del labirinto

    Returns
    -------
    image: TiffImageFile
        E' l'immagine Tiff del labirinto descritto da Maze

    '''
    # Crea un'immagine vuota con le dimensioni della matrice del labirinto
    image = Image.new("RGB", (len(maze[0]), len(maze)))
    pixels = image.load()
    # Imposta i pixel dell'immagine in base alla matrice del labirinto
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == -1:
                pixels[j, i] = (0, 0, 0) # Muro = nero
            elif maze[i][j] == 0:
                pixels[j, i] = (255, 255, 255) # Cammino = bianco
            else:
                pixels[j, i] = (maze[i][j]*16, maze[i][j]*16, maze[i][j]*16) # Altri valori = grigio scuro
    i = end[0]
    j = end[1]
    pixels[j,i] = (255, 0, 0)
    for st in start:
        i = st[0]
        j = st[1]
        pixels[j,i] = (0, 255, 0)
    return image

def draw_path_frames(image, path,index):
    frames = []
    colors = [(0,255,255),(255,0,255),(0,128,0),(128,0,128),(255,255,0),(192,192,192)]
    new_image = copy.deepcopy(image)
    pixels = new_image.load()
    # Serve creare una nuova immagine uguale a image e non solo un riferimento a questa
    # Disegna il percorso sul labirinto
    for x, y in path[1:(len(path)-1)]:
        new_image = copy.deepcopy(new_image)
        pixels = new_image.load()
        pixels[y, x] = colors[i] # Assegniamo un colore
    # Aggiungi l'immagine alla lista dei fotogrammi
        frames.append(new_image)
    # Crea la gif con tutte le immagini
    imageio.mimsave(f'./Percorsi/paths_{index+1}.gif', frames, fps=20)


# Esempio di utilizzo
filepath = input("Inserisci il percorso del file (.json/.tiff/.png):")
# Estrae l'estensione dalla stringa filepath
_,ext = os.path.splitext(filepath)
maze, start, end, image = load_maze(filepath,ext)
paths = []
peso = []
for i in range(len(start)):
    path, weight = find_shortest_path_by_weight(maze, start[i], end)
    paths.append(path)
    peso.append(weight)
    
json_data = []

# Genera e riempie un dizionario path_info che conterrà le informazioni salvate nel json in uscita
for path,i in zip(paths,range(len(start))):
    path_info = {
    "start": start[i],
    "end": end
   }
    if path is not None:
        if ext == ".json":
            draw_path(image, path,i) 
        else:
            draw_path(image, path,i,ext) 
        path_info["length"] = len(path)
        path_info["weight"] = peso[i]
        draw_path_frames(image,path,i)
    else:
        no_path = "Nessun percorso possibile dalla posizione di partenza selezionata"
        path_info["length"] =  no_path
    json_data.append(path_info)
    
# salva le informazioni del percorso in un file JSON
with open(f'./Percorsi/{filepath}_path_info.json', "w") as f:
    json.dump(json_data, f)


  


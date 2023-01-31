from PIL import Image

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
        È una matrice che rappresenta l'immagine di partenza.
    start : list
        È una lista delle coordinate di tutte le caselle verdi (punti di partenza)
    end : tuple
        È una lista con le coordinate di tutte le caselle rosse (punti di arrivo)
    image: TiffImageFile
        È l'immagine Tiff del labirinto descritto dal Json
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
    end = (i, j)

    # Popolo con le caselle in scala di grigi
    for costo in data["costi"]:
        i = costo[0]
        j = costo[1]
        peso = costo[2]
        maze[i][j] = peso

    # Si richiama la funzione maze_to_image in modo da avere l'immagine del labirinto appena generato
    image = maze_to_image(maze, start, end)

    return maze, start, end, image

def maze_to_image(maze, start, end):
    '''
    Questa funzione prende in ingresso la matrice rappresentante il labirinto
    generata da json_to_maze e genera un'immagine ad essa associata.

    Parameters
    ----------
    maze : list
        È una matrice che rappresenta l'immagine di partenza.
    start : list
        Lista delle posizioni di partenza del labirinto
    end : tuple
        Posizione di arrivo del labirinto

    Returns
    -------
    image: TiffImageFile
        È l'immagine Tiff del labirinto descritto dalla variabile Maze

    '''
    # Crea un'immagine vuota con le dimensioni della matrice del labirinto
    image = Image.new("RGB", (len(maze[0]), len(maze)))
    pixels = image.load()
    # Imposta i pixel dell'immagine in base alla matrice del labirinto
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == -1:
                pixels[j, i] = (0, 0, 0)  # Muro = nero
            elif maze[i][j] == 0:
                pixels[j, i] = (255, 255, 255)  # Cammino = bianco
            else:
                pixels[j, i] = (maze[i][j] * 16, maze[i][j] * 16, maze[i][j] * 16)  # Altri valori = grigio
    i = end[0]
    j = end[1]
    pixels[j, i] = (255, 0, 0)
    for st in start:
        i = st[0]
        j = st[1]
        pixels[j, i] = (0, 255, 0)

    return image
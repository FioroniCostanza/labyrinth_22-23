from PIL import Image

def image_to_maze(filepath):
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
        È una matrice che rappresenta l'immagine di partenza.
    start : list
        È una lista delle coordinate di tutte le caselle verdi (punti di partenza)
    end : tuple
        È una lista con le coordinate di tutte le caselle rosse (punti di arrivo)
    image: TiffImageFile
        È l'immagine ottenuta da filepath.
    """
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
            # convertiamo il pixel in un numero, -1 se è un muro, 0 altrimenti
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
                # in tal caso utilizziamo il valore del pixel come peso
                maze_row.append(pixel[0] // 16)
        maze.append(maze_row)
    return maze, start, end, image

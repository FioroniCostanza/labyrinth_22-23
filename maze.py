import os
import json
from PIL import Image


class Maze:
    def __init__(self, filepath):
        """
        Costruttore della classe Maze
        Parameters
        ----------
        filepath : str
            Path del file di input

        Returns
        -------
        None.
        """
        # Inizializziamo i tre attributi della classe
        # maze conterrà la matrice che rappresenta il labirinto
        self.maze = []
        # start è la lista di tutte le caselle di partenza
        self.start = []
        # end è la tupla rappresentante la casella di arrivo
        self.end = ()
        # # image contiene invece l'immagine rappresentante il labirinto
        self.image = None

        # Si richiama il metodo load_maze
        self.load_maze(filepath)

    def load_maze(self, filepath):
        '''
        Questa funzione ha il compito di richiamare la funzione corretta per la
        conversione in matrice facendo un check sull'estensione del file.

        '''
        # Scomposizione del filepath in nome ed estensione
        _, file_ext = os.path.splitext(os.path.basename(filepath))
        # Se è un file immagine richiama il metodo image_to_maze
        if file_ext in [".tiff", ".jpg", ".jpeg", ".png"]:
            # Apre l'immagine del labirinto
            self.image = Image.open(filepath)
            self.image_to_maze()

        # Se è un file .json richiama la funzione json_to_maze
        elif file_ext == ".json":
            # Legge il file JSON
            with open(filepath) as json_file:
                data = json.load(json_file)
            self.json_to_maze(data)
        # In qualsiasi altro caso, genera un errore in quanto il formato non è supportato
        else:
            raise ValueError("Formato file non supportato")

    def image_to_maze(self):
        """
        Questa funzione trasforma l'immagine in ingresso in una matrice
        costituita da:

            - 0 se il colore RGB dei pixel è nero, quindi rappresenta il muro del
              labirinto

            - 1 se il colore RGB dei pixel è bianco, verde o rosso.

            - un numero da 2 a 16 se il colore RGB è una tonalità di grigio, rappresentando in questo
              modo il peso di una casella
        """
        # Converte l'immagine in una matrice di pixel
        pixels = self.image.load()
        # Scansiona i pixel dell'immagine per creare la matrice del labirinto
        for i in range(self.image.height):
            maze_row = []
            for j in range(self.image.width):
                pixel = pixels[j, i]
                # Si converte il pixel in un numero, -1 se è un muro, 0 altrimenti
                if pixel == (255, 255, 255):
                    maze_row.append(1)
                elif pixel == (0, 0, 0):  # Pixel nero
                    maze_row.append(0)
                elif pixel == (0, 255, 0):  # Pixel verde
                    maze_row.append(1)
                    self.start.append((i, j))
                elif pixel == (255, 0, 0):  # Pixel rosso
                    maze_row.append(1)
                    self.end = (i, j)
                elif pixel[0] == pixel[1] == pixel[2]:
                    # in tal caso utilizziamo il valore del pixel come peso
                    # infatti i pixel grigi sono sempre nella forma (x,x,x)
                    # sommando uno cosi nel caso del pixel (16,16,16) si ottiene un peso pari a 2
                    maze_row.append((pixel[0] // 16) + 1)
            self.maze.append(maze_row)

    def json_to_maze(self, data):
        """
        Questa funzione trasforma il Json in ingresso in una matrice
        costituita da:

            - 0 se la casella non è percorribile, quindi rappresenta il muro del
              labirinto

            - 1 se la casella è percorribile

            - un numero da 2 a 16 se la casella è una tonalità di grigio, rappresentando in questo
              modo il peso di una casella

        Parameters
        ----------
        data : dict
            Dizionario contenente le informazioni per convertire il json in una
            matrice rappresentante il labirinto

        Returns
        -------
        """
        for i in range(data["altezza"]):
            maze_row = []
            for j in range(data["larghezza"]):
                maze_row.append(1)
            self.maze.append(maze_row)

        # Popola la matrice con le pareti
        for wall in data["pareti"]:
            if wall["orientamento"] == "H":
                for i in range(wall["lunghezza"]):
                    self.maze[wall["posizione"][0]][wall["posizione"][1] + i] = 0
            elif wall["orientamento"] == "V":
                for i in range(wall["lunghezza"]):
                    self.maze[wall["posizione"][0] + i][wall["posizione"][1]] = 0

        # Popola con le posizioni iniziali
        for iniziale in data["iniziali"]:
            i = iniziale[0]
            j = iniziale[1]
            self.start.append((i, j))

        # Popola con la posizione di arrivo
        i = data["finale"][0][0]
        j = data["finale"][0][1]
        self.end = (i, j)

        # Popolo con le caselle in scala di grigi
        for costo in data["costi"]:
            i = costo[0]
            j = costo[1]
            peso = costo[2] + 1
            self.maze[i][j] = peso + 1

        # Si richiama la funzione maze_to_image in modo da avere l'immagine del labirinto appena generato
        self.maze_to_image()

    def maze_to_image(self):
        '''
        Questo metodo, partendo dalla matrice rappresentante il labirinto
        generata da json_to_maze, genera un'immagine Tiff ad essa associata.

        Returns
        -------
        image: TiffImageFile
            È l'immagine Tiff del labirinto descritto da Maze
        '''
        # Crea un'immagine vuota con le dimensioni della matrice del labirinto
        self.image = Image.new("RGB", (len(self.maze[0]), len(self.maze)))
        pixels = self.image.load()
        # Imposta i pixel dell'immagine in base alla matrice del labirinto
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 0:
                    pixels[j, i] = (0, 0, 0)  # Muro = nero
                elif self.maze[i][j] == 1:
                    pixels[j, i] = (255, 255, 255)  # Cammino = bianco
                else:
                    pixels[j, i] = ((self.maze[i][j] - 1) * 16, (self.maze[i][j] - 1) * 16, (self.maze[i][j] - 1) * 16)  # Altri valori = grigio scuro
        i = self.end[0]
        j = self.end[1]
        pixels[j, i] = (255, 0, 0)
        for st in self.start:
            i = st[0]
            j = st[1]
            pixels[j, i] = (0, 255, 0)

    def get_adjacent_positions(self,pos):
        """
        Questa funzione verifica quali tra le 4 posizioni adiacenti alla posizione corrente
        siano uno spazio percorribile e non un muro.
        Parameters
        ----------
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
            if i>=0 and j>=0 and i<len(self.maze) and j<len(self.maze[0]) and self.maze[i][j]!=0:
                valid_positions.append(((i,j),self.maze[i][j]))
        return valid_positions
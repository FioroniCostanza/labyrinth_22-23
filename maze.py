import json
import os
import copy
from maze_from_image import *
from maze_from_json import *

class Maze:

    def __init__(self,filepath):
        self.name, self.extension = os.path.splitext(filepath)
        self.labyrinth = None
        self.start = []
        self.end = None
        self.image = None

    def load_maze(self,filepath):
        '''
        Questa funzione prende in ingresso il path del file in input e richiama
        la funzione corretta per la conversione in matrice facendo un check sulla
        estensione del file.

        Parameters
        ----------
        filepath : str
            Path del file di input

        file_extension : str
            Stringa che contiene l'estensione in cui salvare l'uscita

        Returns
        -------
        None

        '''
        # Se in ingresso ho un immagine richiama la funzione image_to_maze
        if self.extension in [".jpeg", ".png", ".tiff"]:
            self.labyrinth, self.start, self.end, self.image = image_to_maze(filepath)
        # Se in ingresso ho un file json richiama la funzione json_to_maze
        elif self.extension == ".json":
            with open(filepath) as json_file:
                data = json.load(json_file)
            self.labyrinth, self.start, self.end, self.image = json_to_maze(data)
        # In qualsiasi altro caso, genera un errore in quanto il formato non è supportato
        else:
            raise ValueError("Formato file non supportato")

    def draw_path(self, path, index, ext=".tiff"):
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
            Un intero che identifica la casella di partenza a cui fa riferimento il percorso.

        ext : str
            Stringa che contiene l'estensione in cui salvare l'uscita, di default
            è impostata su ".tiff" in modo da gestire anche il caso in cui in ingresso si abbia un file json
        Returns
        -------
        None.
        """

        # Si crea una copia di image in modo da avere un'immagine da modificare e non un riferimento

        new_image = copy.deepcopy(self.image)
        colors = [(0, 255, 255), (255, 0, 255), (0, 128, 0), (128, 0, 128), (255, 255, 0), (192, 192, 192)]
        # Apre l'immagine del labirinto e disegna il percorso
        pixels = new_image.load()
        for x, y in path[1:(len(path) - 1)]:
            pixels[y, x] = colors[index]  # Il colore del percorso in tal modo varia a seconda della posizione di partenza
            # Salva il labirinto risolto
        new_image.save(f'./Percorsi/{self.name}_path_{index + 1}{ext}', format='PNG')
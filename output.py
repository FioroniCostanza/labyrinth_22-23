import copy
import json
import os


def output_generation(filepath, paths, peso, maze):
    """
    Questa funzione genera gli output da dare in uscita in seguito all'elaborazione.
    Restituisce un file json con informazioni su ogni percorso e delle immagini
    del labirinto di partenza con il percorso colorato.
    Parameters
    ----------

    filepath : str
        Path del file di input

    paths : list of lists
        Contiene tutti i percorsi trovati

    peso : list
        Contiene il peso di ogni percorso

    maze : Class
        Contiene i contenuti della classe Maze
    Returns
    -------
    None.
    """
    # Si scompone filepath in nome del file ed estensione
    filename, file_ext = os.path.splitext(os.path.basename(filepath))

    json_data = []
    # Genera e riempie un dizionario path_info che conterrà le informazioni salvate nel json in uscita
    for path, i in zip(paths, range(len(maze.start))):
        path_info = {
            "start": maze.start[i],
            "end": maze.end,
        }
        if path is not None:
            draw_path(filename, file_ext, maze, path, i)
            path_info["length"] = len(path)
            path_info["weight"] = peso[i]
        else:
            no_path = "Nessun percorso possibile dalla posizione di partenza selezionata"
            path_info["length"] = no_path
        json_data.append(path_info)

    # salva le informazioni del percorso in un file JSON
    with open(f'./Percorsi/{filename}_paths_info.json', "w") as f:
        json.dump(json_data, f, indent=4)


def draw_path(filename, file_ext, maze, path, index):
    """
    Questa funzione colora sull' immagine del labirinto di partenza i percorsi possibili, colorandoli
    in maniera differente per ogni punto di partenza e salvandoli in immagini
    diverse per ogni percorso.

    Parameters
    ----------
    filename : str
        Stringa contenente il nome del file di input

    file_ext : str
        Stringa contenente l'estensione del file di input

    maze : Class
        Contiene i contenuti della classe Maze

    paths : list
        Lista di tutte i percorsi che partono da una stessa casella di partenza.

    index : list
        Un intero che identifica la casella di partenza a cui fa riferimento il percorso.
    Returns
    -------
    None.
    """

    # Si crea una copia di image in modo da avere un'immagine da modificare e non un riferimento
    new_image = copy.deepcopy(maze.image)
    colors = [(0, 255, 255), (255, 0, 255), (0, 128, 0), (128, 0, 128), (255, 255, 0), (192, 192, 192)]
    # Apre l'immagine del labirinto e disegna il percorso
    pixels = new_image.load()
    for x, y in path[1:(len(path) - 1)]:
        pixels[y, x] = colors[index]  # Il colore del percorso in tal modo varia a seconda della posizione di partenza
        # Salva il labirinto risolto
    if file_ext != '.json':
        ext = file_ext
    else:
        ext = '.tiff'  # si imposta di default il formato ".tiff" per l'immagine generata nel caso in cui in ingresso si abbia un file json

    if not os.path.exists('./Percorsi'):
        os.makedirs('./Percorsi')
    new_image.save(f'./Percorsi/{filename}_path_{index + 1}{ext}', format='PNG')

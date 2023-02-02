import copy
import json
import os
import imageio


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
    
    Inoltre, genera, per ogni percorso, una Gif che mostra frame per frame il percorrimento 
    dell'intero percorso.

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

    # Si creano due copie di image in modo da avere un'immagine su cui colorare il percorso completo
    # e una su cui colorare frame per frame, si usa la libreria deepcopy poichè senza genereremmo solo 
    # un riferimento a image non una nuova immagine
    full_path_image = copy.deepcopy(maze.image)
    frame = copy.deepcopy(maze.image)
    # Inizializzo una lista frames in cui si salveranno mano a mano le immagini parziali
    frames = []
    colors = [(0, 255, 255), (255, 0, 255), (0, 128, 0), (128, 0, 128), (255, 255, 0), (192, 192, 192)]
    # Apre l'immagine del labirinto e disegna il percorso
    pixels = full_path_image.load()
    pixels_f = frame.load()
    for x, y in path[1:(len(path) - 1)]:
        # Ad ogni iterazione è come se resettassimo l'immagine frame alla situazione di partenza
        frame = copy.deepcopy(maze.image)
        pixels_f = frame.load()
        pixels[y, x] = colors[index]  # Il colore del percorso in tal modo varia a seconda della posizione di partenza
        pixels_f[y, x] = colors[index] 
        # All'aggiunta di ogni casella del percorso colorata salviamo quest'immagine parziale nella lista frames
        frames.append(frame)

        # Salva il labirinto risolto
    if file_ext != '.json':
        ext = file_ext
    else:
        ext = '.tiff'  # si imposta di default il formato ".tiff" per l'immagine generata nel caso in cui in ingresso si abbia un file json

    if not os.path.exists('./Percorsi'):
        os.makedirs('./Percorsi')
    full_path_image.save(f'./Percorsi/{filename}_path_{index + 1}{ext}', format='PNG')
    imageio.mimsave(f'./Percorsi/paths_{index+1}.gif', frames, fps=15)

import json
from dijkstra_algorithm import *

def final_operations(maze):
    """
    Questa funzione genera un dizionario contentente le informazioni del percorso 
    a peso minimo più breve, trovato per ogni punto di partenza. Inoltre, salva tutte 
    le informazioni in un file JSON all'interno della cartella Percorsi.
    
    Parameters
    ----------
    maze : list
        E' una matrice che rappresenta l'immagine di partenza.

    Returns
    -------
    None.

    """
    paths = []
    peso = []
    for i in range(len(maze.start)):
        path, weight = find_shortest_path_by_weight(maze.labyrinth, maze.start[i], maze.end)
        paths.append(path)
        peso.append(weight)

    json_data = []

    # Genera e riempie un dizionario path_info che conterrà le informazioni salvate nel json in uscita
    for path, i in zip(paths, range(len(maze.start))):
        path_info = {
            "start": maze.start[i],
            "end": maze.end,
        }
        if path is not None:
            maze.draw_path(maze.image, path, i)
            path_info["length"] = len(path)
            path_info["weight"] = peso[i]
        else:
            no_path = "Nessun percorso possibile dalla posizione di partenza selezionata"
            path_info["length"] = no_path
        json_data.append(path_info)

    # salva le informazioni del percorso in un file JSON
    with open(f'./Percorsi/{maze.name}_path_info.json', "w") as f:
        json.dump(json_data, f)

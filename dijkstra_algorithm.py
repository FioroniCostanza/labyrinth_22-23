import heapq

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
    weight_tot = 0

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
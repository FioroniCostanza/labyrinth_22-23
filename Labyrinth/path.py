import heapq


class Path:
    def __init__(self, maze):
        
        """
        Costruttore della classe Path
        Parameters
        ----------
        maze : Class
            Contiene i metodi e gli attributi della classe Maze

        Returns
        -------
        None.
        """
        
        self.paths = []
        self.weight = []
        # Per ogni casella di partenza, calcola il percorso a peso minimo
        for i in range(len(maze.start)):
            path, weight = self.find_shortest_path_by_weight(maze.start[i],maze)
            self.paths.append(path)
            self.weight.append(weight)

    def find_shortest_path_by_weight(self, start, maze):
   
        """
        Questo metodo svolge una ricerca del percorso a peso minimo all'interno del
        labirinto, utilizzando l'algoritmo di Dijkstra.
        Dando in ingresso il punto di partenza e un'istanza della classe Maze,
        la funzione restituirà una lista con tutte le tuple corrispondenti alle posizioni
        che intercorrono tra il punto di partenza e il punto di arrivo.
        
        Parameters
        ----------

        start: tuple
            Contiene la posizione di partenza

        maze : Class
            Contiene i metodi e gli attributi della classe Maze

        Returns
        -------
        path : list
           Restituisce il percorso a peso minimo trovato tra la partenza in ingresso e l'arrivo.
           
        weight_tot : int
            Restituisce il peso totale del percorso trovato
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
            if curr_pos == maze.end:
                # Assegniamo il peso totale e restituiamo il percorso ottenuto
                weight_tot = curr_weight
                return path, weight_tot
            # Altrimenti, per ogni posizione adiacente al nodo corrente si verifica se esse siano state già visitate
            for next_pos, weight in maze.get_adjacent_positions(curr_pos):
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

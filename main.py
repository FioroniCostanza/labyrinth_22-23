from maze import Maze
from path import Path
from output import output_generation

filepath = input("Inserisci il percorso del file (.json/.tiff/.png/.jpeg): ")

m = Maze(filepath)
paths = []
weights = []
for st in m.start:
    p = Path(m.maze, st, m.end)
    paths.append(p.path)
    weights.append(p.weight)

# Una volta calcolati i percorsi, si richiama la funzione output_generation per ottenere i file di output
output_generation(paths,weights,m)
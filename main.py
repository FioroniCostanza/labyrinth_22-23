from maze import Maze
from path import Path
from output import output_generation

# Richiede in input il file da elaborare
filepath = input("Inserisci il percorso del file (.json/.tiff/.png/.jpeg):")
# Richiama la classe Maze
m = Maze(filepath)

paths = []
peso = []

# Per ogni casella di partenza, richiama la classe Path per calcolare
# il percorso a peso minimo
for s in m.start:
    p = Path(m.maze,s,m.end)
    paths.append(p.path)
    peso.append(p.weight)
    
# Una volta calcolati i percorsi, si richiama la funzione output_generation 
# per ottenere i file di output
output_generation(paths,peso,m.start,m.end,m.filename,m.img)
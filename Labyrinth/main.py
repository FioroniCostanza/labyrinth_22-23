from maze import Maze
from path import Path
from output import output_generation

if __name__ == '__main__':
  # Richiede in input il file da elaborare
  filepath = input("Inserisci il percorso del file (.json/.tiff/.png/.jpeg): ").strip()

  # Richiama le classi Maze e Path per calcolare i percorsi
  m = Maze(filepath)
  p = Path(m)

  # Una volta calcolati i percorsi, si richiama la funzione output_generation per ottenere i file di output
  output_generation(filepath,p.paths,p.weight,m)

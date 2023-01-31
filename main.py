from maze import Maze
from final_operations import *

filepath = input("Inserisci il percorso del file (.json/.tiff/.png/.jpeg): ")
maze = Maze(filepath)
maze.load_maze(filepath)
final_operations(maze)
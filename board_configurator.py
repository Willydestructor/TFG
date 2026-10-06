#Coge el tablero en crudo y le asigna números y recursos

import raw_board_creator as rbc

import pickle
import random
import time
import numpy as np
import os
import networkx as nx

#Definimos la cantidad de recursos que habrá en el tablero (Posibilidad futura de hacer que el usuario pueda elegir la cantidad de recursos)
N_FOREST = 4
N_SHEEP = 4
N_WHEAT = 4
N_CLAY = 3
N_ORE = 3 
N_DESERT = 1

NUMBER_ORDER = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]

#Se empieza en la 27
PORT_TILES = [["S", "S", "-", "3", "3"], ["-", "O", "O", "-", "-"], ["W", "W", "-", "3", "3"], ["-", "F", "F", "-", "-"], ["C", "C", "-", "3", "3"], ["-", "3", "3", "-", "-"]]


#Recuperamos el tablero en crudo del archivo raw_board.pkl
board_path = 'raw_board.pkl'

def import_raw_board(board_path):
    if not os.path.exists(board_path):
        rbc.export_board()
    with open(board_path, "rb") as f:
        raw_board = pickle.load(f)
    return raw_board

raw_board = import_raw_board(board_path)
Node_Board = raw_board["Node_Board"]
Tile_Board = raw_board["Tile_Board"]
Position = raw_board["Position"]



def randomize_resources ():
    resources = ["F"] * N_FOREST + ["S"] * N_SHEEP + ["W"] * N_WHEAT + ["C"] * N_CLAY + ["O"] * N_ORE + ["D"] * N_DESERT
    Tiles = []
    for i in range(len(Tile_Board)):
        random_resource = random.choice(resources)
        resources.remove(random_resource)
        Tiles.append(random_resource)
    return Tiles

def determine_tile_order():
    tile_order = []
    outer_ring = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    middle_ring = [12, 13, 14, 15, 16, 17]
    inner_ring = [18]
    #Elijo una loseta aleatoria del anillo exterior
    index = random.choice(outer_ring)
    for _ in range(len(outer_ring)):
        index = index % len(outer_ring)
        tile_order.append(outer_ring[index])
        index += 1
    
    index = int ((index - (index % 2)) / 2)
    for _ in range(len(middle_ring)):
        index = index % len(middle_ring)
        tile_order.append(middle_ring[index])
        index += 1
        
    tile_order.append(inner_ring[0])
    return tile_order



#Primero creo unas listas con el orden de uso de losetas y finalmente asigno los recursos y números según el orden asignado
def assign_numbers_to_tiles():
    tile_order = determine_tile_order()
    resources = randomize_resources()
    final_tiles = [None] * len(Tile_Board)
    
    #print("tile_order:", tile_order)
    #print("resources:", resources)
    
    number_order_extended = NUMBER_ORDER.copy()
    pos_desert = resources.index("D")
    number_order_extended.insert(pos_desert, 0) 
    #print("number_order_extended: ", number_order_extended)    
    
    number_resource = []
    for i in range(len(number_order_extended)):
        number_resource.append([resources[i], number_order_extended[i]])
        
    #print("Asignación:", number_resource)
    
    for j in range(len(number_resource)):
        final_tiles[j] = number_resource[tile_order[j]]
        
    return final_tiles

def assign_ports():
    ports_randomized = random.sample(PORT_TILES, len(PORT_TILES))
    i = 27
    for port in ports_randomized:
        for v in port:
            Node_Board.add_node(i, port=v)
            i = (i + 1) % 30
    return Node_Board

def print_board(Tiles):
    print_order = [0, 11, 10, 1, 12, 17, 9, 2, 13, 18, 16, 8, 3, 14, 15, 7, 4, 5, 6]
    tiles_per_row = [3, 4, 5, 4, 3]
    index = 0
    for row in tiles_per_row:
        for _ in range(5 - row):
            print("\t", end="")
        for _ in range(row):
            print(f"{Tiles[print_order[index]]} \t", end="")
            index += 1
        print("\n")


tiles = assign_numbers_to_tiles()

print_board(tiles)
assign_ports()
print(Node_Board.nodes.data())

#print("Recursos: ", tiles)






#Creación del tablero y archivo raw_board.pkl con los datos del tablero en crudo
#OUTPUT: raw_board.pkl
#       Node_Board: Grafo de nodos
#       Tile_Board: Lista de losetas con sus nodos correspondientes
def export_board():
    inicio = time.time()
    Node_Board = assign_ports()
    Tile_board = assign_numbers_to_tiles()
    export_data = {
        "Node_Board": Node_Board, 
        "Tile_Board": Tile_board,
        "Position": Position
    }
    with open("empty_board.pkl", "wb") as f:
        pickle.dump(export_data, f)
    final = time.time()
    print("Tiempo de ejecución asignación de números: ", final - inicio, "segundos")
    
    
export_board()
# Función que crea un grafo y una lista.
# El grafo es el espacio jugable (donde se sitúan los pueblos y caminos)
# La lista es para relacionar las losetas con sus correspondientes nodos. Es una lista y no un grafo porque los recursos no tienen relación entre sí, 
# mejorando la lectura y velocidad al tener que hacer menos búsquedas entre grafos 

#Documentación networkx https://networkx.org/documentation/stable/tutorial.html

import time
import pickle
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt

Tile_board = []
Node_Board = nx.Graph()
Position = []

# Función para crear un tablero con la estructuar de nodos, donde los jugdores trabajarán
def create_nodes():
    graph = nx.path_graph(54)
    graph.remove_edges_from([(29, 30), (47, 48)])
    graph.add_edges_from([(0, 29), (30, 47), (48, 53)])
    graph.add_edges_from([
        (2, 30), (4, 32), (7, 33), (9, 35), (12, 36), (14, 38), (17, 39), (19, 41), (22, 42), (24, 44), (27, 45), (29, 47), 
        (31, 48), (34, 49), (37, 50), (40, 51), (43, 52), (46, 53)
    ])
    return graph

#Función que encuentra todos los ciclos de 6 vértices en el grafo y los "renombra" con su valor más pequeño de vértice
def find_6cycles(graph):
    inicioC = time.time()
    cycles = [cycle for cycle in nx.simple_cycles(graph) if len(cycle) == 6]
    cyclest = []
    for cycle in cycles:
        min = 60
        for vertex in cycle:
            if vertex < min:
                min = vertex
        cyclest.append((min, cycle))
    cyclest.sort(key=lambda x: x[0])
    finalC = time.time()
    print("Tiempo de ejecución de la función find_6cycles: ", finalC - inicioC, "segundos")
    return cyclest

#Función que renombra los ciclos para adaptarlos a la espiral de colocación de números
def rename_cycles_tuples(cycle_tuples):
    order = range(19)
    renamed_cycle = []
    renamed_tuples = []
    for i in range(len(order)):
        renamed_cycle = [order[i], cycle_tuples[i][1]]
        renamed_tuples.append(renamed_cycle)    
    return renamed_tuples

#Función que crea la lista de losetas final
def create_tiles(nGraph):
    cycles = find_6cycles(nGraph)
    return rename_cycles_tuples(cycles)

#Función que crea el tablero completo, con los nodos y las losetas
def create_board():
    Node_Board = create_nodes()
    Tile_board = create_tiles(Node_Board)
    return Node_Board, Tile_board


# Idea sacada de https://www.redblobgames.com/grids/hexagons/ para imprimir los hexágonos, usar los ángulos, de ahí, he buscado un patrón

def move_x_steps_counterclockwise(pos, steps, i_angle):
    if steps < 0:
        raise ValueError("steps must be non-negative")

    x, y = pos
    #initial_angle = np.pi + np.pi/6
    angle_variation = np.pi/6
    last_angle = i_angle
    edge_length = 1

    for _ in range(steps):
        angle = last_angle + angle_variation
        x += edge_length * np.cos(angle)
        y += edge_length * np.sin(angle)
        last_angle = angle

    return x, y


def board_position():
    graph = Node_Board if Node_Board.number_of_nodes() else create_nodes()
    initial_angle = np.pi
    angle_variation = np.pi/3
    last_angle = initial_angle
    last_pos = (0.0, 0.0)
    edge_length = 1
    position = {}
    pattern = [-1, 1, 1, -1, 1]
    start_circle = 0
    first_node_new_circle = 2
    new_circle_new_pos = (0.0, 0.0)
    for i_node, node in enumerate(graph.nodes):
        angle = last_angle + angle_variation * pattern[(i_node - start_circle) % len(pattern)]
        x = last_pos[0] + edge_length * np.cos(angle)
        y = last_pos[1] + edge_length * np.sin(angle)
        position[node] = (x, y)
        
        if (i_node == first_node_new_circle):
            new_circle_new_pos = position[node]
        
        if (i_node == 30):
            last_pos = move_x_steps_counterclockwise(new_circle_new_pos, 1, np.pi + np.pi/2)
            last_angle = np.pi
            pattern = [1, 1, -1]
            start_circle = 30
            position[node] = last_pos
            first_node_new_circle = 31
        elif(i_node == 48):
            last_pos = move_x_steps_counterclockwise(new_circle_new_pos, 1, np.pi + np.pi/2)
            last_angle = np.pi
            pattern = [1]
            start_circle = 48
            position[node] = last_pos
        else:
            last_pos = (x, y)
            last_angle = angle

    #print("position: ", position)
    return position
    
    
def print_board(position = board_position()):
    graph = Node_Board if Node_Board.number_of_nodes() else create_nodes()
    nx.draw(
        graph,
        position,
        with_labels=True,
        node_color="skyblue",
        node_size=500,
        font_weight="bold",
        edge_color="gray",
        width=1.5,
    )
    plt.show()

    
#print_board()

# Posición manual en 3 círculos concéntricos
# Círculo externo: 0..29
# Círculo interior: 48..53
"""
pos = {}
    for i_node, node in enumerate(graph.nodes):
        angle = last_angle + angle_variation * pattern[i_node % len(pattern)]
        x = last_pos[0] + edge_length * np.cos(angle)
        y = last_pos[1] + edge_length * np.sin(angle)
        position[node] = (x, y)
        last_pos = (x, y)
    angle = 2 * np.pi * (node - 30) / 18
    pos[node] = (np.cos(angle) * 3, np.sin(angle) * 3)

    return position
for node in range(48, 54):
    pos,
    with_labels=True,
    node_color="skyblue",
    font_weight="bold",
    edge_color="gray",
    width=1.5,
)

# Mostrar en pantalla
plt.show()
"""



#Creación del tablero y archivo raw_board.pkl con los datos del tablero en crudo
#OUTPUT: raw_board.pkl
#       Node_Board: Grafo de nodos
#       Tile_Board: Lista de losetas con sus nodos correspondientes
def export_board():
    incio = time.time()
    Node_Board, Tile_board = create_board()
    export_data = {
        "Node_Board": Node_Board, 
        "Tile_Board": Tile_board,
        "Position": board_position()
    }
    with open("raw_board.pkl", "wb") as f:
        pickle.dump(export_data, f)
    final = time.time()
    print("Tiempo de creación crudo: ", final - incio, "segundos")
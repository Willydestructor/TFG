import board_configurator as bc

import time
import pygame
import os
import pickle

inicio = time.time()
#Recuperamos el tablero en crudo del archivo raw_board.pkl
board_path = 'empty_board.pkl'

def import_empty_board(board_path):
    if not os.path.exists(board_path):
        bc.export_board()
    with open(board_path, "rb") as f:
        empty_board = pickle.load(f)
    return empty_board

empty_board = import_empty_board(board_path)
Node_Board = empty_board["Node_Board"]
Tile_Board = empty_board["Tile_Board"]
Position = empty_board["Position"]

print("Node_Board:", Node_Board)
print("Tile_Board:", Tile_Board)
print("Position:", Position)

final = time.time()
print("Tiempo de ejecución:", final - inicio, "segundos")


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1700, 956))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("light blue")
    pygame.draw.circle(screen, "red", player_pos, 40)
    
    for i in range(len(Position)):
        x = (Position[i][0]) * 85 + 750
        y = (Position[i][1]) * 85 + 750
        pygame.draw.circle(screen, "white", (x, y), 10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
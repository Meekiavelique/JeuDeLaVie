import pygame
import numpy as np

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 10
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
ZOOM_FACTOR = 1.1
MIN_CELL_SIZE = 5
MAX_CELL_SIZE = 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu de la vie")

def cadriage_vide():
    return np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)

def dessin(CADRIAGE):
    screen.fill(BLACK)
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y), max(int(CELL_SIZE / 20), 1))
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT), max(int(CELL_SIZE / 20), 1))
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if CADRIAGE[x][y] == 1:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def niveau_2_zoom(event):
    global CELL_SIZE, GRID_WIDTH, GRID_HEIGHT
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4 and CELL_SIZE < MAX_CELL_SIZE:
            CELL_SIZE = min(int(CELL_SIZE * ZOOM_FACTOR), MAX_CELL_SIZE)
            GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
            GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
        elif event.button == 5 and CELL_SIZE > MIN_CELL_SIZE:
            CELL_SIZE = max(int(CELL_SIZE / ZOOM_FACTOR), MIN_CELL_SIZE)
            GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
            GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

def handle_mouse(CADRIAGE):
    mouse_pos = pygame.mouse.get_pos()
    CELL_x = mouse_pos[0] // CELL_SIZE
    CELL_y = mouse_pos[1] // CELL_SIZE
    if pygame.mouse.get_pressed()[0]: 
        CADRIAGE[CELL_x][CELL_y] = 1
    elif pygame.mouse.get_pressed()[2]: 
        CADRIAGE[CELL_x][CELL_y] = 0

def update_CADRIAGE(CADRIAGE):
    new_CADRIAGE = CADRIAGE.copy()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            neighbors = cellules_voisines(CADRIAGE, x, y)
            if CADRIAGE[x][y] == 1 and (neighbors < 2 or neighbors > 3):
                new_CADRIAGE[x][y] = 0
            elif CADRIAGE[x][y] == 0 and neighbors == 3:
                new_CADRIAGE[x][y] = 1
    return new_CADRIAGE

def cellules_voisines(CADRIAGE, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_x = (x + i + GRID_WIDTH) % GRID_WIDTH
            neighbor_y = (y + j + GRID_HEIGHT) % GRID_HEIGHT
            count += CADRIAGE[neighbor_x][neighbor_y]
    count -= CADRIAGE[x][y]
    return count

def main():
    CADRIAGE = cadriage_vide()

    running = True
    simulation_running = False
    simulation_speed = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse(CADRIAGE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                elif event.key == pygame.K_EQUALS:
                    simulation_speed += 5
                elif event.key == pygame.K_MINUS:
                    simulation_speed = max(1, simulation_speed)
            if running:
                niveau_2_zoom(event)

        if simulation_running:
            CADRIAGE = update_CADRIAGE(CADRIAGE)

        dessin(CADRIAGE)
        pygame.display.flip()
        pygame.time.delay(1000 // simulation_speed)

    pygame.quit()

if __name__ == "__main__":
    main()

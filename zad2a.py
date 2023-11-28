import numpy as np
import pygame
from pygame.locals import *

# Inicjalizacja Pygame
pygame.init()

# Ustawienie wymiarów okna gry
width, height = 1024, 768 
screen = pygame.display.set_mode((width, height))

# Funkcja tworząca macierz translacji o wektor (dx, dy, dz)
def translation_matrix(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

# Funkcja tworząca macierz rotacji wokół osi Y
def rotation_matrix_y(angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [cos_a, 0, sin_a, 0],
        [0,     1, 0,     0],
        [-sin_a, 0, cos_a, 0],
        [0,     0, 0,     1]
    ])

# Funkcja tworząca macierz rotacji wokół osi X
def rotation_matrix_x(angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,     0,      0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a,  0],
        [0, 0,     0,      1]
    ])

# Funkcja tworząca macierz rotacji wokół osi Z
def rotation_matrix_z(angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a,  0, 0],
        [0,     0,      1, 0],
        [0,     0,      0, 1]
    ])

# Funkcja tworząca macierz projekcji perspektywicznej
def perspective_matrix(fov, aspect, near, far):
    f = 1 / np.tan(fov / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ])

# Funkcja aktualizująca macierz widoku kamery na podstawie obecnej orientacji i pozycji kamery
def update_view_matrix():
    pitch_matrix = rotation_matrix_x(camera_pitch)
    yaw_matrix = rotation_matrix_y(camera_angle)
    roll_matrix = rotation_matrix_z(camera_roll)
    return np.linalg.inv(roll_matrix @ pitch_matrix @ yaw_matrix @ translation_matrix(*camera_pos))

# Funkcja rysująca linię między dwoma punktami
def draw_line(screen, v1, v2, width, height, color=(255, 255, 255)):
    x1, y1, z1, w1 = v1 / v1[3]
    x2, y2, z2, w2 = v2 / v2[3]
    x1, y1 = int((x1 + 1) * 0.5 * width), int((1 - y1) * 0.5 * height)
    x2, y2 = int((x2 + 1) * 0.5 * width), int((1 - y2) * 0.5 * height)
    pygame.draw.line(screen, color, (x1, y1), (x2, y2))

# Funkcja rysująca sześcian (różne kolory)
def draw_cube(screen, cube_vertices, cube_edges, mvp_matrix, width, height, color):
    for edge in cube_edges:
        v1 = mvp_matrix @ cube_vertices[edge[0]]
        v2 = mvp_matrix @ cube_vertices[edge[1]]
        draw_line(screen, v1, v2, width, height, color)

# Definicja wierzchołków i krawędzi sześcianu
cube_vertices = np.array([[x, y, z, 1] for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]])
cube_edges = [(0, 1), (1, 3), (3, 2), (2, 0), (0, 4), (1, 5), (3, 7), (2, 6), (4, 5), (5, 7), (7, 6), (6, 4)]

# Funkcja do obliczania odległości obiektu od kamery
def calculate_distance(cube_center, camera_position):
    return np.linalg.norm(cube_center - camera_position)

# Struktura danych przechowująca pozycję i kolor każdego sześcianu
cubes_info = [
    {'position': (-5, 0, -5), 'color': (255, 0, 0)},    # Czerwony sześcian
    {'position': (5, 0, -5), 'color': (0, 255, 0)},     # Zielony sześcian
    {'position': (-5, 0, -10), 'color': (0, 0, 255)},   # Niebieski sześcian
    {'position': (5, 0, -10), 'color': (255, 255, 0)}   # Żółty sześcian
]

# Ustawienia początkowe kamery
camera_pos = np.array([0.0, 0.0, -20.0])    # Pozycja kamery
camera_angle = 0                            # Kąt obrotu wokół osi Y (yaw)
camera_pitch = 0                            # Kąt obrotu wokół osi X (pitch)
camera_roll = 0                             # Kąt obrotu wokół osi Z (roll)
camera_fov = np.pi / 4                      # Kąt widzenia kamery (field of view)
camera_speed = 0.5                          # Prędkość przemieszczania się kamery
rotation_speed = 0.05                       # Prędkość obrotu kamery

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Sterowanie kamerą
            if event.key == pygame.K_s:     # Ruch kamery do przodu
                camera_pos -= camera_speed * np.array([np.sin(camera_angle), 0, np.cos(camera_angle)])
            if event.key == pygame.K_w:     # Ruch kamery do tyłu
                camera_pos += camera_speed * np.array([np.sin(camera_angle), 0, np.cos(camera_angle)])
            if event.key == pygame.K_a:     # Ruch kamery w lewo
                camera_pos[0] += camera_speed
            if event.key == pygame.K_d:     # Ruch kamery w prawo
                camera_pos[0] -= camera_speed
            if event.key == pygame.K_q:     # Obrót kamery w lewo
                camera_roll += rotation_speed
            if event.key == pygame.K_e:     # Obrót kamery w prawo
                camera_roll -= rotation_speed
            if event.key == pygame.K_r:     # Zoom in (przybliżenie)
                camera_fov -= 0.01
            if event.key == pygame.K_t:     # Zoom out (oddalenie)
                camera_fov += 0.01
            if event.key == pygame.K_x:     # Ruch kamery w górę
                camera_pos[1] -= camera_speed
            if event.key == pygame.K_z:     # Ruch kamery w dół
                camera_pos[1] += camera_speed

    screen.fill((0, 0, 0))  # Czyszczenie ekranu

    # Ustawienie macierzy projekcji i widoku
    projection = perspective_matrix(camera_fov, width / height, 0.1, 1000)
    view_matrix = update_view_matrix()

    # Obliczanie odległości sześcianów od kamery i sortowanie
    cubes_with_distance = []
    for cube in cubes_info:
        cube_center = np.array(cube['position'] + (1,))
        distance = calculate_distance(cube_center[:3], camera_pos[:3])
        cubes_with_distance.append((distance, cube))

    cubes_with_distance.sort(key=lambda x: x[0], reverse=True)

    # Rysowanie sześcianów z przypisanymi kolorami
    for distance, cube in cubes_with_distance:
        x, y, z = cube['position']
        model_matrix = translation_matrix(x, y, z)
        mvp_matrix = projection @ view_matrix @ model_matrix
        draw_cube(screen, cube_vertices, cube_edges, mvp_matrix, width, height, cube['color'])

    pygame.display.flip()  # Aktualizacja zawartości okna

pygame.quit()  # Zakończenie pracy Pygame

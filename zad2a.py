import numpy as np
import pygame
from pygame.locals import *

# Inicjalizacja Pygame i utworzenie okna
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Funkcje do tworzenia macierzy transformacji
def translation_matrix(dx, dy, dz):
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [cos_a, 0, sin_a, 0],
        [0,     1, 0,     0],
        [-sin_a, 0, cos_a, 0],
        [0,     0, 0,     1]
    ])

def rotation_matrix_x(angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,     0,      0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a,  0],
        [0, 0,     0,      1]
    ])

def rotation_matrix_z(angle):
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a,  0, 0],
        [0,     0,      1, 0],
        [0,     0,      0, 1]
    ])

def perspective_matrix(fov, aspect, near, far):
    f = 1 / np.tan(fov / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ])

# Funkcja do obliczania odległości obiektu od kamery
def calculate_distance(cube_center, camera_position):
    return np.linalg.norm(cube_center - camera_position)

# Funkcja rysująca linię między dwoma punktami
def draw_line(screen, v1, v2, width, height, color=(255, 255, 255)):
    x1, y1, z1, w1 = v1 / v1[3]
    x2, y2, z2, w2 = v2 / v2[3]
    x1, y1 = int((x1 + 1) * 0.5 * width), int((1 - y1) * 0.5 * height)
    x2, y2 = int((x2 + 1) * 0.5 * width), int((1 - y2) * 0.5 * height)
    pygame.draw.line(screen, color, (x1, y1), (x2, y2))

# Funkcja rysująca sześcian
def draw_cube(screen, cube_vertices, cube_edges, mvp_matrix, width, height, color):
    for edge in cube_edges:
        v1 = mvp_matrix @ cube_vertices[edge[0]]
        v2 = mvp_matrix @ cube_vertices[edge[1]]
        draw_line(screen, v1, v2, width, height, color)

# Definicja wierzchołków i krawędzi sześcianu
cube_vertices = np.array([[x, y, z, 1] for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]])
cube_edges = [(0, 1), (1, 3), (3, 2), (2, 0), (0, 4), (1, 5), (3, 7), (2, 6), (4, 5), (5, 7), (7, 6), (6, 4)]

# Ustawienia początkowe kamery
camera_pos = np.array([0.0, 0.0, -20.0])
camera_angle = 0
camera_pitch = 0
camera_roll = 0
camera_fov = np.pi / 4
camera_speed = 0.5
rotation_speed = 0.05

# Aktualizacja macierzy widoku
def update_view_matrix():
    pitch_matrix = rotation_matrix_x(camera_pitch)
    yaw_matrix = rotation_matrix_y(camera_angle)
    roll_matrix = rotation_matrix_z(camera_roll)
    translation = translation_matrix(*camera_pos)
    return np.linalg.inv(translation @ yaw_matrix @ pitch_matrix @ roll_matrix)
    
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Sterowanie kamerą
            if event.key == pygame.K_s:  # Przód
                camera_pos -= camera_speed * np.array([np.sin(camera_angle), 0, np.cos(camera_angle)])
            if event.key == pygame.K_w:  # Tył
                camera_pos += camera_speed * np.array([np.sin(camera_angle), 0, np.cos(camera_angle)])
            if event.key == pygame.K_d:  # Obrót w lewo
                camera_angle += rotation_speed
            if event.key == pygame.K_a:  # Obrót w prawo
                camera_angle -= rotation_speed
            if event.key == pygame.K_q:
                camera_roll += rotation_speed
            if event.key == pygame.K_e:
                camera_roll -= rotation_speed
            if event.key == pygame.K_r:
                camera_fov -= 0.01
            if event.key == pygame.K_t:
                camera_fov += 0.01
            if event.key == pygame.K_x:
                camera_pitch += rotation_speed
            if event.key == pygame.K_z:
                camera_pitch -= rotation_speed

    screen.fill((0, 0, 0))  # Czyszczenie ekranu

    # Ustawienie macierzy projekcji i widoku
    projection = perspective_matrix(camera_fov, width / height, 0.1, 1000)
    view_matrix = update_view_matrix()

    # Lista do przechowywania sześcianów i ich odległości
    cubes_with_distance = []

    # Obliczanie odległości i sortowanie sześcianów
    for z in [-5, -10]:
        for x in [-5, 5]:
            cube_center = np.array([x, 0, z, 1])  # Środek sześcianu
            distance = calculate_distance(cube_center[:3], camera_pos[:3])
            cubes_with_distance.append((distance, x, z))

    # Sortowanie sześcianów według odległości (od najdalszych do najbliższych)
    cubes_with_distance.sort(key=lambda x: x[0], reverse=True)

    # Rysowanie sześcianów
    color_index = 0
    for distance, x, z in cubes_with_distance:
        model_matrix = translation_matrix(x, 0, z)
        mvp_matrix = projection @ view_matrix @ model_matrix
        draw_cube(screen, cube_vertices, cube_edges, mvp_matrix, width, height, colors[color_index % len(colors)])
        color_index += 1

    pygame.display.flip()  # Aktualizacja zawartości okna
    clock.tick(60)  # Utrzymanie stałej liczby klatek na sekundę

pygame.quit()  # Zakończenie pracy Pygame

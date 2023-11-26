from OpenGL.GL import *

# Lista sześcianów wraz z ich pozycjami.
cubes = []

for x in range(-5, 6, 4):
    for z in range(-5, 6, 4):
        cubes.append((x, 0, z))

# Definicja funkcji do rysowania sześcianu.
def draw_cube(x, y, z):
    # Definicja wierzchołków sześcianu.
    vertices = [
        [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1],  # Back face
        [1, -1, 1], [1, 1, 1], [-1, -1, 1], [-1, 1, 1],      # Front face
        [1, -1, -1], [1, 1, -1], [1, 1, 1], [1, -1, 1],      # Right face
        [-1, -1, 1], [-1, 1, 1], [-1, 1, -1], [-1, -1, -1],  # Left face
        [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1],      # Top face
        [-1, -1, 1], [1, -1, 1], [1, -1, -1], [-1, -1, -1]   # Bottom face
    ]

    # Definicja ścian sześcianu.
    faces = [
        [0, 1, 2, 3],  # Tylna ściana
        [4, 5, 6, 7],  # Frontalna ściana
        [8, 9, 10, 11],  # Prawa ściana
        [12, 13, 14, 15],  # Lewa ściana
        [16, 17, 18, 19],  # Górna ściana
        [20, 21, 22, 23]   # Dolna ściana
    ]

    # Kolor ścian - czerwony
    color_red = (1, 0, 0)

    # Kolor krawędzi - czarny (kolor tła)
    color_black = (0, 0, 0)

    # Krawędzie sześcianu.
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Tylna ściana
        (4, 5), (5, 7), (7, 6), (6, 4),  # Frontalna ściana
        (0, 4), (1, 5), (2, 7), (3, 6),  # Połączenia ścian bocznych
        (0, 4), (1, 5), (2, 7), (3, 6),  # Połączenia ścian górnych i dolnych
        (8, 9), (9, 10), (10, 11), (11, 8),  # Prawa ściana
        (12, 13), (13, 14), (14, 15), (15, 12),  # Lewa ściana
        (16, 17), (17, 18), (18, 19), (19, 16),  # Górna ściana
        (20, 21), (21, 22), (22, 23), (23, 20)   # Dolna ściana
    ]

    # Włączenie test głębi.
    glEnable(GL_DEPTH_TEST)

    # Rysowanie każdej ściany sześcianu.
    for i, face in enumerate(faces):
        glBegin(GL_POLYGON)
        glColor3fv(color_red)  # Ustawienie koloru dla danej ściany
        for vertex in face:
            glVertex3fv([vertices[vertex][0] + x, vertices[vertex][1] + y, vertices[vertex][2] + z])
        glEnd()

    # Ustawienie koloru krawędzi na kolor tła - czarny
    glColor3fv(color_black)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv([vertices[vertex][0] + x, vertices[vertex][1] + y, vertices[vertex][2] + z])
    glEnd()

# Definicja funkcji do rysowania sceny.
def draw_scene():
    for x, y, z in cubes:
        glPushMatrix()
        glTranslatef(x, y, z)
        draw_cube(x, y, z)
        glPopMatrix()
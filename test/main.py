import math
from tkinter import *

window_width = 1080
window_height = 720

root = Tk()
root.geometry(f"{window_width}x{window_height}")

maze = [
    [15, 1, 1, 4, 5, 5, 15, 2, 3, 15], 
    [14, 7, 15, 0, 15, 0, 0, 2, 6, 7], 
    [2, 11, 3, 15, 3, 13, 10, 11, 13, 15], 
    [0, 15, 4, 4, 14, 5, 0, 15, 15, 12], 
    [15, 14, 6, 0, 3, 2, 4, 12, 5, 15]
]

maze_height = len(maze)       # 5 lignes
maze_width = len(maze[0])     # 10 colonnes

canva = Canvas(root, width=window_width, height=window_height)
canva.place(x=0, y=0)


angle_L = 20
angle_R = 2 * angle_L + 90  # 150°

def compute_origin(win_w, win_h, maze_w, maze_h, angle_L, angle_R, scale):
    radL = math.radians(angle_L)
    radR = math.radians(angle_R)

    vx_L = math.cos(radL) * scale
    vy_L = -math.sin(radL) * scale
    vx_R = math.cos(radR) * scale
    vy_R = -math.sin(radR) * scale

    xs = [
        0,
        maze_w * vx_R,
        maze_h * vx_L,
        maze_w * vx_R + maze_h * vx_L,
    ]
    ys = [
        0,
        maze_w * vy_R,
        maze_h * vy_L,
        maze_w * vy_R + maze_h * vy_L,
    ]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y

    # Centrer dans la fenêtre
    origin_x = (win_w - width) / 2 - min_x
    origin_y = (win_h - height) / 2 - min_y

    return origin_x, origin_y

def compute_scale(win_w, win_h, maze_w, maze_h, angle_L, angle_R):
    radL = math.radians(angle_L)
    radR = math.radians(angle_R)

    # Vecteurs unitaires (scale = 1)
    vx_L = math.cos(radL)
    vy_L = -math.sin(radL)
    vx_R = math.cos(radR)
    vy_R = -math.sin(radR)

    # Coins du maze avec scale = 1
    xs = [
        0,
        maze_w * vx_R,
        maze_h * vx_L,
        maze_w * vx_R + maze_h * vx_L,
    ]
    ys = [
        0,
        maze_w * vy_R,
        maze_h * vy_L,
        maze_w * vy_R + maze_h * vy_L,
    ]

    width_unit = max(xs) - min(xs)
    height_unit = max(ys) - min(ys)

    # Scale max pour rentrer dans la fenêtre
    sx = win_w / width_unit
    sy = win_h / height_unit

    return min(sx, sy)
start_x, start_y = compute_origin(window_width, window_height, maze_width, maze_height, angle_L, angle_R, compute_scale(window_width, window_height, maze_width, maze_height, angle_L, angle_R))







def draw_with_angle(angle, x, y, dist, canvas, color="red"):
    angle_rad = math.radians(angle)
    end_x = x + math.cos(angle_rad) * dist
    end_y = y - math.sin(angle_rad) * dist
    canvas.create_line(x, y, end_x, end_y, fill=color)
    return end_x, end_y


def decode_walls(cell):
    return {
        "top":    bool(cell & 1),
        "right":  bool(cell & 2),
        "bottom": bool(cell & 4),
        "left":   bool(cell & 8)
    }


def draw_cell(canvas, cell, start_x, start_y, i, j, angle_L, angle_R, scale):
    """
    Dessine une case (i, j) en isométrique selon les murs définis par 'cell'.
    """

    # Vecteur vertical (gauche)
    vx_L = math.cos(math.radians(angle_L)) * scale
    vy_L = -math.sin(math.radians(angle_L)) * scale

    # Vecteur horizontal (droite)
    vx_R = math.cos(math.radians(angle_R)) * scale
    vy_R = -math.sin(math.radians(angle_R)) * scale

    # Position de base de la case
    x0 = start_x + i * vx_R + j * vx_L
    y0 = start_y + i * vy_R + j * vy_L

    walls = decode_walls(cell)

    # Mur gauche
    if walls["left"]:
        draw_with_angle(angle_L, x0, y0, scale, canvas)

    # Mur haut
    if walls["top"]:
        x1, y1 = draw_with_angle(angle_L, x0, y0, scale, canvas)
        draw_with_angle(angle_R, x1, y1, scale, canvas)

    # Mur droite
    if walls["right"]:
        x2, y2 = draw_with_angle(angle_R, x0, y0, scale, canvas)
        draw_with_angle(angle_L, x2, y2, scale, canvas)

    # Mur bas
    if walls["bottom"]:
        draw_with_angle(angle_R, x0, y0, scale, canvas)


def draw_maze_cells(canvas, start_x, start_y, maze, angle_L, angle_R, scale=compute_scale(window_width, window_height, maze_width, maze_height, angle_L, angle_R)):
    for j in range(len(maze)):
        for i in range(len(maze[0])):
            cell = maze[j][i]
            draw_cell(canvas, cell, start_x, start_y, i, j, angle_L, angle_R, scale)


# Dessin du labyrinthe
draw_maze_cells(canva, start_x, start_y, maze, angle_L, angle_R)

root.mainloop()

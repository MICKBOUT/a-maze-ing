from gen import gen_prefect
import tkinter as tk
from random import randint
# -----------------------------
# Labyrinthe fourni
# -----------------------------


# maze = gen_prefect(15, 15)
def get_maze(file_path: str = "output_maze.txt") -> list[list[int]]:
    maze = []
    with open(file_path) as file:
        for i in file:
            line = i.strip()
            if line == "":
                break
            maze.append([int(letter, 16) for letter in line])
    return maze
# -----------------------------
# Paramètres d'affichage
# -----------------------------
CELL = 50  # taille d'une case
WALL_COLOR = "#000000"
BG_COLOR = f"#{randint(30,99):02}{randint(30,99):02}{randint(30,99):02}"

# -----------------------------
# Fonction pour dessiner une cellule
# -----------------------------


def draw_cell(canvas, row, col, value):
    x = col * CELL
    y = row * CELL

    # coordonnées
    x1, y1 = x, y
    x2, y2 = x + CELL, y + CELL

    # Bit 0 → Nord
    if value & 1:
        canvas.create_line(x1, y1, x2, y1, fill=WALL_COLOR, width=2)

    # Bit 1 → Est
    if value & 2:
        canvas.create_line(x2, y1, x2, y2, fill=WALL_COLOR, width=2)

    # Bit 2 → Sud
    if value & 4:
        canvas.create_line(x1, y2, x2, y2, fill=WALL_COLOR, width=2)

    # Bit 3 → Ouest
    if value & 8:
        canvas.create_line(x1, y1, x1, y2, fill=WALL_COLOR, width=2)

# -----------------------------
# Programme principal Tkinter
# -----------------------------


def main():
    maze = get_maze()
    rows = len(maze)
    cols = len(maze[0])

    root = tk.Tk()
    root.title("Labyrinthe bitmask")

    canvas = tk.Canvas(
        root, width=cols * CELL, height=rows * CELL, bg=BG_COLOR)
    canvas.pack()
    # Dessiner le cadre extérieur

    # Dessin du labyrinthe
    for r in range(rows):
        for c in range(cols):
            draw_cell(canvas, r, c, maze[r][c])

    root.mainloop()


if __name__ == "__main__":
    # get_maze()
    main()

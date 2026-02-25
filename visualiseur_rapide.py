from gen import gen
import tkinter as tk

# -----------------------------
# Labyrinthe fourni
# -----------------------------
maze = gen(25, 25)

# -----------------------------
# Paramètres d'affichage
# -----------------------------
CELL = 50  # taille d'une case
WALL_COLOR = "#352208"
BG_COLOR = "#E1BB80"

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
    rows = len(maze)
    cols = len(maze[0])

    root = tk.Tk()
    root.title("Labyrinthe bitmask")

    canvas = tk.Canvas(root, width=cols * CELL, height=rows * CELL, bg=BG_COLOR)
    canvas.pack()
    # Dessiner le cadre extérieur

    # Dessin du labyrinthe
    for r in range(rows):
        for c in range(cols):
            draw_cell(canvas, r, c, maze[r][c])

    root.mainloop()


if __name__ == "__main__":
    main()

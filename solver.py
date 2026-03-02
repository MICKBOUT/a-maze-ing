from gen import gen_perfect, gen_imperfect


def solver_a_star(
        maze: list[list[int]],
        start: tuple[int, int] = (0, 0),
        end: tuple[int, int] = None):
    end = (len(maze) - 1, len(maze[0]) - 1) if end is None else end

    assert maze[start[0]][start[1]] != 15, "Error entry on full block"
    assert maze[end[0]][end[1]] != 15, "Error exit on full block"
    assert start != end, "Start and end need to be diferent"

    y_end, x_end = end
    stack = [[*start, ""]]
    path = {}

    while stack:
        y, x, current_path = stack.pop()
        # North
        if not maze[y][x] & 1:
            if ((y - 1, x) not in path or
               len(current_path) + 1 < len(path[(y - 1, x)])):
                path[(y - 1, x)] = current_path + "N"
                stack.append((y - 1, x, current_path + "N"))
        # East
        if not maze[y][x] & 2:
            if ((y, x + 1) not in path or
               len(current_path) + 1 < len(path[(y, x + 1)])):
                path[(y, x + 1)] = current_path + "E"
                stack.append((y, x + 1, current_path + "E"))
        # South
        if not maze[y][x] & 4:
            if ((y + 1, x) not in path or
               len(current_path) + 1 < len(path[(y + 1, x)])):
                path[(y + 1, x)] = current_path + "S"
                stack.append((y + 1, x, current_path + "S"))
        # West
        if not maze[y][x] & 8:
            if ((y, x - 1) not in path or
               len(current_path) + 1 < len(path[(y, x - 1)])):
                path[(y, x - 1)] = current_path + "W"
                stack.append((y, x - 1, current_path + "W"))

    return path.get(end, None)

# Bit Direction|
# -------------|
# 0 North    1 |
# 1 East     2 |
# 2 South    4 |
# 3 West     8 |


if __name__ == "__main__":
    print("=== perfecte ===")
    maze = gen_perfect(8, 10)
    for row in maze:
        print(row)
    path = solver_a_star(maze)
    print(path)

    print("\n\n=== imperfecte ===")
    maze = gen_imperfect(8, 10)
    for row in maze:
        print(row)
    path = solver_a_star(maze)
    print(path)

from random import randint, choice
import sys


def gen(height: int, width: int) -> list[list[int]]:
    """
    Generate a perfect maze represented as a 2D grid of wall-bit masks.

    Parameters:
    height : int
        Number of rows in the maze (must be a positive integer).
    width : int
        Number of columns in the maze (must be a positive integer).

    Returns:
    list[list[int]]
        A height-by-width 2D list of integers where each integer encodes the
        walls remaining around that cell using the bit layout described above.
    """

    assert height >= 6, "height too small for the 42 logo"
    assert width >= 9, "width need to be >= 7 for the 42 logo"

    grid = [[15 for _ in range(width)] for _ in range(height)]

    mid_height = height // 2
    mid_width = width // 2

    # 42 logo
    seen = {
        # 4
        (mid_height - 2, mid_width - 3),
        (mid_height - 1, mid_width - 3),
        (mid_height, mid_width - 3),
        (mid_height, mid_width - 2),
        (mid_height, mid_width - 1),
        (mid_height, mid_width - 1),
        (mid_height + 1, mid_width - 1),
        (mid_height + 2, mid_width - 1),
        # 2
        (mid_height - 2, mid_width + 1),
        (mid_height - 2, mid_width + 2),
        (mid_height - 2, mid_width + 3),
        (mid_height - 1, mid_width + 3),
        (mid_height, mid_width + 3),
        (mid_height, mid_width + 2),
        (mid_height, mid_width + 1),
        (mid_height + 1, mid_width + 1),
        (mid_height + 2, mid_width + 1),
        (mid_height + 2, mid_width + 2),
        (mid_height + 2, mid_width + 3),
    }

    rnd_cell = (randint(0, height - 1), randint(0, width - 1))
    while rnd_cell in seen:
        rnd_cell = (randint(0, height - 1), randint(0, width - 1))
    stack = [rnd_cell]

    while stack:
        y, x = stack[-1]
        seen.add((y, x))
        candidate = []
        # North
        if y > 0 and (y - 1, x) not in seen:
            candidate.append(0)
        # East
        if x < width - 1 and (y, x + 1) not in seen:
            candidate.append(1)
        # South
        if y < height - 1 and (y + 1, x) not in seen:
            candidate.append(2)
        # West
        if x > 0 and (y, x - 1) not in seen:
            candidate.append(3)
        if not candidate:
            stack.pop()
        else:
            direction = choice(candidate)
            if direction == 0:  # North
                grid[y][x] -= 1  # 0 LSB (least significant bit)
                grid[y - 1][x] -= 4  # 2 LSB
                stack.append((y - 1, x))
            elif direction == 1:  # East
                grid[y][x] -= 2  # 1 LSB
                grid[y][x + 1] -= 8  # 3 LSB
                stack.append((y, x + 1))
            elif direction == 2:  # South
                grid[y][x] -= 4
                grid[y + 1][x] -= 1
                stack.append((y + 1, x))
            elif direction == 3:  # West
                grid[y][x] -= 8
                grid[y][x - 1] -= 2
                stack.append((y, x - 1))
    # north, est, south , west
    return grid


def write_file(
        maze: list[list[int]],
        start: tuple[int, int] = None,
        end: tuple[int, int] = None,
        path: str = "placer_holder") -> str:

    start = (0, 0) if start is None else start
    end = (len(maze) - 1, len(maze[0]) - 1) if end is None else end

    file = "output_maze.txt"
    with open(file, 'w') as f:
        line = ""
        for row in maze:
            for nb in row:
                line += format(nb, "X")
            line += "\n"
        line += "\n"
        line += f"{str(start[0])},{str(start[1])}\n"
        line += f"{str(end[1])},{str(end[0])}\n"
        line += path
        f.write("".join(str(line)))

    return file


def validate_maze(grid: list[list[int]]):
    height = len(grid)
    width = len(grid[0])

    error = []
    for y in range(height - 1):
        for x in range(width - 1):
            if (grid[y][x] >> 2) & 1 != (grid[y + 1][x] >> 0) & 1:
                error.append((y, x, "wrong y"))
            if (grid[y][x] >> 1) & 1 != (grid[y][x + 1] >> 3) & 1:
                error.append((y, x, "wrong x"))

    if error:
        print(error)
    return len(error) == 0


if __name__ == "__main__":
    try:
        grid = gen(height=int(sys.argv[1]), width=int(sys.argv[2]))
    except Exception:
        print("Argv not found")
        grid = gen(height=10, width=10)
    finally:
        write_file(grid, (0, 0), (9, 9))


# Bit Direction|
# -------------|
# 0 North      |
# 1 East       |
# 2 South      |
# 3 West       |

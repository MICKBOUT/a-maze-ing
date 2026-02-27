from random import randint, choice


def gen_prefect(height: int, width: int) -> list[list[int]]:
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

if __name__ == "__main__":
    grid = gen_prefect(height=10, width=10)
    write_file(grid, (0, 0), (9, 9))

# Bit Direction|
# -------------|
# 0 North      |
# 1 East       |
# 2 South      |
# 3 West       |

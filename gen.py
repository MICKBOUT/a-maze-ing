from random import randint, choice, seed
import time
import os


def gen_perfect(width: int, height: int, seed_input: str) -> list[list[int]]:
    """
    Generate a perfect maze (no loops, single path between any two cells) using
    a randomized depth-first search (recursive backtracker) and return it as a
    2D grid of integer cell bitmasks.

    The maze generation reserves a centered "42" logo pattern (cells that will
    not be carved) and chooses a random starting cell outside that pattern.
    The function seeds the random generator either from the provided seed_input
    or by auto-generating one (using os.urandom or time.time), and prints the
    seed used to stdout.

    Parameters
    ----------
    width : int
        Number of columns in the resulting grid. Each row will have this many
        cells. Must be at least 9 to accommodate the centered 42 logo.
    height : int
        Number of rows in the resulting grid. Must be at least 6 to
        accommodate the centered 42 logo.
    seed_input : str | int | None
        Seed value passed to random.seed() to make generation deterministic.
        If None, the string "none" (case-insensitive), or the empty string,
        a seed is auto-generated (os.urandom(4) if available, otherwise the
        current time). The chosen seed is printed to stdout; if a seed is
        provided it is printed as well.

    Returns
    -------
    list[list[int]]
        A height-by-width grid (list of rows) where each cell is an integer
        bitmask representing the presence of the four walls:
          - bit 0 (value 1): north wall
          - bit 1 (value 2): east wall
          - bit 2 (value 4): south wall
          - bit 3 (value 8): west wall
        Cells are initialized to 15 (0b1111, all walls present). When the
        algorithm carves a passage between adjacent cells it clears the
        corresponding bits (subtracts the bit values), so a cleared bit
        indicates an open passage in that direction.

    Raises
    ------
    ValueError
        If height < 6 or width < 9 (these minimums ensure the centered 42
        logo fits within the grid).

    Notes
    -----
    - The algorithm produces a perfect maze: every cell is reachable and there
      are no loops.
    - The centered "42" logo cells are left uncarved (they remain as full-wall
      cells), which affects the maze topology in the central region.
    - The function prints the seed used to stdout for reproducibility.
    """
    if seed_input is None or seed_input.lower() in {"none", ""}:
        try:
            seed_input = int.from_bytes(os.urandom(4), "big")
        except NotImplementedError:
            seed_input = int(time.time())
        print("Seed auto-Generated:", seed_input)
    else:
        print("Seed used:", seed_input)
    seed(seed_input)

    if height < 6:
        raise ValueError("height need to be >= 6 for the 42 logo")
    if width < 9:
        raise ValueError("width need to be >= 9 for the 42 logo")

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


def gen_imperfect(width: int, height: int, seed_input: str):
    """
    Generate an imperfect maze by starting with a perfect maze
    and randomly removing some walls.
    Parameters:
        width : int
            Number of columns in the maze (must be a positive integer).
        height : int
            Number of rows in the maze (must be a positive integer).
    Returns:
        list[list[int]]
            A height-by-width 2D list of integers where each integer encodes
            the walls remaining around that cell
            using the bit layout described above.
    """
    def rm_wall(maze: list[list[int]],
                row: int,
                col: int,
                direction: int,
                ) -> None:
        """
        Remove a wall between the cell at (row, col) and
        its neighbor in the specified direction.
            Parameters:
            maze : list[list[int]]
                The maze represented as a 2D grid of wall-bit masks.
            row : int
                The row index of the cell from which to remove the wall.
            col : int
                The column index of the cell from which to remove the wall.
            direction : int
                The direction of the wall to remove
                (0 for North, 1 for East, 2 for South, 3 for West).
        """
        match direction:
            # North
            case 0:
                maze[row][col] &= ~(1 << 0)
                maze[row - 1][col] &= ~(1 << 2)
            # East
            case 1:
                maze[row][col] &= ~(1 << 1)
                maze[row][col + 1] &= ~(1 << 3)
            # South
            case 2:
                maze[row][col] &= ~(1 << 2)
                maze[row + 1][col] &= ~(1 << 0)
            # West
            case 3:
                maze[row][col] &= ~(1 << 3)
                maze[row][col - 1] &= ~(1 << 1)

    maze = gen_perfect(height, width, seed_input)
    for _ in range((height * width) // 12):
        row = randint(0, height - 1)
        col = randint(0, width - 1)
        if maze[row][col] == 15:
            continue

        candidate = []
        if row > 0 and maze[row - 1][col] != 15:
            candidate.append(0)
        if col < width - 1 and maze[row][col + 1] != 15:
            candidate.append(1)
        if row < height - 1 and maze[row + 1][col] != 15:
            candidate.append(2)
        if col > 0 and maze[row][col - 1] != 15:
            candidate.append(3)

        if not candidate:
            continue
        # else:
        rm_wall(maze, row, col, choice(candidate))
    return maze


if __name__ == "__main__":
    # grid = gen_imprefect(height=10, width=10)
    grid = gen_perfect(width=15, height=10, seed_input=None)

    print("\n=== maze ===")
    for row in grid:
        print(row)

# Bit Direction|
# -------------|
# 0 North      |
# 1 East       |
# 2 South      |
# 3 West       |

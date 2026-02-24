import random


def gen(height: int, width: int) -> list[list[int]]:
    grid = [[15 for _ in range(width)] for _ in range(height)]

    rnd_node = (random.randint(0, height - 1), random.randint(0, width - 1))
    seen = {rnd_node}
    stack = [rnd_node]
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
            direction = random.choice(candidate)
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
    for line in grid:
        print(line)
    return grid


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


# === COLORS ===
RESET = "\033[0m"
WALL  = "\033[100m██\033[0m"   # dark grey wall
EMPTY = "  "                   # empty space

def render_bitmask_maze(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Draw top border
    print(WALL * cols)

    for y in range(rows):
        line = ""
        for x in range(cols):
            cell = grid[y][x]

            # Check walls
            left   = cell & 8
            right  = cell & 2

            # Draw left wall
            if left:
                line += WALL
            else:
                line += EMPTY

            # Draw cell interior
            line += EMPTY

            # Draw right wall
            if right:
                line += WALL
            else:
                line += EMPTY

        print(line)

        # Draw bottom walls
        bottom_line = ""
        for x in range(cols):
            cell = grid[y][x]
            bottom = cell & 4
            if bottom:
                bottom_line += WALL * 2
            else:
                bottom_line += EMPTY * 2
        print(bottom_line)



if __name__ == "__main__":
    grid = gen(height=5, width=3)
    render_bitmask_maze(grid)

# Bit Direction|
# -------------|
# 0 North      |
# 1 East       |
# 2 South      |
# 3 West       |

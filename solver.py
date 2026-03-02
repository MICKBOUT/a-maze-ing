from gen import gen_prefect, gen_imperfect
from heapq import heappop, heappush


def solver_fast(
        maze: list[list[int]],
        start: tuple[int, int] = (0, 0),
        end: tuple[int, int] = None):
    end = (len(maze) - 1, len(maze[0]) - 1) if end is None else end

    assert maze[start[0]][start[1]] != 15, "Error entry on full block"
    assert maze[end[0]][end[1]] != 15, "Error exit on full block"
    assert start != end, "Start and end need to be diferent"

    y_end, x_end = end
    stack = [[*start, ""]]
    heap = []
    y, x = start
    # len(path) + dst + , y, x, path
    seen = {(y, x)}
    heappush(heap, (
        abs(y_end - y) + abs(y_end - x),  # current distance + dst (dst = 0)
        y,
        x,
        "",))

    while heap:
        dst, y, x, current_path = heappop(heap)
        seen.add((y, x))
        if y == y_end and x == x_end:
            return current_path
        # North
        if not maze[y][x] & 1:
            if (y - 1, x) not in seen:
                heappush(heap, (
                    len(current_path) + 1 + abs(y_end - (y - 1)) + abs(x_end - x),
                    y - 1,
                    x,
                    current_path + "N"))
        # East
        if not maze[y][x] & 2:
            if (y, x + 1) not in seen:
                heappush(heap, (
                    len(current_path) + 1 + abs(y_end - y) + abs(x_end - (x + 1)),
                    y,
                    x + 1,
                    current_path + "E"))
        # South
        if not maze[y][x] & 4:
            if (y + 1, x) not in seen:
                heappush(heap, (
                    len(current_path) + 1 + abs(y_end - (y + 1)) + abs(x_end - x),
                    y + 1,
                    x,
                    current_path + "S"))
        # West
        if not maze[y][x] & 8:
            if (y, x - 1) not in seen:
                heappush(heap, (
                    len(current_path) + 1 + abs(y_end - y) + abs(x_end - (x - 1)),
                    y,
                    x - 1,
                    current_path + "W"))

    return path.get(end, None)

# Bit Direction|
# -------------|
# 0 North    1 |
# 1 East     2 |
# 2 South    4 |
# 3 West     8 |


if __name__ == "__main__":
    print("=== perfecte ===")
    maze = gen_prefect(8, 10)
    for row in maze:
        print(row)
    path = solver_fast(maze)
    print(path)

    print("\n\n=== imperfecte ===")
    maze = gen_imperfect(250, 250)
    for row in maze:
        print(row)
    path = solver_fast(maze)
    print(path)

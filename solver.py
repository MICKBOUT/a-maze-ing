from heapq import heappop, heappush
from gen import gen_perfect, gen_imperfect


def solver_fast(
        maze: list[list[int]],
        start: tuple[int, int] = (0, 0),
        end: tuple[int, int] = None):
    end = (len(maze) - 1, len(maze[0]) - 1) if end is None else end

    assert maze[start[0]][start[1]] != 15, "Error entry on full block"
    assert maze[end[0]][end[1]] != 15, "Error exit on full block"
    assert start != end, "Start and end need to be diferent"

    y_end, x_end = end
    heap = []
    y, x = start
    seen = {(y, x)}
    heappush(heap, (
        abs(y_end - y) + abs(y_end - x),
        y, x,
        "",))

    while heap:
        dst, y, x, path = heappop(heap)
        seen.add((y, x))
        if y == y_end and x == x_end:
            return path
        # North
        if not maze[y][x] & 1:
            if (y - 1, x) not in seen:
                heappush(heap, (
                    len(path) + 1 + abs(y_end - (y - 1)) + abs(x_end - x),
                    y - 1,
                    x,
                    path + "N"))
        # East
        if not maze[y][x] & 2:
            if (y, x + 1) not in seen:
                heappush(heap, (
                    len(path) + 1 + abs(y_end - y) + abs(x_end - (x + 1)),
                    y,
                    x + 1,
                    path + "E"))
        # South
        if not maze[y][x] & 4:
            if (y + 1, x) not in seen:
                heappush(heap, (
                    len(path) + 1 + abs(y_end - (y + 1)) + abs(x_end - x),
                    y + 1,
                    x,
                    path + "S"))
        # West
        if not maze[y][x] & 8:
            if (y, x - 1) not in seen:
                heappush(heap, (
                    len(path) + 1 + abs(y_end - y) + abs(x_end - (x - 1)),
                    y,
                    x - 1,
                    path + "W"))

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
    path = solver_fast(maze)
    print(path)

    print("\n\n=== imperfecte ===")
    maze = gen_imperfect(250, 250)
    for row in maze:
        print(row)
    path = solver_fast(maze)
    print(path)

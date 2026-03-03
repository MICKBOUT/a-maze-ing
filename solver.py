from heapq import heappop, heappush
from gen import gen_perfect, gen_imperfect


def solver_fast(
        maze: list[list[int]],
        start: tuple[int, int] = (0, 0),
        end: tuple[int, int] = None) -> str:
    """
    Solves a maze using the A* algorithm and returns the path as a string of
    directions.

    Parameters:
        maze (list[list[int]]): The maze represented as a 2D list of integers,
        where each integer encodes wall information.
        start (tuple[int, int], optional): The starting position in the maze
        as (x, y). Defaults to (0, 0).
        end (tuple[int, int], optional): The ending position in the maze as
        (x, y). If None, must be provided by the caller.

    Returns:
        str: A string representing the path from start to end using
        'N', 'E', 'S', 'W' for directions.

    Raises:
        ValueError: If the start or end position is on a full block.
        Exception: If no path is found.
    """
    x, y = start
    if maze[y][x] == 15:
        raise ValueError("Error entry on full block")
    x_end, y_end = end
    if maze[y_end][x_end] == 15:
        raise ValueError("Error exit on full block")

    heap = []
    seen = {(y, x)}
    heappush(heap, (
        abs(y_end - y) + abs(x_end - x),
        y, x,
        "",))

    while heap:
        _, y, x, path = heappop(heap)
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
    raise Exception("No path found")


if __name__ == "__main__":
    print("=== perfecte ===")
    maze = gen_perfect(8, 10)
    for row in maze:
        print(row)
    path = solver_fast(maze)
    print(path)

    print("\n\n=== imperfecte ===")
    maze = gen_imperfect(10, 250)
    for row in maze:
        print(row)
    path = solver_fast(maze)
    print(path)

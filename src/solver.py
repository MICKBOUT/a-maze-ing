from heapq import heappop, heappush
from .mazegen.generation import MazeGenerator
from .exception import PathNotFound


def solver_heap(
        maze: list[list[int]],
        start: tuple[int, int],
        end: tuple[int, int]) -> str:
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
    coeff = 5
    x, y = start

    if 0 < y <= len(maze):
        print(ValueError("Error: Start outside the maze"))
        exit()
    if 0 < x <= len(maze[0]):
        print(ValueError("Error: Start outside the maze"))
        exit()
    if maze[y][x] == 15:
        print(ValueError("Error: entry on full block"))
        exit()
    x_end, y_end = end


    if 0 < y_end <= len(maze):
        print(ValueError("Error: Exit outside the maze"))
        exit()
    if 0 < x_end <= len(maze[0]):
        print(ValueError("Error: Exit outside the maze"))
        exit()
    if maze[y_end][x_end] == 15:
        print(ValueError("Error: exit on full block"))
        exit()

    heap = []
    seen = {(x, y)}
    heappush(heap, (
        (abs(x_end - x) + abs(y_end - y)) * coeff,
        x, y,
        "",))
    stack_visual = []
    while heap:
        _, x, y, path = heappop(heap)
        if (x, y) not in seen:
            stack_visual.append((x, y))
        seen.add((x, y))
        if y == y_end and x == x_end:
            return path, stack_visual
        # North
        if not maze[y][x] & 1:
            if (x, y - 1) not in seen:
                heappush(heap, (
                    len(path) + 1 + (
                        abs(x_end - x) + abs(y_end - (y - 1))) * coeff,
                    x,
                    y - 1,
                    path + "N"))
        # East
        if not maze[y][x] & 2:
            if (x + 1, y) not in seen:
                heappush(heap, (
                    len(path) + 1 + (
                        abs(x_end - (x + 1)) + abs(y_end - y)) * coeff,
                    x + 1,
                    y,
                    path + "E"))
        # South
        if not maze[y][x] & 4:
            if (x, y + 1) not in seen:
                heappush(heap, (
                    len(path) + 1 + (
                        abs(x_end - x) + abs(y_end - (y + 1))) * coeff,
                    x,
                    y + 1,
                    path + "S"))
        # West
        if not maze[y][x] & 8:
            if (x - 1, y) not in seen:
                heappush(heap, (
                    len(path) + 1 + (
                        abs(x_end - (x - 1)) + abs(y_end - y)) * coeff,
                    x - 1,
                    y,
                    path + "W"))
    raise PathNotFound


if __name__ == "__main__":

    import time

    maze = MazeGenerator.maze_generator(200, 200, None, False)
    print("\n\n=== imperfecte ===")
    t = time.time()
    path = solver_heap(
        maze=maze,
        start=(0, 0),
        end=(199, 199)
    )
    print(f"{time.time()- t}")

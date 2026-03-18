from heapq import heappop, heappush


class MisplaceCell(Exception):
    """
    Exception raised when a key cell is placed on the 42 logo in the maze.
    """
    def __init__(self, message: str = "Key cell place on 42 logo"):
        self.message = message
        super().__init__(self.message)


def solver_heap(
        maze: list[list[int]],
        start: tuple[int, int],
        end: tuple[int, int]) -> tuple[str | None, list[tuple[int, int]]]:
    """
    Solve the maze using a heuristic-based search algorithm (A*).
    The function takes a maze represented as a 2D list of integers, the entry
    and exit points as tuples of coordinates. It returns a tuple containing the
    solution path as a string of directions (N, E, S, W) or None if no path is
    found, and a list of coordinates representing the progress stack from the
    maze-solving process. The algorithm uses a priority queue (min-heap) to
    explore the maze, prioritizing paths that are estimated to be closer to the
    exit point based on the Manhattan distance heuristic. If the entry or exit
    points are invalid (e.g., outside the maze boundaries or on a cell with the
    42 logo), a MisplaceCell exception is raised with an appropriate message.

    Parameters
    ----------
    maze : list[list[int]]
        A 2D list representing the maze, where each cell contains an integer
        encoding the presence of walls in the four cardinal directions.
    start : tuple[int, int]
        A tuple representing the coordinates (x, y) of the entry point in the
        maze.
    end : tuple[int, int]
        A tuple representing the coordinates (x, y) of the exit point in the
        maze.

    Returns
    -------
    tuple[str | None, list[tuple[int, int]]]
        A tuple containing the solution path as a string of directions
        (N, E, S, W) or None if no path is found, and a list of coordinates
        representing the progress stack from the maze-solving process.
    """
    coeff = 5

    x, y = start
    if not (0 <= y < len(maze)):
        raise ValueError("Entry outside the maze")
    if not (0 <= x < len(maze[0])):
        raise ValueError("Entry outside the maze")
    if maze[y][x] == 15:
        raise MisplaceCell("Entry on logo 42")

    x_end, y_end = end
    if not (0 <= y_end < len(maze)):
        raise ValueError("Exit outside the maze")
    if not (0 <= x_end < len(maze[0])):
        raise ValueError("Exit outside the maze")
    if maze[y_end][x_end] == 15:
        raise MisplaceCell("Exit on logo 42")

    heap: list[tuple[int, int, int, str]] = []
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

    return None, stack_visual

from gen import gen_prefect, gen_imperfect
from solver import solver_a_star


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
        line += f"{str(end[0])},{str(end[1])}\n"
        line += path
        f.write("".join(str(line)))

    return file


def validate_maze(grid: list[list[int]]):
    height = len(grid)
    width = len(grid[0])

    error = []
    for y in range(height - 1):
        for x in range(width - 1):
            if (grid[y][x] >> 2) & 1 != grid[y + 1][x] & 1:
                error.append((y, x, "wrong y"))
            if (grid[y][x] >> 1) & 1 != (grid[y][x + 1] >> 3) & 1:
                error.append((y, x, "wrong x"))

    if error:
        print(error)
    return len(error) == 0


def main() -> None:
    maze = gen_imperfect(25, 25)
    if not validate_maze(maze):
        raise Exception("Maze Not validate")
    else:
        print("maze validate (No wall on a single side1)")
    path = solver_a_star(maze)
    if path is None:
        raise Exception("Path Not found")
    else:
        print("Solution found", f"{len(path)} move")

    write_file(maze, path=path)


if __name__ == "__main__":
    main()

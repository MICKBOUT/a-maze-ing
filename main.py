from gen import gen_imperfect, gen_perfect
from solver import solver_fast
from sys import argv


def write_file(
        maze: list[list[int]],
        start: tuple[int, int] = None,
        end: tuple[int, int] = None,
        path: str = "Placer_holder",
        file_output: str = "output_maze.txt") -> str:
    """
    Write the given 2-D integer maze to a text file.

    Each row of the maze is written on its own line; each cell is formatted
    using uppercase hexadecimal (format(cell, "X")) with no separators.
    After all rows are written a blank line is added, then the start
    coordinates as "row,col" on a line, the end coordinates as "row,col" on
    the next line, and finally the path string appended as-is.

    Parameters
    ----------
    maze : list[list[int]]
        2-D list representing the maze grid (rows of integer cells).
    start : tuple[int, int], optional
        (row, column) coordinates of the start cell.
        If None, defaults to (0, 0).
    end : tuple[int, int], optional
        (row, column) coordinates of the end cell. If None, defaults to
        (len(maze) - 1, len(maze[0]) - 1).
    path : str, optional
        Arbitrary string describing or representing the path; written verbatim
        after the coordinates. Defaults to "Placer_holder".
    file_output : str, optional
        Filesystem path to write the output to. Defaults to "output_maze.txt".

    Returns
    -------
    str
        The path of the file that was written (the value of file_output).

    Raises
    ------
    IndexError
        If maze is empty or rows are inconsistent such that computing default
        end coordinates or iterating rows fails.
    OSError
        If the file cannot be opened or written.
    """
    start = (0, 0) if start is None else start
    end = (len(maze) - 1, len(maze[0]) - 1) if end is None else end
    file = file_output
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


def validate_maze(grid: list[list[int]]) -> bool:
    height = len(grid)
    width = len(grid[0])

    error = []
    for y in range(height):
        for x in range(width):
            if y < height - 1 and ((grid[y][x] >> 2) & 1) != (
               grid[y + 1][x] & 1):
                error.append((y, x, "wrong y"))
            if x < width - 1 and ((grid[y][x] >> 1) & 1) != (
               (grid[y][x + 1] >> 3) & 1):
                error.append((y, x, "wrong x"))

    if error:
        raise Exception(f"maze not validate: {error}")
    print("maze validate")
    return True


def load_file(file_name: str, config_dict: dict) -> None:
    """
    Loads maze configuration parameters from a file and updates the provided
    config_dict.

    Parameters
    ----------
    file_name : str
        Path to the configuration file to read.
    config_dict : dict
        Dictionary to update with configuration values parsed from the file.

    Raises
    ------
    Exception
        If the file cannot be opened or parsed,
        or if an error occurs during processing.
    """
    try:
        with open(file_name, "r") as file:
            for line in [line.strip() for line in file if line[0] != '#']:
                variable, data = line.split("=")
                variable = variable.lower()

                if variable in {"width", "height"}:
                    config_dict[variable] = int(data)
                elif variable in {"entry", "exit"}:
                    x, y = data.split(',')
                    config_dict[variable] = (int(x), int(y))
                elif variable == "output_file":
                    config_dict[variable] = data
                elif variable == "perfect":
                    if data.lower() == "true":
                        config_dict["perfect"] = True
                    elif data.lower() == "false":
                        config_dict["perfect"] = False
                else:

                    print("unused parameter", variable, data)

    except Exception as e:
        print("Error:", e)


def get_maze(file_path: str = "output_maze.txt") -> list[list[int]]:
    maze = []
    with open(file_path) as file:
        for i in file:
            line = i.strip()
            if line == "":
                break
            maze.append([int(letter, 16) for letter in line])
    return maze


def main() -> None:
    config_dict = {
        "width": 20,
        "height": 20,
        "entry": (0, 0),
        "exit": (19, 19),
        "output_file": "output_maze.txt",
        "perfect": True,
        "animation": False,
    }
    if len(argv) > 1:
        load_file(argv[1], config_dict)

    if config_dict["perfect"]:
        maze = gen_perfect(config_dict["height"], config_dict["width"])
    else:
        maze = gen_imperfect(config_dict["height"], config_dict["width"])

    path = solver_fast(maze, config_dict["entry"], config_dict["exit"])

    write_file(
        maze,
        config_dict["entry"],
        config_dict["exit"],
        path,
        config_dict["output_file"]
    )


if __name__ == "__main__":
    main()

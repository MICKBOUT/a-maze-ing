import sys
 
from .mazegen.generation import MazeGenerator
from .solver import solver_heap
from .exception import ConfigFileError

config_dict = {
    "width": 75,
    "height": 50,
    "entry": (37, 25),
    "exit": (0, 0),
    "output_file": "output_maze.txt",
    "perfect": False,
    "seed": None
}


def write_file(
        maze: list[list[int]],
        start: tuple[int, int],
        end: tuple[int, int],
        path: str,
        file) -> str:
    """
    Write the given 2-D integer maze to a text file.
    Each row of the maze is written on its own line; each cell is formatted
    using uppercase hexadecimal (format(cell, "X")) with no separators.
    After all rows are written a blank line is added, then the start
    coordinates as "row,col" on a line, the end coordinates as "row,col"
    on the next line, and finally the path string appended as-is.

    Parameters
    ----------
    maze : list[list[int]]
        2-D list representing the maze grid (rows of integer cells).
    start : tuple[int, int]
        (row, column) coordinates of the start cell.
        If None, defaults to (0, 0).
    end : tuple[int, int]
        (row, column) coordinates of the end cell. If None, defaults to
        (len(maze) - 1, len(maze[0]) - 1).
    path : str
        Arbitrary string describing or representing the path; written verbatim
        after the coordinates. Defaults to "Placer_holder".
    file : str
        Filesystem path to write the output to. Defaults to "output_maze.txt".

    Returns
    -------
    str
        The path of the file that was written (the value of file_output).
    """
    try:
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
    except Exception as e:
        print(e)
        sys.exit()
    return file


def load_file(file_name: str, config_dict: dict) -> None:
    """
    Load configuration parameters from a file and update the provided
    configuration dictionary accordingly. The file is expected to contain lines
    in the format "KEY=VALUE", where KEY is a configuration parameter and VALUE
    is its corresponding value. Lines that are empty or start with '#' are
    ignored. The function updates the config_dict with the values from the
    file, converting them to the appropriate types based on the expected
    configuration parameters.

    Parameters
    ----------
    file_name : str
        The path to the configuration file to be loaded.
    config_dict : dict
        A dictionary to be updated with the configuration parameters from the
        file.
    Raises
    ------
    ConfigFileError
        If there is an error in the configuration file, such as an unrecognized
        key, invalid value format, or other parsing issues. The error message
        will include details about the specific issue and the line number where
        it occurred.
    """
    try:
        index = None
        line = None
        with open(file_name, "r") as file:
            for index, line in enumerate(
                    [line.strip() for line in file
                     if line.strip() and line.strip()[0] != '#']):
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
                    if data.lower() in {"true", 1, "yes", "y"}:
                        config_dict["perfect"] = True
                    elif data.lower() in {"false", 0, "no", "n"}:
                        config_dict["perfect"] = False
                    else:
                        raise Exception("bool not found")
                elif variable == "seed":
                    config_dict["seed"] = data
                else:
                    raise Exception("KEY not used")
    except Exception as e:
        print(ConfigFileError(f"{e}", line=line, line_nb=index))
        sys.exit()


def new_maze(new_seed: bool = False) -> list[tuple[int, int]]:
    """
    Generate a new maze based on the configuration parameters provided in a
    file. If a configuration file is provided as a command-line argument, it
    will be loaded to update the default configuration parameters. If the
    new_seed parameter is set to True, the seed value in the configuration will
    be reset to None, allowing for a new random seed to be generated for
    the maze. The function generates the maze, solves it using a heap-based
    solver, and writes the maze and solution path to an output file specified
    in the configuration.

    Parameters
    ----------
    new_seed : bool, optional
        If True, resets the seed value in the configuration to None to allow
        for a new random seed to be generated. Defaults to False.

    Returns
    -------
    list[tuple[int, int]]
        A list of (x, y) coordinates representing the progress stack from the
        maze-solving process. This stack can be used for visualization or
        analysis of the solver's path through the maze.
    """
    if len(sys.argv) > 1:
        load_file(sys.argv[1], config_dict)
    else:
        print("config file missing")
        print("default value used")

    if new_seed:
        config_dict["seed"] = None

    maze = MazeGenerator(
            width=config_dict["width"],
            height=config_dict["height"],
            perfect=config_dict["perfect"],
            seed_input=config_dict["seed"],
    ).maze

    path, progress_stack = solver_heap(
        maze,
        config_dict["entry"],
        config_dict["exit"]
    )
    write_file(
        maze,
        config_dict["entry"],
        config_dict["exit"],
        path,
        config_dict["output_file"]
    )
    return progress_stack

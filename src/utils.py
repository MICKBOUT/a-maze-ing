from typing import Optional, Tuple, TypedDict

from .mazegen.generation import MazeGenerator
from .solver import solver_heap
from .exception import ConfigFileError, PathNotFound


class MazeConfig(TypedDict):
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[str]


config_dict: MazeConfig = {
    "width": 75,
    "height": 50,
    "entry": (37, 25),
    "exit": (0, 0),
    "output_file": "output_maze.txt",
    "perfect": False,
    "seed": None
}


def validate_data(config_dict: MazeConfig) -> None:
    if config_dict["entry"] == config_dict["exit"]:
        raise ConfigFileError("Entry and Exit can not be on the same cell")
    if config_dict["width"] < 7:
        raise ConfigFileError("width to small for the logo '42'")
    if config_dict["height"] < 5:
        raise ConfigFileError("width to small for the logo '42'")

    x, y = config_dict["entry"]
    if not (0 <= y < config_dict["height"]):
        raise ConfigFileError("Entry outside the maze")
    if not (0 <= x < config_dict["width"]):
        raise ConfigFileError("Entry outside the maze")

    x_end, y_end = config_dict["exit"]
    if not (0 <= y_end < config_dict["height"]):
        raise ConfigFileError("Exit outside the maze")
    if not (0 <= x_end <= config_dict["width"]):
        raise ConfigFileError("Exit outside the maze")


def write_file(
        maze: list[list[int]],
        start: Tuple[int, int],
        end: Tuple[int, int],
        path: str,
        file: str) -> str:
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
    except Exception:
        raise ConfigFileError(f"Unable to write in the file '{file}'")
    return file


def load_file(file_name: str, config_dict: MazeConfig) -> None:
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
        index = line = None
        with open(file_name, "r") as file:
            for index, line in enumerate(
                    [line.strip() for line in file
                     if line.strip() and line.strip()[0] != '#']):
                variable, data = line.split("=")
                variable = variable.lower()

                if variable in {"width", "height"}:
                    if variable == "width":
                        config_dict["width"] = int(data)
                    else:
                        config_dict["height"] = int(data)
                elif variable in {"entry", "exit"}:
                    x, y = data.split(',')
                    if variable == "entry":
                        config_dict["entry"] = (int(x), int(y))
                    else:
                        config_dict["exit"] = (int(x), int(y))
                elif variable == "output_file":
                    config_dict["output_file"] = data
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
    except FileNotFoundError:
        raise ConfigFileError("This programge need the file 'config.txt'")
    except Exception as e:
        raise ConfigFileError(f"{e}", line=line, line_nb=index)


def new_maze(config_file: str = "config.txt", new_seed: bool = False
             ) -> tuple[list[int], str]:
    """
    Generate a new maze based on the configuration parameters specified in a
    given configuration file. The function reads the configuration parameters
    from the file, generates a maze using the MazeGenerator class, solves the
    maze using the solver_heap function, and writes the maze and solution path
    to an output file. The function returns the progress stack from the
    maze-solving process and the path to the output file.

    Parameters
    ----------
    config_file : str, optional
        The path to the configuration file containing the maze generation and
        solving parameters. Defaults to "config_file.txt".
    new_seed : bool, optional
        If True, the seed value in the configuration will be ignored and set to
        None, resulting in a new random seed being used for maze generation.
        Defaults to False.
    Returns
    -------
    tuple
        A tuple containing:
        - progress_stack: A list of tuples representing the progress of the
            maze solving process.
        - output_file: A string representing the path to the output file where
            the maze and solution path have been written.

    Raises
    ------
    ConfigFileError
        If there is an error in the configuration file, such as an unrecognized
        key, invalid value format, or other parsing issues. The error message
        will include details about the specific issue and the line number where
        it occurred.
    """

    load_file(config_file, config_dict)
    validate_data(config_dict)

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
    if path is None:
        raise PathNotFound

    write_file(
        maze,
        config_dict["entry"],
        config_dict["exit"],
        path,
        config_dict["output_file"]
    )
    return progress_stack, config_dict["output_file"]

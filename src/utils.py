from typing import Tuple, TypedDict

from mazegen.generation import MazeGenerator
from mazegen.solver import solver_heap
from exception import ConfigFileError, PathNotFound


class MazeConfig(TypedDict):
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: str


config_dict: MazeConfig = {
    "width": 75,
    "height": 50,
    "entry": (37, 25),
    "exit": (0, 0),
    "output_file": "output_maze.txt",
    "perfect": False,
    "seed": ""
}


def validate_data(config_dict: MazeConfig) -> None:
    """
    Validate the configuration parameters for maze generation and solving.
    This function checks the validity of the configuration parameters provided
    in the config_dict. It ensures that the entry and exit points are not the
    same, that the width and height of the maze are sufficient for the logo
    '42', and that the entry and exit points are within the bounds of the maze
    dimensions. If any of the validation checks fail, a ConfigFileError is
    raised with an appropriate error message indicating the specific issue with
    the configuration parameters.

    Parameters
    ----------
    config_dict : MazeConfig
        A dictionary containing the configuration parameters for maze
        generation and solving. The expected keys in the dictionary include
        "width", "height", "entry", "exit", "output_file", "perfect", and
        "seed". The function validates the values associated with these keys to
        ensure they meet the necessary criteria for successful maze generation
        and solving.
    Raises
    ------
    ConfigFileError
        If any of the validation checks fail, such as if the entry and exit
        points are the same, if the width or height of the maze is too small
        for the logo '42', or if the entry or exit points are outside the
        bounds of the maze dimensions. The error message will indicate the
        specific issue with the configuration parameters.
    """
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
    if not (0 <= x_end < config_dict["width"]):
        raise ConfigFileError("Exit outside the maze")


def write_file(
        maze: list[list[int]],
        start: Tuple[int, int],
        end: Tuple[int, int],
        path: str,
        file: str) -> str:
    """
    Write the maze configuration and solution path to a specified output file.
    The function takes the maze as a 2D list of integers, the entry and exit
    points as tuples of coordinates, the solution path as a string, and the
    output file name. It formats the maze and solution information into a
    string and writes it to the specified file. If there is an error during the
    file writing process, a ConfigFileError is raised with details about the
    issue.

    Parameters
    ----------
    maze : list[list[int]]
        A 2D list representing the maze, where each element is an integer
        indicating the type of cell (e.g., wall, path).
    start : Tuple[int, int]
        A tuple representing the coordinates of the entry point in the maze
        (x, y).
    end : Tuple[int, int]
        A tuple representing the coordinates of the exit point in the maze
        (x, y).
    path : str
        A string representing the solution path through the maze, typically
        using characters to indicate directions (e.g., 'N', 'S', 'E', 'W').
    file : str
        The name of the output file where the maze and solution will be
        written.

    Returns
    -------
    str
        The name of the output file where the maze and solution were written.
    Raises
    ------
    ConfigFileError
        If there is an error during the file writing process, such as issues
        with file permissions, invalid file name, or other I/O errors. The
        error message will include details about the specific issue
        encountered.
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
    Load configuration parameters from a text file into a dictionary.
    The function reads the specified file line by line, parsing key-value pairs
    in the format "key=value". It ignores empty lines and lines starting with
    '#'. The recognized keys are "width", "height", "entry", "exit",
    "output_file", "perfect", and "seed". The values are processed and stored
    in the provided config_dict. If the file is not found or if there are
    parsing errors, a ConfigFileError is raised with details about the issue
    and the line number where it occurred.

    Parameters
    ----------
    file_name : str
        The path to the configuration file to be loaded.
    config_dict : dict
        A dictionary to store the loaded configuration parameters. The function
        updates this dictionary with the values read from the file.
    Raises
    ------
    ConfigFileError
        If the specified file is not found, or if there are parsing errors such
        as unrecognized keys, invalid value formats, or other issues. The error
        message will include details about the specific issue and the line
        number where it occurred.
    """
    try:
        index = line = None
        with open(file_name, "r") as file:
            for index, line in enumerate(
                    [line.strip() for line in file], start=1):
                if not line or line[0] == '#':
                    continue
                variable, data = line.split("=", maxsplit=1)
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
                    if data.lower() in {"true", '1', "yes", "y"}:
                        config_dict["perfect"] = True
                    elif data.lower() in {"false", '0', "no", "n"}:
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
             ) -> tuple[list[tuple[int, int]], str]:
    """
    Generate a new maze based on the configuration parameters specified in a
    configuration file. The function reads the configuration from the specified
    file, validates the parameters, generates a maze using the MazeGenerator
    class, and solves the maze using the solver_heap function. The resulting
    maze, along with the entry and exit points, is then written to an output
    file. The function returns a tuple containing the progress stack from the
    maze-solving process and the path to the output file.

    Parameters
    ----------
    config_file : str, optional
        The path to the configuration file to be loaded. Defaults to
        "config.txt".
    new_seed : bool, optional
        If True, the seed value in the configuration will be ignored and a new
        maze will be generated with a random seed. Defaults to False.
    Returns
    -------
    tuple[list[tuple[int, int]], str]
        A tuple containing the progress stack from the maze-solving process and
        the path to the output file where the maze and solution are written.
    Raises
    ------
    ConfigFileError
        If there is an error in the configuration file, such as an unrecognized
        key, invalid value format, or other parsing issues. The error message
        will include details about the specific issue and the line number where
        it occurred.
    PathNotFound
        If the maze-solving algorithm fails to find a path from the entry point
        to the exit point in the generated maze.
    """

    load_file(config_file, config_dict)
    validate_data(config_dict)

    if new_seed:
        config_dict["seed"] = ""

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

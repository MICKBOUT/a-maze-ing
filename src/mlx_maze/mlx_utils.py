from random import randint
from pathlib import Path
from PIL import Image
from enum import Enum
from typing import Any, TypedDict


class MazeFileData(TypedDict):
    maze_data: list[list[int]]
    start: tuple[int, int]
    end: tuple[int, int]
    path: str


class MazeData:
    """
    Load and store maze structure and metadata.

    This class parses the maze file and exposes the grid, dimensions,
    start/end coordinates, and the solution path.
    """
    def __init__(self, heap: list[tuple[int, int]], filename: str) -> None:
        """
        Initialize the maze data by parsing the maze file.
        """
        print(heap)
        self.parse(heap, filename)

    def parse(self, heap: list[tuple[int, int]], filename: str) -> None:
        """
        Parse the maze file and extract structural information.

        The method loads:
        - the maze grid (hex-encoded wall bitmasks),
        - maze dimensions,
        - start and end coordinates,
        - the solution path.

        All values are stored as attributes of the instance.
        """
        parsed = read_file(filename)
        self.maze: list[list[int]] = parsed["maze_data"]
        self.heap: list[tuple[int, int]] = heap
        self.height: int = len(self.maze)
        self.width: int = len(self.maze[0])
        self.start: tuple[int, int] = parsed["start"]
        self.end: tuple[int, int] = parsed["end"]
        self.path: str = parsed["path"]


def create_colors() -> dict[str, list[int]]:
    """
    Generate randomized RGBA colors for maze rendering.

    Returns
    -------
    dict
        Dictionary containing two RGBA lists:
        - "background": bright base color
        - "wall": darker variant derived from the background
    """
    colors = {
        "background": [
            randint(128, 255),
            randint(128, 255),
            randint(128, 255)
        ] + [255]
    }

    colors["wall"] = (
        [c - randint(64, 128) for c in colors["background"][:-1]] + [255]
    )

    return colors


def rescale_image(filename: str,
                  new_size: tuple[int, int]) -> tuple[Any, str]:
    """
    Resize an image and save it into the rescaled assets directory.

    Parameters
    ----------
    filename : str
        Path to the source image.
    new_size : tuple
        Target size as (width, height).

    Returns
    -------
    tuple
        The resized PIL image and the output file path as a string.
    """
    input_path = Path(filename)
    output_dir = Path("assets/rescaled")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "buttons.png"

    img = Image.open(input_path)
    resized = img.resize(new_size, Image.Resampling.LANCZOS)
    resized.save(output_path)

    return resized, str(output_path)


def read_file(file_name: str = "output_maze.txt") -> MazeFileData:
    """
    Read and parse a maze description file.

    Parameters
    ----------
    file_name : str, optional
        Path to the maze file. Defaults to "output_maze.txt".

    Returns
    -------
    dict
        Parsed maze data containing:
        - "maze_data": 2D list of wall bitmasks
        - "start": (x, y) start coordinates
        - "end": (x, y) end coordinates
        - "path": string representing the solution path
    """
    with open(file_name, 'r') as file:
        data = [line.strip() for line in file]

    start_vals: tuple[int, ...] = tuple(int(n) for n in data[-3].split(","))
    end_vals: tuple[int, ...] = tuple(int(n) for n in data[-2].split(","))

    start = (start_vals[0], start_vals[1])
    end = (end_vals[0], end_vals[1])

    return {
        "maze_data": [[int(c, 16) for c in line] for line in data[:-4]],
        "start": start,
        "end": end,
        "path": data[-1]
    }


class Colors(Enum):
    """A basic Enum for maze colors."""
    BACKGROUND = "background"
    WALL = "wall"


buttons_size = (580, 1946)
button1_box = (2900, 450, 3440, 600)
button2_box = (2900, 750, 3440, 900)
button3_box = (2900, 1050, 3440, 1200)
button4_box = (2900, 1320, 3440, 1490)

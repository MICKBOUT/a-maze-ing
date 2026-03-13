import random
import os
import time

from .solver import solver_heap


class MazeGenerator:
    """

    A class to generate a maze with a 42 logo in the center. The maze can be
    perfect (no loops) or imperfect (with loops). The maze is represented as
    a 2D list of integers, where each integer encodes the presence of walls
    in the four cardinal directions (North, East, South, West) using a 4-bit
    binary representation. The class provides methods to generate the maze and
    to find a path from an entry point to an exit point using a maze-solving
    algorithm.

    Attributes
    ----------
    width : int
        The width of the maze.
    height : int
        The height of the maze.
    perfect : bool
        A flag indicating whether the maze should be perfect (no loops) or
        imperfect (with loops).
    maze : list[list[int]]
        A 2D list representing the maze, where each cell contains an integer
        encoding the presence of walls in the four cardinal directions.

    """
    def __init__(
      self, width: int, height: int, perfect: bool, seed_input: str = ""
    ) -> None:
        self.width = width
        self.height = height
        self.perfect = perfect
        self.maze: list[list[int]] = []

        if self.width < 7:
            raise ValueError("width too smale for a maze w/ logo")
        if self.height < 5:
            raise ValueError("height too smale for a maze w/ logo")

        self.generator(seed_input)

    def _gen_perfect(self) -> None:
        height, width = self.height, self.width
        self.maze = [[15 for _ in range(width)] for _ in range(height)]
        mid_height = height // 2
        mid_width = width // 2

        # 42 logo
        seen = {
            # 4
            (mid_height - 2, mid_width - 3),
            (mid_height - 1, mid_width - 3),
            (mid_height, mid_width - 3),
            (mid_height, mid_width - 2),
            (mid_height, mid_width - 1),
            (mid_height, mid_width - 1),
            (mid_height + 1, mid_width - 1),
            (mid_height + 2, mid_width - 1),
            # 2
            (mid_height - 2, mid_width + 1),
            (mid_height - 2, mid_width + 2),
            (mid_height - 2, mid_width + 3),
            (mid_height - 1, mid_width + 3),
            (mid_height, mid_width + 3),
            (mid_height, mid_width + 2),
            (mid_height, mid_width + 1),
            (mid_height + 1, mid_width + 1),
            (mid_height + 2, mid_width + 1),
            (mid_height + 2, mid_width + 2),
            (mid_height + 2, mid_width + 3),
        }

        stack = [
            (mid_height + 1, mid_width - 2),  # bottom left of the 4
            (mid_height, mid_width),  # b/w 4 and 2
            (mid_height + 1, mid_width + 2),  # bottom part of the 2
        ]

        while stack:
            y, x = stack[-1]
            seen.add((y, x))

            candidate = []
            # North
            if y > 0 and (y - 1, x) not in seen:
                candidate.append(0)
            # East
            if x < width - 1 and (y, x + 1) not in seen:
                candidate.append(1)
            # South
            if y < height - 1 and (y + 1, x) not in seen:
                candidate.append(2)
            # West
            if x > 0 and (y, x - 1) not in seen:
                candidate.append(3)
            if not candidate:
                stack.pop()
            else:
                direction = random.choice(candidate)
                if direction == 0:  # North
                    self.maze[y][x] -= 1  # 0 LSB (least significant bit)
                    self.maze[y - 1][x] -= 4  # 2 LSB
                    stack.append((y - 1, x))
                elif direction == 1:  # East
                    self.maze[y][x] -= 2  # 1 LSB
                    self.maze[y][x + 1] -= 8  # 3 LSB
                    stack.append((y, x + 1))
                elif direction == 2:  # South
                    self.maze[y][x] -= 4
                    self.maze[y + 1][x] -= 1
                    stack.append((y + 1, x))
                elif direction == 3:  # West
                    self.maze[y][x] -= 8
                    self.maze[y][x - 1] -= 2
                    stack.append((y, x - 1))

    def _gen_imperfect(self) -> None:
        def rm_wall(row: int,
                    col: int,
                    direction: int,
                    ) -> None:
            match direction:
                # North
                case 0:
                    self.maze[row][col] &= ~(1 << 0)
                    self.maze[row - 1][col] &= ~(1 << 2)
                # East
                case 1:
                    self.maze[row][col] &= ~(1 << 1)
                    self.maze[row][col + 1] &= ~(1 << 3)
                # South
                case 2:
                    self.maze[row][col] &= ~(1 << 2)
                    self.maze[row + 1][col] &= ~(1 << 0)
                # West
                case 3:
                    self.maze[row][col] &= ~(1 << 3)
                    self.maze[row][col - 1] &= ~(1 << 1)

        width, height = len(self.maze[0]), len(self.maze)
        for _ in range((height * width) // 12):
            row = random.randint(0, height - 1)
            col = random.randint(0, width - 1)
            if self.maze[row][col] == 15:
                continue

            candidate = []
            if row > 0 and self.maze[row - 1][col] != 15:
                candidate.append(0)
            if col < width - 1 and self.maze[row][col + 1] != 15:
                candidate.append(1)
            if row < height - 1 and self.maze[row + 1][col] != 15:
                candidate.append(2)
            if col > 0 and self.maze[row][col - 1] != 15:
                candidate.append(3)

            if candidate:
                rm_wall(row, col, random.choice(candidate))

    def generator(self, seed_input: str) -> None:
        if not seed_input:
            try:
                seed_input = str(int.from_bytes(os.urandom(4), "big"))
            except NotImplementedError:
                seed_input = str(int(time.time()))
            print("Seed auto-Generated:", seed_input)
        else:
            print("Seed used:", seed_input)
        random.seed(seed_input)
        if self.height < 5:
            print(ValueError(
                "\033[0;31mError\033[0m"
                ": Height need to be >= 5 for the 42 logo"))
            exit(1)
        if self.width < 7:
            print(ValueError(
                "\033[0;31mError\033[0m"
                ": Width need to be >= 7 for the 42 logo"))
            exit(1)

        self._gen_perfect()
        if not self.perfect:
            self._gen_imperfect()

    def get_maze(self) -> list[list[int]]:
        return self.maze

    def get_path(self, entry: tuple[int, int], end: tuple[int, int]
                 ) -> str | None:
        return solver_heap(self.maze, entry, end)[0]

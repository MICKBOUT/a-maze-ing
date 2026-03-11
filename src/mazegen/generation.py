import random
import os


class MazeGenerator:

    def __init__(
      self, width: int, height: int, perfect: bool, seed_input: str = None
    ) -> None:
        self.width = width
        self.height = height
        self.perfect = perfect
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

        rnd_cell = (random.randint(
            0, height - 1), random.randint(0, width - 1))
        while rnd_cell in seen:
            rnd_cell = (random.randint(
                0, height - 1), random.randint(0, width - 1))
        stack = [rnd_cell]

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

    def generator(self, seed_input) -> list[list[int]]:
        if seed_input is None or seed_input.lower() in {"none", ""}:
            try:
                seed_input = int.from_bytes(os.urandom(4), "big")
            except NotImplementedError:
                seed_input = int(time.time())
            print("Seed auto-Generated:", seed_input)
        else:
            print("Seed used:", seed_input)
        random.seed(str(seed_input))
        if self.height < 6:
            print(ValueError("\033[0;31mError\033[0m: Height need to be >= 6 \
                             for the 42 logo"))
            exit(1)
        if self.width < 9:
            print(ValueError("\033[0;31mError\033[0m: Width need to be >= 9 \
                             for the 42 logo"))
            exit(1)

        self._gen_perfect()
        if not self.perfect:
            self._gen_imperfect()
        return self.maze


if __name__ == "__main__":
    # 5.1
    import time
    t = time.time()
    for i in range(50):
        MazeGenerator(
            width=200, height=200, seed_input=None, perfect=False).maze
    print(f"{round(time.time() - t, 3)}s")

# Bit Direction|
# -------------|
# 0 North      |
# 1 East       |
# 2 South      |
# 3 West       |

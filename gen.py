from random import randint, choice, seed
import os


class MazeGenerator:

    @classmethod
    def gen_perfect(self) -> list[list[int]]:
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

        rnd_cell = (randint(0, height - 1), randint(0, width - 1))
        while rnd_cell in seen:
            rnd_cell = (randint(0, height - 1), randint(0, width - 1))
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
                direction = choice(candidate)
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
        # north, est, south , west
        return self.maze

    @classmethod
    def gen_imperfect(cls):
        def rm_wall(row: int,
                    col: int,
                    direction: int,
                    ) -> None:
            match direction:
                # North
                case 0:
                    cls.maze[row][col] &= ~(1 << 0)
                    cls.maze[row - 1][col] &= ~(1 << 2)
                # East
                case 1:
                    cls.maze[row][col] &= ~(1 << 1)
                    cls.maze[row][col + 1] &= ~(1 << 3)
                # South
                case 2:
                    cls.maze[row][col] &= ~(1 << 2)
                    cls.maze[row + 1][col] &= ~(1 << 0)
                # West
                case 3:
                    cls.maze[row][col] &= ~(1 << 3)
                    cls.maze[row][col - 1] &= ~(1 << 1)

        width, height = len(cls.maze[0]), len(cls.maze)
        for _ in range((height * width) // 12):
            row = randint(0, height - 1)
            col = randint(0, width - 1)
            if cls.maze[row][col] == 15:
                continue

            candidate = []
            if row > 0 and cls.maze[row - 1][col] != 15:
                candidate.append(0)
            if col < width - 1 and cls.maze[row][col + 1] != 15:
                candidate.append(1)
            if row < height - 1 and cls.maze[row + 1][col] != 15:
                candidate.append(2)
            if col > 0 and cls.maze[row][col - 1] != 15:
                candidate.append(3)

            if candidate:
                rm_wall(row, col, choice(candidate))

    @classmethod
    def maze_generator(
         cls, width: int, height: int, seed_input: str, perfect: bool
         ) -> list[list[int]]:
        if seed_input is None or seed_input.lower() in {"none", ""}:
            try:
                seed_input = int.from_bytes(os.urandom(4), "big")
            except NotImplementedError:
                seed_input = int(time.time())
            print("Seed auto-Generated:", seed_input)
        else:
            print("Seed used:", seed_input)
        seed(seed_input)

        if height < 6:
            raise ValueError("height need to be >= 6 for the 42 logo")
        if width < 9:
            raise ValueError("width need to be >= 9 for the 42 logo")

        cls.width = width
        cls.height = height
        cls.gen_perfect()
        if not perfect:
            cls.gen_imperfect()
        return cls.maze


if __name__ == "__main__":
    # 5.1
    import time
    t = time.time()
    for i in range(50):
        MazeGenerator.maze_generator(
            width=200, height=200, seed_input=None, perfect=False)
    print(f"{round(time.time() - t, 3)}s")

    # print(grid)
    # print("\n=== maze ===")
    # for row in grid:
    #     print(row)

# Bit Direction|
# -------------|
# 0 North      |
# 1 East       |
# 2 South      |
# 3 West       |

from mlx import Mlx
from random import randint
from PIL import Image as Img
from pathlib import Path
from enum import Enum

buttons_size = (580, 1946)
button1_box = (2900, 400, 3420, 550)
button2_box = (2900, 660, 3420, 820)
button3_box = (2900, 930, 3420, 1090)
button4_box = (2900, 1190, 3420, 1340)


def create_colors():
    """
    Generate randomized RGBA colors for background and wall.

    Returns
    -------
    dict
        Dictionary containing two RGBA lists: "background" (bright color)
        and "wall" (darker variant).
    """
    colors = {
        "background": [
            randint(128, 255),
            randint(128, 255),
            randint(128, 255)
        ] + [255]
    }

    colors["wall"] = (
        [c - randint(0, 128) for c in colors["background"][:-1]] + [255]
    )

    return colors


class Colors(Enum):
    """A simple Enum class to represent colors."""
    BACKGROUND = "background"
    WALL = "wall"


class MLXImage:
    """Image wrapper providing basic drawing operations using MLX."""
    def __init__(self, mlx, mlx_ptr, width, height):
        """
        Initialize an MLX image buffer.

        Parameters
        ----------
        mlx : Mlx
            MLX wrapper instance.
        mlx_ptr : int
            MLX context pointer.
        width : int
            Image width in pixels.
        height : int
            Image height in pixels.
        """
        self.width, self.height = width, height
        self.img = mlx.mlx_new_image(mlx_ptr, self.width, self.height)
        data_img = mlx.mlx_get_data_addr(self.img)
        self.data_img, self.bpp, self.size_line, self.fmt = data_img

    def draw_rect(self, x1: int, y1: int,
                  x2: int, y2: int,
                  color: tuple[int, int, int, int]):
        """
        Draw a filled rectangle on the image.

        Parameters
        ----------
        x1, y1 : int
            Top-left corner.
        x2, y2 : int
            Bottom-right corner.
        color : Colors or tuple
            RGBA color or enum member.
        """

        if x2 <= x1 or y2 <= y1:
            return

        r, g, b, a = color
        bpp = self.bpp // 8

        pixel = bytes([b, g, r, a]) if bpp == 4 else bytes([b, g, r])
        line = pixel * (x2 - x1)

        for y in range(y1, y2):
            offset = y * self.size_line + x1 * bpp
            self.data_img[offset:offset + len(line)] = line

    def fill(self, color: tuple[int, int, int, int]):
        """
        Fill the entire image with a given color.

        Parameters
        ----------
        color : tuple
            RGBA color.
        """

        self.draw_rect(0, 0, self.width, self.height, color)


class MazeData:
    """
    Store maze structure and metadata.
    """
    def __init__(self):
        self.parse()

    def parse(self):
        parsed = read_file("output_maze.txt")
        self.maze = parsed["maze_data"]
        self.height = len(self.maze)
        self.width = len(self.maze[0])
        self.start = parsed["start"]
        self.end = parsed["end"]
        self.path = parsed["path"]


class MazeImage(MLXImage):
    def __init__(self, mlx, mlx_ptr, width, height, data):
        super().__init__(mlx, mlx_ptr, width, height)
        # Logical
        self.data = data
        self.drawn_path = False
        self.drawn_path = False

        # Visual
        self.cell_size = min(int(self.width // self.data.width),
                             int(self.height // self.data.height))
        self.width_wall = max(1, self.cell_size // 10)

        maze_width_px = self.data.width * self.cell_size
        maze_height_px = self.data.height * self.cell_size
        self.offset_x = (self.width - maze_width_px) // 2
        self.offset_y = (self.height - maze_height_px) // 2

        self.colors = create_colors()
        self.background_color = self.colors["background"]
        self.wall_color = self.colors["wall"]

    def draw_rect(self, x1: int, y1: int,
                  x2: int, y2: int,
                  color: Colors | tuple[int, int, int, int]):
        if color == Colors.BACKGROUND:
            color = self.background_color
        elif color == Colors.WALL:
            color = self.wall_color
        return super().draw_rect(x1, y1, x2, y2, color)

    def fill(self, color: Colors | tuple[int, int, int, int]):
        """
        Fill the entire image with a given color.

        Parameters
        ----------
        color : Colors or tuple
            RGBA color or enum member.
        """

        if color == Colors.BACKGROUND:
            color = self.background_color
        elif color == Colors.WALL:
            color = self.wall_color
        return super().fill(color)

    def draw_cell(self, value, y, x, background_color=None):
        px = x * self.cell_size + self.offset_x
        py = y * self.cell_size + self.offset_y

        x1, y1 = px, py
        x2, y2 = px + self.cell_size, py + self.cell_size

        if background_color is not None:
            self.draw_rect(
                x1, y1,
                x2, y2,
                background_color
            )
        if value & 1:
            self.draw_rect(
                x1, y1,
                x2, y1 + self.width_wall,
                self.wall_color
            )

        # Est
        if value & 2:
            self.draw_rect(
                x2 - self.width_wall, y1,
                x2, y2,
                self.wall_color
            )

        # Sud
        if value & 4:
            self.draw_rect(
                x1, y2 - self.width_wall,
                x2, y2,
                self.wall_color
            )

        # # Ouest
        if value & 8:
            self.draw_rect(
                x1, y1,
                x1 + self.width_wall, y2,
                self.wall_color
            )

        if value == 15:
            self.draw_rect(
                x1 + self.width_wall, y1 + self.width_wall,
                x2 - self.width_wall, y2 - self.width_wall,
                self.wall_color
            )

    def draw_maze(self):
        # Background Maze

        self.fill(Colors.WALL)

        for y in range(self.data.height):
            for x in range(self.data.width):
                self.draw_cell(self.data.maze[y][x], y, x,
                               background_color=self.background_color)

        x_start, y_start = self.data.start
        x_end, y_end = self.data.end

        self.draw_cell(
            self.data.maze[y_start][x_start],
            y_start,
            x_start,
            background_color=(0, 255, 0, 255),
        )

        # end
        self.draw_cell(
            self.data.maze[y_end][x_end],
            y_end,
            x_end,
            background_color=(255, 0, 0, 255),
        )

    def draw_path(self, color=None):
        current_x, current_y = self.data.start
        if color == Colors.BACKGROUND:
            color = self.background_color
        else:
            color = (255, 255, 255, 255)
        for i in range(len(self.data.path[:-1])):
            if self.data.path[i] == "S":
                current_y += 1
            elif self.data.path[i] == "N":
                current_y -= 1
            elif self.data.path[i] == "E":
                current_x += 1
            else:
                current_x -= 1
            self.draw_cell(
                self.data.maze[current_y][current_x],
                current_y, current_x,
                color
            )

    def update_colors(self):
        """
        Regenerate and update background and wall colors.
        """
        self.colors.update(create_colors())
        self.background_color = self.colors["background"]
        self.wall_color = self.colors["wall"]

    @staticmethod
    def get_faded_path(current: int, end: int):
        start_color, end_color = (255, 0, 0), (255, 255, 0)
        start_r, start_g, start_b = start_color
        end_r, end_g, end_b = end_color

        diff_r = end_r - start_r
        diff_b = end_b - start_b
        diff_g = end_g - start_g

        coef = current/end

        return (
            int(start_r + coef * diff_r,),
            int(start_g + coef * diff_g,),
            int(start_b + coef * diff_b,),
            255
        )


class MLXRenderer:
    def __init__(self, heap: list[tuple[int, int]]) -> None:
        """
        Initialise and loop the main window.
        """
        # attributes
        self.data = MazeData()
        self.heap = heap
        # Mlx instance
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.max_monitor_size = self.mlx.mlx_get_screen_size(self.mlx_ptr)[1:]
        self.windows_width = int(self.max_monitor_size[0]*0.9)
        self.windows_height = int(self.max_monitor_size[1]*0.9)
        # New Windows
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.windows_width,
            self.windows_height,
            "Amazing !"
        )

        # Maze Image
        self.maze_img = MazeImage(
            self.mlx,
            self.mlx_ptr,
            int(self.windows_width * 5/6),
            self.windows_height,
            self.data
        )
        self.maze_img.draw_maze()
        self.put_image(self.maze_img, 0, 0)

        path = self.compute_buttons()
        self.button_ptr, w, h = self.mlx.mlx_png_file_to_image(
            self.mlx_ptr, path)
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.button_ptr,
            self.maze_img.width, 0
        )
        # Buttons

        # Hooks
        def on_keypress(keycode, param):
            if keycode == 65307:
                self.mlx.mlx_destroy_image(self.mlx_ptr, self.maze_img.img)
                self.mlx.mlx_destroy_image(self.mlx_ptr, self.button_ptr)
                self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
                self.mlx.mlx_release(self.mlx_ptr)
                self.mlx.mlx_loop_exit(self.mlx_ptr)

        def on_mouse(button, x, y, param):
            # Change Color Button
            if button != 1:
                return

            if (
                self.button_new_color[0] <= x <= self.button_new_color[2]
                and self.button_new_color[1] <= y <= self.button_new_color[3]
            ):

                self.maze_img.update_colors()
                self.maze_img.draw_maze()
                if self.maze_img.drawn_path:
                    self.show_heap(float("inf"))
                if self.maze_img.drawn_path:
                    self.maze_img.draw_path()
                self.put_image(self.maze_img, 0, 0)

            # New maze button
            if (
                self.button_new_maze[0] <= x <= self.button_new_maze[2]
                and self.button_new_maze[1] <= y <= self.button_new_maze[3]
            ):
                from .utils import new_maze
                self.heap = new_maze(new_seed=True)
                self.data.parse()
                self.maze_img.draw_maze()
                self.put_image(self.maze_img, 0, 0)
                self.maze_img.drawn_path = False
                self.maze_img.drawn_path = False

            # Show path Button
            if (
                self.button_show_path[0] <= x <= self.button_show_path[2]
                and self.button_show_path[1] <= y <= self.button_show_path[3]
            ):
                if self.maze_img.drawn_path:
                    self.maze_img.drawn_path = False
                    self.maze_img.draw_path(Colors.BACKGROUND)
                    self.put_image(self.maze_img, 0, 0)
                else:
                    self.maze_img.drawn_path = True
                    self.maze_img.draw_path()
                    self.put_image(self.maze_img, 0, 0)

                if not self.maze_img.drawn_path and self.maze_img.drawn_path:
                    self.show_heap(float("inf"))

            # Draw heap
            if (
                self.button_show_heap[0] <= x <= self.button_show_heap[2]
                and self.button_show_heap[1] <= y <= self.button_show_heap[3]
            ):
                if not self.maze_img.drawn_path:
                    self.maze_img.drawn_path = True
                    self.show_heap(max(1, len(self.heap)//100))
                else:
                    self.maze_img.drawn_path = False
                    self.show_heap(float("inf"), erase=True)
                    if self.maze_img.drawn_path:
                        self.maze_img.draw_path
                    self.put_image(self.maze_img, 0, 0)

        self.mlx.mlx_hook(self.win_ptr, 2, 1, on_keypress, None)
        self.mlx.mlx_mouse_hook(self.win_ptr, on_mouse, None)

    def show_heap(self, sample, erase=False):
        i, heap = 0, self.heap[:-1]
        while i < len(heap):
            j = 0
            while j < sample and i < len(heap):
                x, y = heap[i]
                i, j = i + 1, j + 1
                value = self.data.maze[y][x]
                if erase:
                    color = self.maze_img.background_color
                else:
                    color = MazeImage.get_faded_path(i, len(heap))
                self.maze_img.draw_cell(value, y, x, color)

            self.put_image(self.maze_img, 0, 0)
            if not erase:
                self.mlx.mlx_do_sync(self.mlx_ptr)

    def put_image(self, img, x, y):
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            img.img,
            x, y
        )

    def compute_buttons(self):
        def scale_box(box, screen_w, screen_h):
            return (
                int(box[0] * screen_w / 3840),
                int(box[1] * screen_h / 2160),
                int(box[2] * screen_w / 3840),
                int(box[3] * screen_h / 2160),
            )

        self.button_new_color = scale_box(
            button1_box, self.max_monitor_size[0], self.max_monitor_size[1])
        self.button_new_maze = scale_box(
            button2_box, self.max_monitor_size[0], self.max_monitor_size[1])
        self.button_show_path = scale_box(
            button3_box, self.max_monitor_size[0], self.max_monitor_size[1])
        self.button_show_heap = scale_box(
            button4_box, self.max_monitor_size[0], self.max_monitor_size[1])

        if self.max_monitor_size == (3840, 2160):
            return "assets/buttons_copy.png"
        else:
            new_image_size = (
                int((buttons_size[0] * self.max_monitor_size[0])/3840),
                int((buttons_size[1] * self.max_monitor_size[1])/2160)
            )

            rescale_image("assets/buttons_copy.png", new_image_size)
            return "assets/rescaled/buttons.png"


def rescale_image(filename: str, new_size: tuple):
    input_path = Path(filename)
    output_dir = Path("assets/rescaled")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "buttons.png"

    img = Img.open(input_path)
    resized = img.resize(new_size, Img.Resampling.LANCZOS)
    resized.save(output_path)

    return resized, str(output_path)


def read_file(file_name: str = "output_maze.txt"):
    with open(file_name, 'r') as file:
        data = [line.strip() for line in file]

    return {
        "maze_data": [[int(c, 16) for c in line] for line in data[:-4]],
        "start": tuple([int(n) for n in data[-3].split(sep=",")]),
        "end": tuple([int(n) for n in data[-2].split(sep=",")]),
        "path": data[-1]
    }

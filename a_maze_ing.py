from mlx import Mlx
import sys
from random import randint
from PIL import Image as Img
from pathlib import Path

FILENAME = "maze_output.txt"
TITLE = "Amazing !"
ANIMATION = False

buttons_size = (580, 1946)
button1_box = (2900, 400, 3420, 550)
button2_box = (2900, 660, 3420, 820)
button3_box = (2900, 930, 3420, 1090)
button4_box = (2900, 1190, 3420, 1250)


def create_colors():
    """Create colors using random"""
    # Dict of complementary colors randomly generated
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
    red, green, blue, _ = colors["background"]
    # Apply the best color to contrast tehe text with the background.

    return colors

from enum import Enum
class Colors(Enum):
    BACKGROUND = "background"
    WALL = "wall"

class Image:
    def __init__(self, mlx, mlx_ptr, width, height):
        self.width, self.height = width, height
        self.img = mlx.mlx_new_image(mlx_ptr, self.width, self.height)
        data_img = mlx.mlx_get_data_addr(self.img)
        self.data, self.bpp, self.size_line, self.fmt = data_img
        

    def draw_rect(self, x1: int, y1: int, x2: int, y2: int, color: Colors | tuple[int, int, int, int]):
        if x2 <= x1 or y2 <= y1:
            return

        if color == Colors.BACKGROUND:
            color = self.background_color
        elif color == Colors.WALL:
            color = self.wall_color

        r, g, b, a = color
        bpp = self.bpp // 8

        pixel = bytes([b, g, r, a]) if bpp == 4 else bytes([b, g, r])
        line = pixel * (x2 - x1)

        for y in range(y1, y2):
            offset = y * self.size_line + x1 * bpp
            self.data[offset:offset + len(line)] = line

    def clear(self):
        self.draw_rect(0, 0, self.width, self.height, (0, 0, 0, 255))

    def fill(self, color: Colors | tuple[int, int, int, int]):
        if color == Colors.BACKGROUND:
            self.draw_rect(0, 0, self.width, self.height, self.background_color)
        elif color == Colors.WALL:
            self.draw_rect(0, 0, self.width, self.height, self.wall_color)
        else:
            self.draw_rect(0, 0, self.width, self.height, color)

    def update_colors(self):
        self.colors.update(create_colors())
        self.background_color = self.colors["background"]
        self.wall_color = self.colors["wall"]


class MazeImage(Image):
    def __init__(self, mlx, mlx_ptr, width, height):
        super().__init__(mlx, mlx_ptr, width, height)
        # Logical
        self.fetch_data()
        self.drawed_path = False
        self.drawed_heap = False

        # Visual
        self.cell_size = min(int(self.width // self.maze_width),
                             int(self.height // self.maze_height))
        self.width_wall = max(1, self.cell_size // 10)

        maze_width_px = self.maze_width * self.cell_size
        maze_height_px = self.maze_height * self.cell_size
        self.offset_x = (self.width - maze_width_px) // 2
        self.offset_y = (self.height - maze_height_px) // 2

        self.colors = create_colors()
        self.background_color = self.colors["background"]
        self.wall_color = self.colors["wall"]
        self.path_color_start = tuple(255 - i for i in self.background_color[:-1])
        self.path_color_end = tuple(255 - i for i in self.wall_color[:-1])

    def fetch_data(self):
        parsed_data = read_file()
        self.maze = parsed_data["maze_data"]
        self.maze_height = len(self.maze)
        self.maze_width = len(self.maze[0])
        self.maze_size = (self.maze_width, self.maze_height)

        self.start = parsed_data["start"]
        self.end = parsed_data["end"]
        self.path = parsed_data["path"]

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

        for y in range(self.maze_height):
            for x in range(self.maze_width):
                self.draw_cell(self.maze[y][x], y, x,
                               background_color=self.background_color)

            x_start, y_start = self.start
            x_end, y_end = self.end

            # start
            # start
        self.draw_cell(
            self.maze[y_start][x_start],
            y_start,
            x_start,
            background_color=(0, 255, 0, 255),
        )

        # end
        self.draw_cell(
            self.maze[y_end][x_end],
            y_end,
            x_end,
            background_color=(255, 0, 0, 255),
        )
        if self.drawed_path:
            self.draw_path()

    def get_faded_path(self, current: int, end: int):
        start_color, end_color = self.path_color_start, self.path_color_end
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
            255  # alpha
        )

    def draw_path(self, color=None):
        current_x, current_y = self.start
        if color == Colors.BACKGROUND:
            color = self.background_color
        else:
            color = (255, 255, 255, 255)
        for i in range(len(self.path[:-1])):
            if self.path[i] == "S":
                current_y += 1
            elif self.path[i] == "N":
                current_y -= 1
            elif self.path[i] == "E":
                current_x += 1
            else:
                current_x -= 1
            self.draw_cell(
                self.maze[current_y][current_x],
                current_y, current_x,
                color
            )


class MLXRendering:
    def __init__(self, heap: list[tuple[int, int]]) -> None:
        """
        Initialise and loop the main window.
        """
        # attributes
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
            TITLE
        )
        
        # Maze Image
        self.maze_img = MazeImage(
            self.mlx,
            self.mlx_ptr,
            int(self.windows_width * 5/6),
            self.windows_height,
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

                sys.exit(0)

        def on_mouse(button, x, y, param):
            # Change Color Button
            if (
                self.button_new_color[0] <= x <= button1_box[2]
                and self.button_new_color[1] <= y <= button1_box[3]
            ):
                self.maze_img.update_colors()
                self.maze_img.draw_maze()
                if self.maze_img.drawed_heap:
                    self.show_heap(float("inf"))
                self.put_image(self.maze_img, 0, 0)

            # New maze button
            if (
                self.button_new_maze[0] <= x <= button2_box[2]
                and self.button_new_maze[1] <= y <= button2_box[3]
            ):
                print("testtttt")
                from main import new_maze
                self.heap = new_maze(new_seed=True)
                self.maze_img.fetch_data()
                self.maze_img.draw_maze()
                self.put_image(self.maze_img, 0, 0)

            # Show path Button
            if (
                self.button_show_path[0] <= x <= button3_box[2]
                and self.button_show_path[1] <= y <= button3_box[3]
            ):
                if self.maze_img.drawed_path:
                    self.maze_img.drawed_path = False
                    self.maze_img.draw_path(Colors.BACKGROUND)
                    self.put_image(self.maze_img, 0, 0)
                else:
                    self.maze_img.drawed_path = True
                    self.maze_img.draw_path()
                    self.put_image(self.maze_img, 0, 0)
                
                if not self.maze_img.drawed_path and self.maze_img.drawed_heap:
                    self.show_heap(float("inf"))
            
            if (
                self.button_show_path_animated[0] <= x <= button4_box[2]
                and self.button_show_path_animated[1] <= y <= button4_box[3]
            ):
                if not self.maze_img.drawed_heap:
                    self.maze_img.drawed_heap = True
                    self.show_heap(len(self.heap)//100)
                else:
                    self.maze_img.drawed_heap = False
                    self.show_heap(float("inf"), erase=True)
                    if self.maze_img.drawed_path:
                        self.maze_img.draw_path
                    self.put_image(self.maze_img, 0, 0)

        self.mlx.mlx_hook(self.win_ptr, 2, 1, on_keypress, None)
        self.mlx.mlx_mouse_hook(self.win_ptr, on_mouse, None)

    def show_heap(self, sample, erase=False):
        i = 0
        while i < len(self.heap):
            j = 0
            while j < sample and i < len(self.heap):
                x, y = self.heap[i]
                i, j = i + 1, j + 1
                value = self.maze_img.maze[y][x]
                if erase:
                    color = self.maze_img.background_color
                else:
                    color = self.maze_img.get_faded_path(i, len(self.heap))
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
        if self.max_monitor_size == (3840, 2160):
            self.button_new_color = button1_box
            self.button_new_maze = button2_box
            self.button_show_path = button3_box
            self.button_show_path_animated = button4_box
            return "assets/buttons_copy.png"
        else:
            new_image_size = (
                int((buttons_size[0] * self.max_monitor_size[0])/3840),
                int((buttons_size[1] * self.max_monitor_size[1])/2160)
            )

            self.button_new_color = (
                int((button1_box[0] * self.max_monitor_size[0])/3840),
                int((button1_box[1] * self.max_monitor_size[1])/2160),
            )

            self.button_new_maze = (
                int((button2_box[0] * self.max_monitor_size[0])/3840),
                int((button2_box[1] * self.max_monitor_size[1])/2160),
            )

            self.button_show_path = (
                int((button3_box[0] * self.max_monitor_size[0])/3840),
                int((button3_box[1] * self.max_monitor_size[1])/2160),
            )

            self.button_show_path_animated = (
                int((button4_box[0] * self.max_monitor_size[0])/3840),
                int((button4_box[1] * self.max_monitor_size[1])/2160),
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


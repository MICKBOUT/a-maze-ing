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
    if (red * 0.299 + green*0.587 + blue*0.114) > 186:
        colors["text"] = (0, 0, 0, 255)
    else:
        colors["text"] = (255, 255, 255, 255)

    return colors


COLORS = create_colors()


class Image:
    def __init__(self, mlx, mlx_ptr, width, height):
        self.width, self.height = width, height
        self.img = mlx.mlx_new_image(mlx_ptr, self.width, self.height)
        data_img = mlx.mlx_get_data_addr(self.img)
        self.data, self.bpp, self.size_line, self.fmt = data_img

    def draw_rect(self, x1, y1, x2, y2, color):
        if x2 <= x1 or y2 <= y1:
            return  # rien à dessiner

        r, g, b, a = color
        bpp = self.bpp // 8

        pixel = bytes([b, g, r, a]) if bpp == 4 else bytes([b, g, r])
        line = pixel * (x2 - x1)

        for y in range(y1, y2):
            offset = y * self.size_line + x1 * bpp
            self.data[offset:offset + len(line)] = line

    def clear(self):
        self.draw_rect(0, 0, self.width, self.height, (0, 0, 0, 255))

    def fill(self, color):
        self.draw_rect(0, 0, self.width, self.height, color)


class MazeImage(Image):
    def __init__(self, mlx, mlx_ptr,
                 width, height, maze_width,
                 maze_height, maze, start, end, path):
        super().__init__(mlx, mlx_ptr, width, height)
        # Logical
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze = maze
        self.start = start
        self.end = end
        self.background_color = COLORS["background"]
        self.wall_color = COLORS["wall"]
        self.path = path
        self.drawed_path = False

        # Visual
        self.cell_size = min(int(self.width // maze_width),
                             int(self.height // maze_height))
        self.width_wall = max(1, self.cell_size // 10)

        maze_width_px = self.maze_width * self.cell_size
        maze_height_px = self.maze_height * self.cell_size
        self.offset_x = (self.width - maze_width_px) // 2
        self.offset_y = (self.height - maze_height_px) // 2

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
        self.fill(self.wall_color)

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
        print(self.drawed_path)
        if self.drawed_path:
            self.draw_path()

    def draw_path(self):
        if self.drawed_path:
            color_path = (255, 255, 255, 255)
        else:
            color_path = self.background_color
        current_x, current_y = self.start
        for c in self.path[:-1]:
            if c == "S":
                current_y += 1
            elif c == "N":
                current_y -= 1
            elif c == "E":
                current_x += 1
            else:
                current_x -= 1
            self.draw_cell(
                self.maze[current_y][current_x],
                current_y, current_x,
                background_color=color_path
            )


class MLXRendering:
    def __init__(self) -> None:
        """
        Initialise and loop the main window.
        """
        # attributes
        self.fetch_data()

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
        self.cell_size = max(1, min(
            int(self.windows_width * 5/6) // self.maze_width,
            self.windows_height // self.maze_height
        ))

        # Maze Image
        self.maze_img = MazeImage(
            self.mlx,
            self.mlx_ptr,
            int(self.windows_width * 5/6),
            self.windows_height,
            self.maze_width,
            self.maze_height,
            self.maze,
            self.start,
            self.end,
            self.path
        )
        self.maze_img.draw_rect(0, 0, self.maze_img.width,
                                self.maze_img.height, (255, 255, 255, 255))
        self.put_image(self.maze_img, 0, 0)

        print()

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
                self.button_new_color[0] <= x <=
                self.button_new_color[0] + button1_box[2] - button1_box[0]
                and self.button_new_color[1] <= y <=
                self.button_new_color[1] + button1_box[3] - button1_box[1]
            ):
                COLORS.update(create_colors())
                self.maze_img.wall_color = COLORS["wall"]
                self.maze_img.background_color = COLORS["background"]
                self.maze_img.draw_maze()
                self.put_image(self.maze_img, 0, 0)

            # Show path Button

            if (
                self.button_show_path[0] <= x <=
                self.button_show_path[0] + button3_box[2] - button3_box[0]
                and self.button_show_path[1] <= y <=
                self.button_show_path[1] + button3_box[3] - button3_box[1]
            ):
                self.maze_img.drawed_path = not self.maze_img.drawed_path
                self.maze_img.draw_path()
                self.put_image(self.maze_img, 0, 0)

        self.mlx.mlx_hook(self.win_ptr, 2, 1, on_keypress, None)
        self.mlx.mlx_mouse_hook(self.win_ptr, on_mouse, None)

    def fetch_data(self):
        parsed_data = read_file()
        self.maze = parsed_data["maze_data"]
        self.maze_height = len(self.maze)
        self.maze_width = len(self.maze[0])
        self.maze_size = (self.maze_width, self.maze_height)

        self.start = parsed_data["start"]
        self.end = parsed_data["end"]
        self.path = parsed_data["path"]

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


if __name__ == "__main__":
    render = MLXRendering()
    render.maze_img.draw_maze()
    render.put_image(render.maze_img, 0, 0)
    render.mlx.mlx_loop(render.mlx_ptr)

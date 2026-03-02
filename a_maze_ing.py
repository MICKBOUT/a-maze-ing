from mlx import Mlx
import sys
from random import choice, randint
from time import sleep


class Image:
    def __init__(self, mlx, mlx_ptr, size: tuple):
        self.width, self.height = size
        self.img = mlx.mlx_new_image(mlx_ptr, self.width, self.height)
        self.data, self.bpp, self.size_line, self.fmt = mlx.mlx_get_data_addr(self.img)

    def draw_rect(self, pos1, pos2, color):
        r, g, b, a = color
        bpp = self.bpp // 8
        width = pos2[0] - pos1[0]

        # ligne complète en bytes
        if bpp == 4:
            pixel = bytes([b, g, r, a])
        else:
            pixel = bytes([b, g, r])

        line = pixel * width

        for y in range(pos1[1], pos2[1]):
            offset = y * self.size_line + pos1[0] * bpp
            self.data[offset:offset + len(line)] = line

    def clear(self):
        self.draw_rect((0, 0), (self.width, self.height), (0, 0, 0, 255))


class MLXRendering:
    def __init__(self, window_size): # dev
        # Mlx instance
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        # The main window
        self.window_size: tuple = window_size
        self.win_ptr = self.mlx.mlx_new_window(self.mlx_ptr, *self.window_size, "Maze")
        # The image where the maze is draw
        self.maze_img = Image(self.mlx, self.mlx_ptr, self.window_size)
        self.maze_img_ptr = self.maze_img.img

        # parsing, init self.{start, end, size, path}
        self.fetch_data()

        # === Cells proprieties ===
        # the size of each cell is the bigger size possible, depending of the windows
        self.cell_size = min(
            self.window_size[0] // self.maze_size[0],
            self.window_size[1] // self.maze_size[1]
        )
        self.width_wall = max(1, self.cell_size // 10)

        colors = MLXRendering.create_colors()
        self.wall_color: tuple = colors["wall"]
        self.background_color = colors["background"]
        self.font_color = colors["text"]

        self.draw_maze()
        self.put_image(self.maze_img)

        def on_keypress(keycode, param):
            if keycode == 65307:
                self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
                self.mlx.mlx_loop_exit(self.mlx_ptr)
                sys.exit(0)
            
            elif keycode == 65361:
                self.draw_path()
                # draw start
                # draw end
        
        self.mlx.mlx_hook(self.win_ptr, 2, 1, on_keypress, None)

    def fetch_data(self):
        parsed_data = read_file()
        self.maze = parsed_data["maze_data"]
        self.maze_size = (len(self.maze[0]), len(self.maze))
        self.start = parsed_data["start"]
        self.end = parsed_data["end"]
        self.path = parsed_data["path"]

        print("Maze size:", self.maze_size) 
        print("Start:", self.start) 
        print("End:", self.end)

    def draw_maze(self):
        maze_size = tuple(s * self.cell_size for s in self.maze_size)
        self.maze_img.draw_rect((0, 0), maze_size, self.background_color)
        self.maze_img.draw_rect((maze_size[0], 0), self.window_size, self.wall_color)
        for col in range(self.maze_size[0]):
            for row in range(self.maze_size[1]):
                self.draw_cell(self.maze_img, self.maze[row][col], row, col)

        x_start, y_start = self.start
        x_end, y_end = self.end

        self.draw_cell(self.maze_img, self.maze[y_start][x_start], y_start, x_start, background_color=(0, 255, 0, 255))
        self.draw_cell(self.maze_img, self.maze[y_end][x_end], y_end, x_end, background_color=(255, 0, 0, 255))
        
        

    def draw_cell(self, img, value, row, col, background_color=None):
        x = col * self.cell_size
        y = row * self.cell_size

        x1, y1 = x, y
        x2, y2 = x + self.cell_size, y + self.cell_size

        # Nord
        if background_color is not None:
            self.maze_img.draw_rect(
                (x1, y1),
                (x2, y2),
                background_color
            )
        if value & 1:
            self.maze_img.draw_rect(
                (x1, y1),
                (x2, y1 + self.width_wall),
                self.wall_color
            )

        # Est
        if value & 2:
            self.maze_img.draw_rect(
                (x2 - self.width_wall, y1),
                (x2, y2),
                self.wall_color
            )

        # Sud
        if value & 4:
            self.maze_img.draw_rect(
                (x1, y2 - self.width_wall),
                (x2, y2),
                self.wall_color
                
            )

        # # Ouest
        if value & 8:
            self.maze_img.draw_rect(
                (x1, y1),
                (x1 + self.width_wall, y2),
                self.wall_color
            )

        if value == 15:
            self.maze_img.draw_rect(
                (x1 + self.width_wall, y1 + self.width_wall),
                (x2 - self.width_wall, y2 - self.width_wall),
                self.wall_color
            )

    @staticmethod
    def create_colors():
        """Create colors using random"""
        colors = {
            "background": [randint(128, 255), randint(128, 255), randint(128, 255)] + [255]
        }
        colors["wall"] = ([c - randint(0, 128) for c in colors["background"][:-1]] + [255])
        red, green, blue, _ = colors["background"]
        if (red *0.299 + green*0.587 + blue*0.114) > 186:
            colors["text"] = (0, 0, 0, 255)
        else:
            colors["text"] = (255, 255, 255, 255)

        return colors
    
    def draw_path(self):
        current_x, current_y = self.start # The position in the maze (col, row)
        for c in self.path[:-1]:
            if c == "S":
                current_y += 1
            elif c == "N":
                current_y -= 1
            elif c == "E":
                current_x += 1
            else:
                current_x -= 1
            self.draw_cell(self.maze_img, self.maze[current_y][current_x], current_y, current_x, background_color=(255, 255, 255, 255))
        self.put_image(self.maze_img)
                

    def put_image(self, img):
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr, img.img, 0, 0)
    
    def main_loop(self):
        self.mlx.mlx_loop(self.mlx_ptr)

    def put_string(self, pos: tuple, color: tuple, string):
        r, g, b, _ = self.font_color
        color = (r << 16) | (g << 8) | b
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr, *pos, color, string)


def read_file(file_name: str="output_maze.txt"):
    with open(file_name, 'r') as file:
        data = [line.strip() for line in file]

    return {
        "maze_data": [[int(c, 16) for c in line ] for line in data[:-4]],
        "start": tuple([int(n) for n in data[-3].split(sep=",")]),
        "end": tuple([int(n) for n in data[-2].split(sep=",")]),
        "path": data[-1]
    }



if __name__ == "__main__":
    render = MLXRendering((1500, 1500))
    render.put_string((1000, 0), (255, 255, 255, 255), "Test123 456 Maze\nhi poqwpow")
    render.main_loop()
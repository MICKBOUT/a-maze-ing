from mlx_maze.mlx_utils import create_colors, Colors
from mlx_maze.mlx_utils import MazeData

import mlx

from typing import Callable


class MLXImage:
    """Image wrapper providing basic drawing operations using MLX."""

    def __init__(self, mlx: mlx.Mlx, mlx_ptr: int,
                 width: int, height: int) -> None:
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

    def draw_rect(self,
                  x1: int, y1: int,
                  x2: int, y2: int,
                  color: list[int]) -> None:
        """
        Draw a filled rectangle on the image.

        Parameters
        ----------
        x1, y1 : int
            Top-left corner.
        x2, y2 : int
            Bottom-right corner.
        color : list RGBA color
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

    def fill(self, color: list[int]) -> None:
        """
        Fill the entire image with a given color.

        Parameters
        ----------
        color : list
            RGBA color.
        """

        self.draw_rect(0, 0, self.width, self.height, color)


class MazeImage(MLXImage):
    def __init__(self, mlx: mlx.Mlx, mlx_ptr: int,
                 width: int, height: int,
                 data: MazeData) -> None:
        """
        Initialize a maze-rendering image.

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
        data : MazeData
            Parsed maze structure and metadata.
        """
        super().__init__(mlx, mlx_ptr, width, height)
        # Logical
        self.data = data
        self.drawn_path = False
        self.drawn_heap = False

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

    def draw_rect(self,
                  x1: int, y1: int,
                  x2: int, y2: int,
                  color: Colors | list[int]) -> None:
        """
        Draw a rectangle using maze-aware colors.

        Parameters
        ----------
        x1, y1 : int
            Top-left corner.
        x2, y2 : int
            Bottom-right corner.
        color : Colors or list
            Enum member or RGBA list.
        """

        if color == Colors.BACKGROUND:
            color = self.background_color
        elif color == Colors.WALL:
            color = self.wall_color
        return super().draw_rect(x1, y1, x2, y2, color)

    def fill(self, color: Colors | list[int]) -> None:
        """
        Fill the entire image with a given color.

        Parameters
        ----------
        color : Colors or list
            RGBA color or enum member.
        """

        if color == Colors.BACKGROUND:
            color = self.background_color
        elif color == Colors.WALL:
            color = self.wall_color
        return super().fill(color)

    def draw_cell(self, value: int, y: int, x: int,
                  background_color: list[int]
                  | None = None) -> None:
        """
        Draw a single maze cell with its walls.

        Parameters
        ----------
        value : int
            Bitmask representing the cell's walls.
        y, x : int
            Cell coordinates in the maze grid.
        background_color : list or None
            Optional RGBA fill for the cell interior.
        """
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

        # Ouest
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

    def draw_maze(self) -> None:
        """
        Render the full maze grid, including start and end cells.
        """

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
            background_color=[0, 255, 0, 255],
        )

        # end
        self.draw_cell(
            self.data.maze[y_end][x_end],
            y_end,
            x_end,
            background_color=[255, 0, 0, 255],
        )

    def draw_path(self, color: Colors | None = None) -> None:
        """
        Draw the solution path over the maze.

        Parameters
        ----------
        color : Colors or tuple, optional
            Path color. Defaults to white unless BACKGROUND is specified.
            in the case where background is specified,
            if the background is in Colors: background color will be used.

        """
        current_x, current_y = self.data.start
        if color == Colors.BACKGROUND:
            color_used = self.background_color
        else:
            color_used = [255, 255, 255, 255]
        for d in self.data.path[:-1]:
            if d == "S":
                current_y += 1
            elif d == "N":
                current_y -= 1
            elif d == "E":
                current_x += 1
            else:
                current_x -= 1
            self.draw_cell(
                self.data.maze[current_y][current_x],
                current_y, current_x,
                color_used
            )

    def show_heap(self, sample: int,
                  put_img: Callable[[], None],
                  do_sync: Callable[[], None] | None = None,
                  erase: bool = False) -> None:
        """
        Animate the exploration heap by progressively coloring visited cells.

        Parameters
        ----------
        sample : int
            Number of heap elements to draw per frame.
        put_img : Callable[[], None]
            Callback used to display the updated image after each batch.
        do_sync : Callable[[], None], optional
            Optional callback to synchronize the display (e.g., mlx_loop_hook).
        erase : bool, optional
            If True, cells are redrawn using the maze background color.
            If False, cells are colored using a fading gradient computed
            by `get_faded_path`.
        """
        i, heap = 0, self.data.heap[:-1]
        while i < len(heap):
            j = 0
            while j < sample and i < len(heap):
                x, y = heap[i]
                i, j = i + 1, j + 1
                value = self.data.maze[y][x]
                if erase:
                    color = self.background_color
                else:
                    color = MazeImage.get_faded_path(i, len(heap))
                self.draw_cell(value, y, x, color)

            put_img()
            if do_sync is not None:
                do_sync()

    def update_colors(self) -> None:
        """
        Regenerate the entire color palette and update the maze's
        background and wall colors accordingly.

        Notes
        -----
        This refreshes *all* entries in the internal color dictionary,
        not only the background and wall colors.
        """
        self.colors.update(create_colors())
        self.background_color = self.colors["background"]
        self.wall_color = self.colors["wall"]

    @staticmethod
    def get_faded_path(current: int, end: int) -> list[int]:
        """
        Compute a fading RGBA color used for heap exploration animation.

        The color transitions linearly from yellow (start of heap)
        to pink (end of heap).

        Parameters
        ----------
        current : int
            Current index in the heap traversal.
        end : int
            Total number of heap elements.

        Returns
        -------
        list[int]
            A 4‑component RGBA color representing the interpolated value.
        """
        start_color, end_color = [255, 255, 0], [255, 0, 127]
        if end == 0:
            return start_color + [255]
        start_r, start_g, start_b = start_color
        end_r, end_g, end_b = end_color

        diff_r = end_r - start_r
        diff_b = end_b - start_b
        diff_g = end_g - start_g

        coef = current/end

        return [
            int(start_r + coef * diff_r,),
            int(start_g + coef * diff_g,),
            int(start_b + coef * diff_b,),
            255
        ]

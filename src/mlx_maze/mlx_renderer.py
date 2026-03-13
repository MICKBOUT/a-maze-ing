from typing import Any

import mlx

from mlx_maze.mlx_image import MazeImage, MLXImage
from mlx_maze.mlx_utils import button1_box, MazeData, buttons_size
from mlx_maze.mlx_utils import rescale_image, button2_box, button3_box
from mlx_maze.mlx_utils import button4_box, Colors
from utils import new_maze


class MLXRenderer:
    """
    Main controller for the MLX graphical window.

    This class initializes the MLX context, creates the window, manages
    the maze image, handles user interactions (mouse and keyboard), and
    updates the display accordingly.
    """

    def __init__(self, heap: list[tuple[int, int]], filename: str) -> None:
        """
        Initialize the MLX window and prepare all rendering components.

        Parameters
        ----------
        heap : list of tuple[int, int]
            Sequence of visited maze cells used for heap visualization.
        """
        self.data = MazeData(heap, filename)

        # INIT
        self.mlx = mlx.Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        # WINDOW
        val, w, h = self.mlx.mlx_get_screen_size(self.mlx_ptr)
        if val == 0:
            self.max_monitor_size = (w, h)
        else:
            self.max_monitor_size = (1920, 1080)

        self.windows_width = int(self.max_monitor_size[0]*0.9)
        self.windows_height = int(self.max_monitor_size[1]*0.9)

        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.windows_width,
            self.windows_height,
            "Amazing !"
        )

        # MAZE
        self.maze_img = MazeImage(
            self.mlx,
            self.mlx_ptr,
            int(self.windows_width * 5/6),
            self.windows_height,
            self.data
        )
        self.maze_img.draw_maze()
        self.put_image(self.maze_img, 0, 0)

        # BUTTONS
        path = self.compute_buttons()
        self.button_ptr, w, h = self.mlx.mlx_png_file_to_image(
            self.mlx_ptr, path)
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.button_ptr,
            self.maze_img.width, 0
        )

        # EVENTS
        def on_keypress(keycode: int, param: Any) -> None:
            if keycode == 65307:
                self.destroy()

        def on_mouse(button: int, x: int, y: int, param: Any) -> None:
            # New Color Button
            if button != 1:
                return

            def put_image() -> None: self.put_image(self.maze_img, 0, 0)
            def do_sync() -> None: self.mlx.mlx_do_sync(self.mlx_ptr)

            if (
                self.button_new_color[0] <= x <= self.button_new_color[2]
                and self.button_new_color[1] <= y <= self.button_new_color[3]
            ):
                self.maze_img.update_colors()
                self.maze_img.draw_maze()
                if self.maze_img.drawn_heap:
                    self.maze_img.show_heap(
                        len(self.data.heap),
                        put_image,
                    )
                if self.maze_img.drawn_path:
                    self.maze_img.draw_path()
                self.put_image(self.maze_img, 0, 0)

            # New Maze button
            if (
                self.button_new_maze[0] <= x <= self.button_new_maze[2]
                and self.button_new_maze[1] <= y <= self.button_new_maze[3]
            ):
                heap, filename = new_maze(new_seed=True)

                self.data.parse(heap, filename)
                self.maze_img.draw_maze()
                self.put_image(self.maze_img, 0, 0)

                self.maze_img.drawn_path = False
                self.maze_img.drawn_heap = False

            # Show Path Button
            if (
                self.button_show_path[0] <= x <= self.button_show_path[2]
                and self.button_show_path[1] <= y <= self.button_show_path[3]
            ):
                if self.maze_img.drawn_path:
                    self.maze_img.drawn_path = False
                    self.maze_img.draw_path(Colors.BACKGROUND)
                else:
                    self.maze_img.drawn_path = True
                    self.maze_img.draw_path()

                if not self.maze_img.drawn_path and self.maze_img.drawn_heap:
                    self.maze_img.show_heap(
                        len(self.data.heap),
                        put_image
                    )

                self.put_image(self.maze_img, 0, 0)

            # Draw Heap Button
            if (
                self.button_show_heap[0] <= x <= self.button_show_heap[2]
                and self.button_show_heap[1] <= y <= self.button_show_heap[3]
            ):
                if not self.maze_img.drawn_heap:
                    self.maze_img.drawn_heap = True
                    self.maze_img.show_heap(
                        max(1, len(self.data.heap)//100),
                        put_image,
                        do_sync
                    )
                    self.maze_img.drawn_path = False

                else:
                    self.maze_img.drawn_heap = False

                    self.maze_img.show_heap(
                        max(1, len(self.data.heap)),
                        put_image,
                        do_sync,
                        erase=True
                    )

                    if self.maze_img.drawn_path:
                        self.maze_img.draw_path()

                    self.put_image(self.maze_img, 0, 0)

        self.mlx.mlx_hook(self.win_ptr, 2, 1, on_keypress, None)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, lambda x: self.destroy(), None)
        self.mlx.mlx_mouse_hook(self.win_ptr, on_mouse, None)

    def put_image(self, img: MLXImage, x: int, y: int) -> None:
        """
        Draw an MLX image into the window.

        Parameters
        ----------
        img : MLXImage
            Image object to display.
        x, y : int
            Pixel coordinates where the image is placed.
        """
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            img.img,
            x, y
        )

    def compute_buttons(self) -> str:
        """
        Compute the scaled button hitboxes and return the appropriate
        button image.

        Returns
        -------
        str
            Path to the PNG file containing the button graphics.
        """

        def scale_box(box: tuple[int, int, int, int],
                      screen_w: int, screen_h: int
                      ) -> tuple[int, int, int, int]:
            """
            This function return the right box of the button
            depending on the size
            """
            return (
                int(box[0] * screen_w / 3840),
                int(box[1] * screen_h / 2160),
                int(box[2] * screen_w / 3840),
                int(box[3] * screen_h / 2160)
            )

        self.button_new_color: tuple[int, int, int, int] = scale_box(
            button1_box, self.max_monitor_size[0], self.max_monitor_size[1])
        self.button_new_maze: tuple[int, int, int, int] = scale_box(
            button2_box, self.max_monitor_size[0], self.max_monitor_size[1])
        self.button_show_path: tuple[int, int, int, int] = scale_box(
            button3_box, self.max_monitor_size[0], self.max_monitor_size[1])
        self.button_show_heap: tuple[int, int, int, int] = scale_box(
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

    def destroy(self) -> None:
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.maze_img.img)
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.button_ptr)
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_release(self.mlx_ptr)
        self.mlx.mlx_loop_exit(self.mlx_ptr)

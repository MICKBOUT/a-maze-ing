
from src.utils import new_maze
from src.mlx_maze.mlx_renderer import MLXRenderer
from src.exception import ConfigFileError, PathNotFound, MisplaceCell

import sys


def main() -> None:
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        print("\033[0;31mError\033[0m"
              ":No file provided")
        return

    try:
        heap, filename = new_maze(config_file=config_file)
    except ConfigFileError as e:
        print(e)
        return
    except (MisplaceCell, PathNotFound) as e:
        print("\033[0;31mError\033[0m:", e)
        return

    render = MLXRenderer(heap, filename)
    render.mlx.mlx_loop(render.mlx_ptr)


if __name__ == "__main__":
    main()

    # import mazegen
    # obj = mazegen.MazeGenerator(
    #         width=100,
    #         height=100,
    #         perfect=True)

    # maze_grid = maze.get_maze()
    # path = maze.get_path((0, 0), (99, 99))
    # print(path)

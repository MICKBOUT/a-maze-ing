import sys

from utils import new_maze
from mlx_maze.mlx_renderer import MLXRenderer
from exception import ConfigFileError, PathNotFound, MisplaceCell


def main() -> None:
    profiler = False
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2] == "profiler":
            profiler = True
    else:
        print("\033[0;31mError\033[0m"
              ":No file provided")
        return
    try:
        heap, filename = new_maze(config_file=config_file)
    except ConfigFileError as e:
        print(f"\033[0;31m{type(e).__name__}\033[0m:", e)
        return
    except (MisplaceCell, PathNotFound) as e:
        print("\033[0;31mError\033[0m:", e)
        return

    render = MLXRenderer(heap, filename, profiler=profiler)
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


from src.mazegen.utils import new_maze
from mazegen.mlx.mlx_renderer import MLXRenderer


def main() -> None:
    heap = new_maze()
    render = MLXRenderer(heap)
    render.mlx.mlx_loop(render.mlx_ptr)


if __name__ == "__main__":
    main()


from src.mazegen.utils import new_maze
from src.mazegen.drawing_mlx import MLXRenderer


def main() -> None:
    heap = new_maze()
    render = MLXRenderer(heap)
    render.mlx.mlx_loop(render.mlx_ptr)


if __name__ == "__main__":
    main()

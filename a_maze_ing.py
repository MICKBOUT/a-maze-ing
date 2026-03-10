
from src.utils import new_maze
from src.drawing_mlx import MLXRendering


def main() -> None:
    heap = new_maze()
    render = MLXRendering(heap)
    render.mlx.mlx_loop(render.mlx_ptr)


if __name__ == "__main__":
    main()

import mazegen
from mazegen.solver import solver_heap


def test_perfecte_maze_small_0() -> None:
    maze = mazegen.MazeGenerator(
        width=25,
        height=25,
        perfect=True,
    ).maze
    start = (0, 0)
    end = (24, 24)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_perfecte_maze_small_1() -> None:
    maze = mazegen.MazeGenerator(
        width=20,
        height=25,
        perfect=True,
    ).maze
    start = (0, 0)
    end = (19, 24)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_perfecte_maze_small_2() -> None:
    maze = mazegen.MazeGenerator(
        width=25,
        height=20,
        perfect=True,
    ).maze
    start = (0, 0)
    end = (24, 19)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_imperfecte_maze_small_0() -> None:
    maze = mazegen.MazeGenerator(
        width=25,
        height=25,
        perfect=False,
    ).maze
    start = (0, 0)
    end = (24, 24)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_imperfecte_maze_small_1() -> None:
    maze = mazegen.MazeGenerator(
        width=20,
        height=25,
        perfect=False,
    ).maze
    start = (0, 0)
    end = (19, 24)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_imperfecte_maze_small_2() -> None:
    maze = mazegen.MazeGenerator(
        width=25,
        height=20,
        perfect=False,
    ).maze
    start = (0, 0)
    end = (24, 19)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_perfecte_maze_medium_0() -> None:
    maze = mazegen.MazeGenerator(
        width=50,
        height=50,
        perfect=True,
    ).maze
    start = (0, 0)
    end = (49, 49)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_perfecte_maze_medium_1() -> None:
    maze = mazegen.MazeGenerator(
        width=50,
        height=75,
        perfect=True,
    ).maze
    start = (0, 0)
    end = (49, 74)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_perfecte_maze_medium_2() -> None:
    maze = mazegen.MazeGenerator(
        width=75,
        height=50,
        perfect=True,
    ).maze
    start = (0, 0)
    end = (74, 49)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_imperfecte_maze_medium_0() -> None:
    maze = mazegen.MazeGenerator(
        width=50,
        height=50,
        perfect=False,
    ).maze
    start = (0, 0)
    end = (49, 49)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_imperfecte_maze_medium_1() -> None:
    maze = mazegen.MazeGenerator(
        width=50,
        height=75,
        perfect=False,
    ).maze
    start = (0, 0)
    end = (49, 74)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_imperfecte_maze_medium_2() -> None:
    maze = mazegen.MazeGenerator(
        width=75,
        height=50,
        perfect=False,
    ).maze
    start = (0, 0)
    end = (74, 49)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_perfecte_maze_large_0() -> None:
    maze = mazegen.MazeGenerator(
        width=125,
        height=125,
        perfect=True,
    ).maze
    start = (0, 0)
    end = (124, 124)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_perfecte_maze_large_1() -> None:
    maze = mazegen.MazeGenerator(
        width=125,
        height=100,
        perfect=True,
    ).maze
    start = (0, 0)
    end = (124, 99)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_imperfecte_maze_large_0() -> None:
    maze = mazegen.MazeGenerator(
        width=125,
        height=125,
        perfect=False,
    ).maze
    start = (0, 0)
    end = (124, 124)

    path, _ = solver_heap(maze, start, end)
    assert path is not None


def test_imperfecte_maze_large_1() -> None:
    maze = mazegen.MazeGenerator(
        width=125,
        height=100,
        perfect=False,
    ).maze
    start = (0, 0)
    end = (124, 99)

    path, _ = solver_heap(maze, start, end)
    assert path is not None

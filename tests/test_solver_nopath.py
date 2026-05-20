import mazegen
from mazegen.solver import solver_heap


def test_perfecte_nopath_0() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=True,
    ).maze
    start = (0, 3)
    end = (3, 3)

    path, _ = solver_heap(maze, start, end)

    assert path is None


def test_perfecte_nopath_1() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=True,
    ).maze
    start = (3, 3)
    end = (5, 3)

    path, _ = solver_heap(maze, start, end)

    assert path is None


def test_perfecte_nopath_2() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=True,
    ).maze
    start = (5, 3)
    end = (3, 3)

    path, _ = solver_heap(maze, start, end)

    assert path is None


def test_imperfecte_nopath_0() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=False,
    ).maze
    start = (0, 3)
    end = (3, 3)

    path, _ = solver_heap(maze, start, end)

    assert path is None


def test_imperfecte_nopath_1() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=False,
    ).maze
    start = (3, 3)
    end = (5, 3)

    path, _ = solver_heap(maze, start, end)

    assert path is None


def test_imperfecte_nopath_2() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=False,
    ).maze
    start = (5, 3)
    end = (3, 3)

    path, _ = solver_heap(maze, start, end)

    assert path is None

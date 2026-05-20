import mazegen


def test_perfect_too_small_height_maze() -> None:
    width = 10
    height = 4

    try:
        mazegen.MazeGenerator(
            width=width,
            height=height,
            perfect=True
        ).maze
    except Exception:
        assert True
    else:
        assert False


def test_perfect_too_small_width_maze() -> None:
    width = 6
    height = 10
    try:
        mazegen.MazeGenerator(
            width=width,
            height=height,
            perfect=True
        ).maze
    except Exception:
        assert True
    else:
        assert False


def test_perfect_small_maze_0() -> None:
    width = 7
    height = 5
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_perfect_small_maze_1() -> None:
    width = 7
    height = 7
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_perfect_big_maze_0() -> None:
    width = 150
    height = 100
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_perfect_big_maze_1() -> None:
    width = 100
    height = 150
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_perfect_big_maze_2() -> None:
    width = 100
    height = 100
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_imperfect_too_small_height_maze() -> None:
    width = 10
    height = 4

    try:
        mazegen.MazeGenerator(
            width=width,
            height=height,
            perfect=False
        ).maze
    except Exception:
        assert True
    else:
        assert False


def test_imperfect_too_small_width_maze() -> None:
    width = 6
    height = 10
    try:
        mazegen.MazeGenerator(
            width=width,
            height=height,
            perfect=False
        ).maze
    except Exception:
        assert True
    else:
        assert False


def test_imperfect_small_maze_1() -> None:
    width = 7
    height = 5
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=False
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_imperfect_small_maze_2() -> None:
    width = 7
    height = 7
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=False
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_imperfect_big_maze_0() -> None:
    width = 150
    height = 100
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=False
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_imperfect_big_maze_1() -> None:
    width = 100
    height = 150
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=False
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width


def test_imperfect_big_maze_2() -> None:
    width = 100
    height = 100
    maze = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=False
    ).maze

    assert len(maze) == height
    assert len(maze[0]) == width

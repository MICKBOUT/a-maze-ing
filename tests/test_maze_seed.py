import mazegen


def test_perfect_maze_same_0() -> None:
    width = 25
    height = 25
    maze_0 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="123456"
    ).maze

    maze_1 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="123456"
    ).maze

    maze_2 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="123456"
    ).maze

    assert maze_0 == maze_1 == maze_2


def test_perfect_maze_same_1() -> None:
    width = 25
    height = 25
    maze_0 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="abcdefgh"
    ).maze

    maze_1 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="abcdefgh"
    ).maze

    maze_2 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="abcdefgh"
    ).maze

    assert maze_0 == maze_1 == maze_2


def test_perfect_maze_diff_0() -> None:
    width = 25
    height = 25
    maze_0 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="1234"
    ).maze

    maze_1 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="4321"
    ).maze

    assert maze_0 != maze_1


def test_perfect_maze_diff_1() -> None:
    width = 25
    height = 25
    maze_0 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="abcd"
    ).maze

    maze_1 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input="1234"
    ).maze

    assert maze_0 != maze_1


def test_perfect_maze_diff_noseed() -> None:
    width = 100
    height = 100
    maze_0 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input=None
    ).maze

    maze_1 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input=None
    ).maze

    maze_2 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=True,
        seed_input=None
    ).maze

    assert maze_0 != maze_1 != maze_2


def test_imperfect_maze_diff_noseed() -> None:
    width = 100
    height = 100
    maze_0 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=False,
        seed_input=None
    ).maze

    maze_1 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=False,
        seed_input=None
    ).maze

    maze_2 = mazegen.MazeGenerator(
        width=width,
        height=height,
        perfect=False,
        seed_input=None
    ).maze

    assert maze_0 != maze_1 != maze_2

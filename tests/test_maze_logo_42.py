import mazegen


def test_count_full_block_0() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=True,
    ).maze

    count_full_block = 0
    for row in maze:
        for cell in row:
            if cell == 15:
                count_full_block += 1

    assert count_full_block == 18


def test_count_full_block_1() -> None:
    maze = mazegen.MazeGenerator(
        width=25,
        height=25,
        perfect=True,
    ).maze

    count_full_block = 0
    for row in maze:
        for cell in row:
            if cell == 15:
                count_full_block += 1

    assert count_full_block == 18


def test_maze_logo_4() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=True,
    ).maze

    assert maze[0][0] == 15
    assert maze[1][0] == 15
    assert maze[2][0] == 15
    assert maze[2][1] == 15
    assert maze[2][2] == 15
    assert maze[3][2] == 15
    assert maze[4][2] == 15


def test_maze_logo_2() -> None:
    maze = mazegen.MazeGenerator(
        width=7,
        height=5,
        perfect=True,
    ).maze

    assert maze[0][4] == 15
    assert maze[0][5] == 15
    assert maze[0][6] == 15
    assert maze[1][6] == 15
    assert maze[2][6] == 15
    assert maze[2][5] == 15
    assert maze[2][4] == 15
    assert maze[3][4] == 15
    assert maze[4][4] == 15
    assert maze[4][5] == 15
    assert maze[4][6] == 15

from gen import gen
import heapq


def solver_heap(
        maze: list[list[int]],
        start: tuple[int, int] = (0, 0),
        end: tuple[int, int] = None):
    end = (len(maze) - 1, len(maze[0]) - 1) if end is None else end

    assert maze[start[0]][start[1]] != 15, "Error entry on full block"
    assert maze[end[0]][end[1]] != 15, "Error exit on full block"
    assert start != end, "Start and end need to be diferent"

    y_end, x_end = end
    y, x = start
    heap = []
    seen = {start}
    heapq.heappush(heap, (abs(x_end - x) + abs(y_end - y), y, x, ""))
    print(heap)
    while heap:
        # print(heap)
        dst, y, x, path = heapq.heappop(heap)
        print(y == y_end, x == x_end)
        if (y, x) == end:
            return path
        # north
        if (not (maze[y][x] >> 0) & 1) and (y - 1, x) not in seen:
            heapq.heappush(heap, (
                    abs(y_end - y - 1) + abs(x_end - x), y - 1, x, path + "N"))
            seen.add((y - 1, x))
        # East
        if (not (maze[y][x] >> 1) & 1) and (y, x + 1) not in seen:
            heapq.heappush(heap, (
                    abs(y_end - y) + abs(x_end - x + 1), y, x + 1, path + "E"))
            seen.add((y, x + 1))
        # South
        if (not (maze[y][x] >> 2) & 1) and (y + 1, x) not in seen:
            heapq.heappush(heap, (
                    abs(y_end - y + 1) + abs(x_end - x), y + 1, x, path + "S"))
            seen.add((y + 1, x))
        # West
        if (not (maze[y][x] >> 3) & 1) and (y, x - 1) not in seen:
            heapq.heappush(heap, (
                    abs(y_end - y) + abs(x_end - x - 1), y, x - 1, path + "W"))
            seen.add((y + 1, x))
    print("not found")
    print("found ?", end in seen)
# Bit Direction|
# -------------|
# 0 North      |
# 1 East       |
# 2 South      |
# 3 West       |


if __name__ == "__main__":
    maze = gen(10, 10)
    start = (0, 0)
    end = (9, 9)

    assert maze[start[0]][start[1]] != 15, "Error entry on full block"
    assert maze[end[0]][end[1]] != 15, "Error exit on full block"
    solver_heap(maze)

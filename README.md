# Genaration algorithme

Generate a perfect maze represented as a 2D grid of wall-bit masks.

Each cell is an integer bitmask with four wall bits (1 = wall present):
- 1 (LSB): north
- 2: east
- 4: south
- 8: west

The algorithm uses a randomized depth-first search (iterative
recursive-backtracker) to carve passages between cells. The grid is
initialized with all walls present (value 15) for every cell; when a
passage between two adjacent cells is created the corresponding bits in
both cells are cleared.

## Parameters
Height : int\
Number of rows in the maze (must be a positive integer).

Width : int\
Number of columns in the maze (must be a positive integer).

## Returns
list[list[int]]
    A height-by-width 2D list of integers where each integer encodes the
    walls remaining around that cell using the bit layout described above.

## Notes
- The starting cell is selected uniformly at random.
- The function prints each row of the generated grid to stdout as a list
    of integers before returning the grid.
- The function relies on the standard random module being available.

## Examples
grid = gen(5, 7)
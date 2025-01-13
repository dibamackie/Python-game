

from a1_partc import Queue

def get_overflow_list(grid):

    # Returns a list of tuples (row, col) indicating all the cells that will overflow.
    # If there are no cells that will overflow, function returns None.
    overflow_list = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            num_neighbours = get_num_neighbours(row, col, grid)
            if abs(grid[row][col]) >= num_neighbours:
                overflow_list.append((row, col))
    return overflow_list if overflow_list else None

def get_num_neighbours(row, col, grid):

    # Returns the number of neighbours for a cell at (row, col) in the grid.
    num_neighbours = 0
    if row > 0:
        num_neighbours += 1
    if row < len(grid) - 1:
        num_neighbours += 1
    if col > 0:
        num_neighbours += 1
    if col < len(grid[0]) - 1:
        num_neighbours += 1
    return num_neighbours

def overflow(grid, a_queue):
    overflow_cells = get_overflow_list(grid)

    # Check if all values in the grid are integers
    if not all(isinstance(val, int) for row in grid for val in row):
        raise ValueError("Grid contains non-integer values")

    if overflow_cells:
        init_sign = None
        all_same_sign = True

        # Check if all non-zero values in the grid are either all positive or all negative
        for row in grid:
            for val in row:
                if val != 0:
                    is_positive = val > 0
                    if init_sign is None:
                        init_sign = is_positive
                    elif init_sign != is_positive:
                        all_same_sign = False
                        break
            if not all_same_sign:
                break

        if not all_same_sign:
            # Set overflow cells to 0
            for row, col in overflow_cells:
                init_sign = grid[row][col] > 0
                grid[row][col] = 0

            # Update values of cells around each overflow cell
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for row, col in overflow_cells:
                for dir_row, dir_col in directions:
                    row_to_change, col_to_change = row + dir_row, col + dir_col
                    if 0 <= row_to_change < len(grid) and 0 <= col_to_change < len(grid[0]):
                        grid[row_to_change][col_to_change] = abs(grid[row_to_change][col_to_change]) + 1
                        grid[row_to_change][col_to_change] *= 1 if init_sign else -1

            # Make a deep copy of the grid so the original grid won't be affected later
            modified_grid = [row[:] for row in grid]  
            a_queue.enqueue(modified_grid)
            
            # Recursive call 
            return overflow(grid, a_queue) + 1

    return 0
def create_warehouse(rows, cols, obstacle_count):
    warehouse = [[0 for _ in range(cols)] for _ in range(rows)]

    def is_space_free(row, col, size):
        if col + size > cols:
            return False
        for i in range(size):
            if warehouse[row][col + i] != 0:
                return False
        return True

    def place_obstacle(row, col, size):
        for i in range(size):
            warehouse[row][col + i] = -1

    obstacle_sizes = [1, 4, 5, 6, 7, 8, 9, 10]

    for _ in range(obstacle_count):
        obstacle_placed = False
        while not obstacle_placed:
            r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
            size = random.choice(obstacle_sizes)  # Choose a random size

            if is_space_free(r, c, size):
                place_obstacle(r, c, size)
                obstacle_placed = True

    return warehouse
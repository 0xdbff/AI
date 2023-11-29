from enum import Enum
import numpy as np
import random

from .patterns import patterns


class WarehouseTypeEnum(Enum):
    Regular = 1
    Random = 2


class Environment:
    """ """

    def __init__(self, w_type: WarehouseTypeEnum, rows, cols, obstacle_count=0):
        """ """

        self.cols = cols
        self.rows = rows
        self.obstacles = obstacle_count

        self.map = np.zeros((self.rows, self.cols), dtype=np.int8)

        if (w_type is WarehouseTypeEnum.Regular):
            self._create_with_patterns()
        elif (w_type is WarehouseTypeEnum.Random):
            self._create_random()
        else:
            raise ValueError(f"Unknown Environment type: {w_type}")
        self._position_robot_and_package()

    def _position_robot_and_package(self):
        """ """

        free_spaces = np.argwhere(self.map == 0)
        robot_pos, package_pos = map(tuple, random.sample(list(free_spaces), 2))

        self.robot_pos = robot_pos
        self.package_pos = package_pos

    def _create_random(self):
        """ """

        def is_space_free(row, col, size):
            if col + size > self.cols:
                return False
            for i in range(size):
                if self.map[row][col + i] != 0:
                    return False
            return True

        def place_obstacle(row, col, size):
            for i in range(size):
                self.map[row][col + i] = -1

        obstacle_sizes = [
            1,
            int(self.rows / 6.0),
            int(self.rows / 8.0),
            int(self.rows / 16.0),
            int(self.rows / 32.0),
        ]

        for _ in range(self.obstacles):
            obstacle_placed = False
            while not obstacle_placed:
                r, c = random.randint(0, self.rows - 1), random.randint(
                    0, self.cols - 1
                )
                size = random.choice(obstacle_sizes)

                if is_space_free(r, c, size):
                    place_obstacle(r, c, size)
                    obstacle_placed = True

    def _create_with_patterns(self):
        """ """

        def is_edge(i, j, rows, cols):
            return i == 0 or j == 0 or i + 10 == rows or j + 10 == cols

        for i in range(0, self.rows, 10):
            for j in range(0, self.cols, 10):
                # Choose a pattern. At the edge, first 2 pattern types
                # are avoided to ensure paths are not blocked
                if is_edge(i, j, self.rows, self.cols):
                    selected_pattern = random.choice(patterns[2:])
                else:
                    selected_pattern = random.choice(patterns)

                # Ensure we don't go out of bounds
                end_i = min(i + 10, self.rows)
                end_j = min(j + 10, self.cols)

                self.map[i:end_i, j:end_j] = selected_pattern[: end_i - i, : end_j - j]
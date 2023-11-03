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

        self._create_with_patterns() if w_type.Regular else self._create_random()
        self._position_robot_and_package()

    def _position_robot_and_package(self):
        """ """

        free_spaces = np.argwhere(self.map == 0)
        robot_pos, package_pos = map(tuple, random.sample(list(free_spaces), 2))

        self.robot_pos = robot_pos
        self.package_pos = package_pos

    def _create_random(self):
        """ """

        # Identify all available positions for obstacles
        free_spaces = np.column_stack(np.where(self.map == 0))

        # Randomly choose positions for obstacles
        for _ in range(min(self.obstacles, free_spaces.shape[0])):
            idx = random.randrange(free_spaces.shape[0])
            r, c = free_spaces[idx]
            self.map[r, c] = -1
            free_spaces = np.delete(free_spaces, idx, 0)

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

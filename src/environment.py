from enum import Enum
from typing import Optional
import numpy as np
import random

from .patterns import patterns


class WarehouseTypeEnum(Enum):
    Regular = 1
    Random = 2


class Environment:
    """ """

    def __init__(
        self,
        w_type: WarehouseTypeEnum,
        rows=10,
        cols=10,
        obstacle_count: Optional[int] = None,
        n_packages: int = 1,
        n_robots: int = 1,
        save_fn: Optional[str] = None,
    ):
        """ """

        self.cols = cols
        self.rows = rows
        self.obstacles = obstacle_count

        self.map = np.zeros((self.rows, self.cols), dtype=np.int8)

        self.n_packages = n_packages
        self.n_robots = n_robots

        self.robot_positions = []
        self.package_positions = []

        if w_type is WarehouseTypeEnum.Regular:
            self._create_with_patterns()
        elif w_type is WarehouseTypeEnum.Random:
            self._create_random()
        else:
            raise ValueError(f"Unknown Environment type: {w_type}")

        self._place_robots()
        self._place_packages()

        if save_fn:
            self._save_to_file(save_fn)

    # @staticmethod
    # def load_from_file(filename):
    #     """Load the environment map from a file and set attributes dynamically."""
    #     with open(filename, "r") as file:
    #         map_data = np.loadtxt(file, delimiter=",", dtype=np.int8)
    #
    #     env = Environment(WarehouseTypeEnum.Regular, *map_data.shape)
    #     env.map = map_data
    #     env.rows, env.cols = map_data.shape
    #
    #     free_spaces = np.argwhere(env.map == 0)
    #     env.robot_pos, env.package_pos = map(tuple, random.sample(list(free_spaces), 2))
    #
    #     return env

    def _place_robots(self):
        """Place multiple robots at random locations."""
        self.robot_positions = []
        free_spaces = np.argwhere(self.map == 0)
        chosen_positions = random.sample(list(free_spaces), self.n_robots)

        for pos in chosen_positions:
            self.robot_positions.append(tuple(pos))

    def _place_packages(self):
        """Place multiple packages at random locations."""
        self.package_positions = []
        free_spaces = np.argwhere(self.map == 0)
        chosen_positions = random.sample(list(free_spaces), self.n_packages)

        for pos in chosen_positions:
            self.package_positions.append(tuple(pos))

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

    def _save_to_file(self, filename):
        """Save the environment map to a file."""
        np.savetxt("envs/" + filename, self.map, fmt="%d", delimiter=",")

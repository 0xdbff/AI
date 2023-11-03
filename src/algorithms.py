from enum import Enum
import collections
import numpy as np
import time
import heapq

from .environment import Environment

DIRECTIONS = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])


class AlgorithmTypeEnum(Enum):
    """ """

    BFS = "Best first seach"
    A_STAR = "fdsf"
    GREEDY = " sdlfkj"


class Search:
    """ """

    def __init__(self, a_type: AlgorithmTypeEnum, environment: Environment):
        """ """

        self.environment = environment
        self.algorithm = None
        self.path = None

        match a_type:
            case AlgorithmTypeEnum.BFS:
                self.algorithm = self._bfs_search
            case AlgorithmTypeEnum.A_STAR:
                self.algorithm = self._a_star_search
            case AlgorithmTypeEnum.GREEDY:
                self.algorithm = self._a_star_search
            case _:
                raise ValueError(f"Unknown AlgorithmType: {a_type}")

        self._run()

        if self.path:
            print("Solution found with: ", self.cost, " cost")
            print("Search Time: ", self.search_time)
            print("Total Time: ", self.search_time + self.cost, " with ", a_type)
        else:
            print("No path is available!")

    def _run(self):
        """ """
        try:
            if self.algorithm:
                s_t = time.time()
                self.algorithm()
                e_t = time.time()
                self.search_time = e_t - s_t
        except Exception as e:
            print(e)

    def _calculate_cost(self, current_dir, new_dir):
        """ """

        if (current_dir == new_dir).all():
            return 1.0
        elif (current_dir == -new_dir).all():
            return 3.0
        return 1.5

    def _bfs_search(self, uniform: bool = False):
        """ """

        rows, cols = self.environment.map.shape
        queue = collections.deque([(self.environment.robot_pos, (0, 1), 0, [])])
        visited = set()
        visited.add(self.environment.robot_pos)

        goal = self.environment.package_pos
        best_cost = float("inf")
        best_path = []

        while queue:
            position, direction, cost, path = queue.popleft()
            r, c = position

            # Check for goal state
            if position == goal and cost < best_cost:
                best_cost = cost
                best_path = path + [position]
                if uniform:
                    # If search is uniform in all directions this would be the
                    # best path
                    return

            for new_dir in DIRECTIONS:
                next_position = (r + new_dir[0], c + new_dir[1])
                if (
                    0 <= next_position[0] < rows
                    and 0 <= next_position[1] < cols
                    and self.environment.map[next_position] != -1
                ):
                    if next_position not in visited:
                        visited.add(next_position)
                        new_cost = cost + self._calculate_cost(
                            np.array(direction), np.array(new_dir)
                        )
                        queue.append(
                            (next_position, new_dir, new_cost, path + [position])
                        )

        self.path = best_path
        self.cost = best_cost

    def _heuristic(self, a, b):
        """ """

        # Manhattan distance on a square grid
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # def _a_star_search(self):
    #     """ """
    #
    #     start = self.environment.robot_pos
    #     goal = self.environment.package_pos
    #
    #     rows, cols = self.environment.map.shape
    #     queue = []
    #     heapq.heappush(
    #         queue, (0 + self._heuristic(start, goal), 0, start, [(0, 1)], [])
    #     )
    #     visited = set()
    #     visited.add(start)
    #
    #     goal = self.environment.package_pos
    #
    #     while queue:
    #         _, cost, (r, c), direction, path = heapq.heappop(queue)
    #
    #         if (r, c) == goal:
    #             self.path = path + [(r, c)]
    #             self.cost = cost
    #             return
    #
    #         for new_dir in DIRECTIONS:
    #             next_r, next_c = np.array([r, c]) + new_dir
    #             if (
    #                 0 <= next_r < rows
    #                 and 0 <= next_c < cols
    #                 and self.environment.map[next_r, next_c] != -1
    #             ):
    #                 new_cost = cost + self._calculate_cost(direction[-1], new_dir)
    #                 new_position = (next_r, next_c)
    #                 if new_position not in visited:
    #                     heapq.heappush(
    #                         queue,
    #                         (
    #                             new_cost + self._heuristic(new_position, goal),
    #                             new_cost,
    #                             new_position,
    #                             direction + [new_dir],
    #                             path + [(r, c)],
    #                         ),
    #                     )
    #                     visited.add(new_position)

    def _a_star_search(self):
        """Perform A* search to find the best path"""

        start = self.environment.robot_pos
        goal = self.environment.package_pos
        rows, cols = self.environment.map.shape
        queue = []
        heapq.heappush(
            queue, (0 + self._heuristic(start, goal), 0, start, [(0, 1)], [])
        )
        cost_so_far = {
            start: 0
        }  # This dictionary will track the best cost for each node

        while queue:
            _, current_cost, (r, c), direction, path = heapq.heappop(queue)

            if (r, c) == goal:
                self.path = path + [(r, c)]
                self.cost = current_cost
                return

            for new_dir in DIRECTIONS:
                next_r, next_c = np.array([r, c]) + new_dir
                if (
                    0 <= next_r < rows
                    and 0 <= next_c < cols
                    and self.environment.map[next_r, next_c] != -1
                ):
                    new_cost = current_cost + self._calculate_cost(
                        direction[-1], new_dir
                    )
                    new_position = (next_r, next_c)

                    if (
                        new_position not in cost_so_far
                        or new_cost < cost_so_far[new_position]
                    ):
                        cost_so_far[new_position] = new_cost
                        priority = new_cost + self._heuristic(new_position, goal)
                        heapq.heappush(
                            queue,
                            (
                                priority,
                                new_cost,
                                new_position,
                                direction + [new_dir],
                                path + [(r, c)],
                            ),
                        )

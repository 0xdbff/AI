from enum import Enum
import collections
import numpy as np
import time
import heapq

from .environment import Environment

DIRECTIONS = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])


class AlgorithmTypeEnum(Enum):
    """ """

    BFS = "Breadth First Search (BFS)"
    DIJKSTRA = "Dijkstra's Search"
    A_STAR = "A* Search"
    IDA_STAR = "Iterative Deepening A* (IDA) Search"


class Search:
    """ """

    def __init__(self, a_type: AlgorithmTypeEnum, environment: Environment):
        """ """

        self.environment = environment
        self.algorithm = None
        self.a_type = a_type.value
        self.path = None

        if a_type is AlgorithmTypeEnum.BFS:
            self.algorithm = self._bfs_search

        elif a_type is AlgorithmTypeEnum.A_STAR:
            self.algorithm = self._a_star_search

        elif a_type is AlgorithmTypeEnum.DIJKSTRA:
            self.algorithm = self._dijkstra_search

        elif a_type is AlgorithmTypeEnum.IDA_STAR:
            self.algorithm = self._a_star_search

        else:
            raise ValueError(f"Unknown AlgorithmType: {a_type}")

        self._run()

        if self.path:
            self.total_search_time = self.search_time + self.cost
        else:
            print("No path is available!")

    def print_cost(self):
        print("Solution found with: ", self.cost, " cost")
        print("Search Time: ", self.search_time)
        print("Total Time: ", self.search_time + self.cost, " with ", self.a_type)

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

    def _bfs_search(self):
        """Breadth Breadth First Search algorithm"""

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

    def _dijkstra_search(self):
        """Perform Dijkstra's algorithm to find the lowest cost path"""

        start = self.environment.robot_pos
        goal = self.environment.package_pos
        rows, cols = self.environment.map.shape

        # Priority queue to hold nodes to visit with their priority (cost)
        queue = []
        heapq.heappush(queue, (0, start, [(0, 1)], []))  # Initial cost is 0

        # Dictionary to track the best cost to reach each node
        cost_so_far = {start: 0}

        while queue:
            current_cost, (r, c), direction, path = heapq.heappop(queue)

            # If goal is reached, set the path and cost and return
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
                    new_position = (next_r, next_c)
                    new_cost = current_cost + self._calculate_cost(
                        direction[-1], new_dir
                    )

                    # Check if new path is cheaper or node hasn't been visited
                    if (
                        new_position not in cost_so_far
                        or new_cost < cost_so_far[new_position]
                    ):
                        cost_so_far[new_position] = new_cost
                        heapq.heappush(
                            queue,
                            (
                                new_cost,
                                new_position,
                                direction + [new_dir],
                                path + [(r, c)],
                            ),
                        )

    def _heuristic(self, a, b):
        """
        Manhattan distance on a square grid Heuristic
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def _a_star_search(self):
        """Perform A* search to find the best path"""

        start = self.environment.robot_pos
        goal = self.environment.package_pos
        rows, cols = self.environment.map.shape
        queue = []
        heapq.heappush(
            queue, (0 + self._heuristic(start, goal), 0, start, [(0, 1)], [])
        )
        cost_so_far = {start: 0}

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

    def _ida_star_search(self):
        """Perform Iterative Deepening A* (IDA*) search to find the best path"""

        start = self.environment.robot_pos
        goal = self.environment.package_pos

        def search(path, g, bound):
            node = path[-1]
            f = g + self._heuristic(node, goal)
            if f > bound:
                return f
            if node == goal:
                return True
            min_bound = float("inf")
            for new_dir in DIRECTIONS:
                next_r, next_c = np.array(node) + new_dir
                if (
                    0 <= next_r < self.environment.map.shape[0]
                    and 0 <= next_c < self.environment.map.shape[1]
                    and self.environment.map[next_r, next_c] != -1
                    and (next_r, next_c) not in path
                ):
                    path.append((next_r, next_c))
                    new_cost = g + self._calculate_cost(
                        np.array(DIRECTIONS[-1]), new_dir
                    )
                    t = search(path, new_cost, bound)
                    if t is True:
                        return True
                    if t < min_bound:
                        min_bound = t
                    path.pop()
            return min_bound

        bound = self._heuristic(start, goal)
        path = [start]
        while True:
            t = search(path, 0, bound)
            if t is True:
                self.path = path[:]
                self.cost = sum(
                    [
                        self._calculate_cost(
                            np.array(DIRECTIONS[-1]), np.array(DIRECTIONS[i % 4])
                        )
                        for i in range(len(path) - 1)
                    ]
                )
                return
            if t == float("inf"):
                self.path = None
                return
            bound = t

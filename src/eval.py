from .algorithms import AlgorithmTypeEnum, Search, HeuristicEnum
from .environment import Environment, WarehouseTypeEnum


def test_algorithms(algorithms, heuristic, iterations=10, rows=200, cols=200):
    absolute_data = {alg: [] for alg in algorithms}
    relative_data = {alg: [] for alg in algorithms}

    for _ in range(iterations):
        env = Environment(WarehouseTypeEnum.Regular, rows, cols)
        times = []

        for alg in algorithms:
            search = Search(alg, env, heuristic)
            times.append(search.total_search_time)
            absolute_data[alg].append(search.total_search_time)

        min_time = min(times)
        for alg in algorithms:
            relative_data[alg].append(min_time / absolute_data[alg][-1] * 100)

    return absolute_data, relative_data

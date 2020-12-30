from collections import Counter
from itertools import chain
from pkg.ai.pathfinders import Node


def merge_paths(*paths):
    merged = [p for p in chain(*paths)]
    return list(dict.fromkeys(merged))


def compare_paths(path1, path2):
    def path_to_ids(path):
        return [Node(p[0], p[1]).id() for p in path]
    ids1 = path_to_ids(path1)
    ids2 = path_to_ids(path2)
    return Counter(ids1) == Counter(ids2)

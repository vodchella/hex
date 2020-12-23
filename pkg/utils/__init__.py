import itertools


def merge_paths(*paths):
    merged = [p for p in itertools.chain(*paths)]
    return list(dict.fromkeys(merged))

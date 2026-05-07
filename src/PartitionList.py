from typing import List
import random


def partition_list(l: List, k: int, seed=0):
    """Partitions a list into two random lists, the first of which has length k and the second part being the difference
    of the whole list and the first part."""
    if k > len(l):
        raise IndexError(f'Index {k} must be smaller than or equal to the length of list, which is {len(l)}.')

    random.seed(seed)
    randomized_l = l.copy()
    random.shuffle(randomized_l)

    first_part = randomized_l[:k]
    second_part = randomized_l[k:]
    return first_part, second_part

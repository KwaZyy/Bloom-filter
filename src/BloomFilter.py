import copy
import time
from pathlib import Path
import numpy as np


class BloomFilter:
    """BloomFilter represents a Bloom filter object of length m and using the given hash functions."""
    
    def __init__(self, m: int, *hash_functions) -> None:
        self.m = m
        self.hash_functions = hash_functions
        self.array = m*[0]

    def add(self, x) -> None:
        """Adds the given string or list of strings to the Bloom filter."""
        # Checks if x is a list or a singular string
        items = [x] if isinstance(x, str) else x

        for item in items:
            for hash_function in self.hash_functions:
                index = hash_function(item) % self.m
                self.array[index] = 1

    def search(self, x: str) -> bool:
        """Searches the bloom filter and returns False if x is not present otherwise returns
        True if x is possibly present."""
        for hash_function in self.hash_functions:
            if self.array[hash_function(x) % self.m] == 0:
                return False
        return True


class KMBloomFilter(BloomFilter):
    """Subclass of BloomFilter that uses the Kirsch-Mitzenmacher optimization to generate k hashing functions."""
    def __init__(self, m: int, h1, h2, k: int) -> None:

        hash_functions = [(lambda x, i=i: h1(x) + i * h2(x)) for i in range(k)]
        super().__init__(m, *hash_functions)


def false_positive_rate(empty_filter, total_strings, inserted_strings):
    """For a given empty Bloom filter inserts a series of strings and returns the approximate false error rate for the
     filled filter. The false positive rate is the probability that one of the strings in total_strings, which is not
     in inserted_strings, results in a True when searching."""
    filter = copy.deepcopy(empty_filter)
    filter.add(inserted_strings)
    false_positive_list = (len(total_strings) - len(inserted_strings)) * [0]
    for j, word in enumerate(list(set(total_strings) - set(inserted_strings))):
        if filter.search(word):
            false_positive_list[j] = 1
    false_positive_rate = sum(false_positive_list) / len(false_positive_list)
    return false_positive_rate


def time_search_add(dataset, empty_filter: BloomFilter):
    """For a given dataset and empty bloom filter returns a tuple containing four lists, which contain the time needed
    for each search and addition and the amount of cumulative time needed for these operations. The searching is done
    for a Bloom filter in which we include the previous elements, this highlights how the amount of time changes as the
    amount of elements in a filter increase."""

    # Copy empty filter
    filter = copy.deepcopy(empty_filter)

    # Accessing dataset
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / dataset

    with open(data_path, 'r') as file:
        data_list = file.read().splitlines()

    # Calculating time per search and add
    time_per_search = []
    time_per_add = []
    for string in data_list:
        start = time.perf_counter()
        filter.search(string)
        end = time.perf_counter()
        time_per_search.append(end - start)

        start = time.perf_counter()
        filter.add(string)
        end = time.perf_counter()
        time_per_add.append(end - start)

    # Calculating cumulative time per search and add
    cumulative_time_per_search = np.cumsum(time_per_search)
    cumulative_time_per_add = np.cumsum(time_per_add)
    return (time_per_search, time_per_add), (cumulative_time_per_search, cumulative_time_per_add)

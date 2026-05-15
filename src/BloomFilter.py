import copy


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



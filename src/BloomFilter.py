class BloomFilter:
    """BloomFilter represents a Bloom filter object of length m and using the given hash functions."""
    
    def __init__(self, m: int, *hash_functions) -> None:
        self.m = m
        self.hash_functions = hash_functions
        self.array = m*[0]

    def add(self, x: str) -> None:
        """Adds the given string x to the Bloom filter."""
        for hash_function in self.hash_functions:
            self.array[hash_function(x) % self.m] = 1

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

#testing testing
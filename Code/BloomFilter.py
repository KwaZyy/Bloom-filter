class BloomFilter:
    """BloomFilter represents a Bloom filter object of length m and using the given hash functions."""
    
    def __init__(self, m: int, *hash_functions) -> None:
        self.m = m
        self.hash_functions = hash_functions
        self.filter = m*[0]

    def add(self, x: str) -> None:
        """adds the given string x to the Bloom filter."""
        for hash_function in self.hash_functions:
            self.filter[hash_function(x) % self.m] = 1

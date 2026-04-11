class BloomFilter:
    """BloomFilter represents a Bloom filter object of length m and using the given hash functions."""
    
    def __init__(self, m: int, *hash_functions) -> None:
        self.m = m
        self.hash_functions = hash_functions
        self.filter = m*[0]

    def add(self, x: str) -> None:
        """Adds the given string x to the Bloom filter."""
        for hash_function in self.hash_functions:
            self.filter[hash_function(x) % self.m] = 1

    def search(self, x: str) -> bool:
        """Searches the bloom filter and returns False if x is not present otherwise returns
        True if x is possibly present."""
        for hash_function in self.hash_functions:
            if self.filter[hash_function(x) % self.m] == 0:
                return False
        return True
import pickle
import os

# ... inside your BloomFilter class ...

    def save(self, filepath: str) -> None:
        """
        
        Serializes the current state of the Bloom filter to a file.
        This captures the bit array and the size m.
        """
        try:
            with open(filepath, 'wb') as f:
                # We store the filter and the size m as a dictionary
                state = {
                    'm': self.m,
                    'filter': self.filter
                }
                pickle.dump(state, f)
            print(f"Successfully saved Bloom filter to: {filepath}")
        except Exception as e:
            print(f"Error saving filter: {e}")

    @classmethod
    def load(cls, filepath: str, *hash_functions):
        """
        Loads a Bloom filter from a file. 
        Note: You must provide the same hash functions used during creation.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No saved filter found at {filepath}")
            
        with open(filepath, 'rb') as f:
            state = pickle.load(f)
            
        # Reconstruct the object using the stored size m and provided hashes
        instance = cls(state['m'], *hash_functions)
        instance.filter = state['filter']
        return instance
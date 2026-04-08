from src.HashingFunctions import djb2
from src.BloomFilter import BloomFilter

m = 5
small_filter = BloomFilter(m, djb2)

# Adding elements
print(djb2("a") % m)
print(djb2("b") % m)
small_filter.add("a")
small_filter.add("b")
print(small_filter.filter)


# Searching elements
print(small_filter.search("a"))
print(small_filter.search("b"))
print(djb2("c") % m)
print(small_filter.search("c"))  # Not in set
print(djb2("z") % m)
print(small_filter.search("z"))  # False positive

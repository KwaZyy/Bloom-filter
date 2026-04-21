from src.HashingFunctions import djb2, sdbm
from src.BloomFilter import BloomFilter, KMBloomFilter

m = 5
small_filter = BloomFilter(m, djb2)

# Adding elements
print(djb2("a") % m)
print(djb2("b") % m)
small_filter.add("a")
small_filter.add("b")
print(small_filter.array)


# Searching elements
print(small_filter.search("a"))
print(small_filter.search("b"))
print(djb2("c") % m)
print(small_filter.search("c"))  # Not in set
print(djb2("z") % m)
print(small_filter.search("z"))  # False positive


# Kirsch-Mitzenmacher Bloom filter

KM = KMBloomFilter(15, djb2, sdbm, 3)
KM.add("a")
KM.add("b")
KM.add("c")
print(KM.array)

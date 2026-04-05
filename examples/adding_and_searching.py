from Code.HashingFunctions import djb2
from Code.BloomFilter import BloomFilter

m = 5
small_filter = BloomFilter(m, djb2)

print(djb2("a") % m)
print(djb2("b") % m)

small_filter.add("a")
small_filter.add("b")
print(small_filter.filter)
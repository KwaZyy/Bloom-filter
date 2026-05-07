from src.BloomFilter import BloomFilter, KMBloomFilter,\
    plot_time_search_add, plot_cumulative_time_per_hash, plot_time_length_string
from src.HashingFunctions import lose_lose, djb2, sdbm, MurmurHash3

plot_time_search_add("words.txt", KMBloomFilter(200000, sdbm, MurmurHash3, 3))
plot_time_search_add("DNA.txt", KMBloomFilter(5000000, sdbm, MurmurHash3, 5))


plot_cumulative_time_per_hash("words.txt", 200000, sdbm, MurmurHash3, 20)
plot_cumulative_time_per_hash("DNA.txt", 5000000, sdbm, MurmurHash3, 20)

plot_time_length_string(BloomFilter(10000, lose_lose), "lose_lose")
plot_time_length_string(KMBloomFilter(1000, sdbm, MurmurHash3, 5), "traditional_filter")

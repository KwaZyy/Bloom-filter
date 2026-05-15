from src.BloomFilter import KMBloomFilter
from src.BloomFilterPlots import false_positive_against_inserted_strings
from src.HashingFunctions import sdbm, MurmurHash3

false_positive_against_inserted_strings("words.txt", KMBloomFilter(200000, sdbm, MurmurHash3, 3), 200)
false_positive_against_inserted_strings("DNA.txt", KMBloomFilter(800000, sdbm, MurmurHash3, 5), 200)

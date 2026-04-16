from src.PartitionList import partition_list
import json

with open('words.txt', 'r') as file:
    words = file.read().splitlines()


n = [10, 100, 1000, 10000, 100000, 200000, 400000]

words_dict = {}
for i in n:
    words_dict[i] = partition_list(words, i, 0)

with open('words_bloom_filter.json', 'w') as file:
    json.dump(words_dict, file, indent=4)

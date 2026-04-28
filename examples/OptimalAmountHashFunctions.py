import numpy as np

from src.BloomFilter import KMBloomFilter, false_positive_rate
from src.HashingFunctions import sdbm, MurmurHash3
import random
from pathlib import Path
import math
import matplotlib.pyplot as plt


current_dir = Path(__file__).parent

words_path = current_dir.parent / "datasets" / "words.txt"
with open(words_path, 'r') as file:
    words = file.read().splitlines()

DNA_path = current_dir.parent / "datasets" / "DNA.txt"
with open(DNA_path, 'r') as file:
    DNA = file.read().splitlines()


random.seed(0)  # For reproducibility
randomized_words = words.copy()
random.shuffle(randomized_words)
randomized_DNA = DNA.copy()
random.shuffle(randomized_DNA)

n1 = 30000
m1 = 300000
subset_words = randomized_words[:n1]

max_k1 = 20
words_error_rates = max_k1 * [0]
x1 = np.linspace(1, max_k1, 1000)
y1 = (1-np.exp(-x1*n1/m1))**x1

for k in range(1, max_k1+1):
    words_error_rates[k-1] = false_positive_rate(KMBloomFilter(m1, sdbm, MurmurHash3, k), words, subset_words)

optimal_k_words = m1/n1 * math.log(2)

plt.plot(list(range(1, max_k1+1)), words_error_rates, label="Actual error rate")
plt.plot(x1, y1, label="Theoretical error rate")
plt.xlabel("Amount of hash functions")
plt.ylabel("False positive rate")
plt.axvline(x=optimal_k_words, color="r", label="Theoretical minimum", linestyle="dashed")
plt.legend()
plt.grid(True)
plt.savefig("OptimalAmountHashFunctions_words")
plt.clf()

n2 = 200000
m2 = 1000000
subset_DNA = randomized_DNA[:n2]

max_k2 = 10
DNA_error_rates = max_k2 * [0]
x2 = np.linspace(1, max_k2, 1000)
y2 = (1-np.exp(-x2*n2/m2))**x2

for k in range(1, max_k2+1):
    DNA_error_rates[k-1] = false_positive_rate(KMBloomFilter(m2, sdbm, MurmurHash3, k), DNA, subset_DNA)

optimal_k_DNA = m2/n2 * math.log(2)

plt.plot(list(range(1, max_k2+1)), DNA_error_rates, label="Actual error rate")
plt.plot(x2, y2, label="Theoretical error rate")
plt.xlabel("Amount of hash functions")
plt.ylabel("False positive rate")
plt.axvline(x=optimal_k_DNA, color="r", label="Theoretical minimum", linestyle="dashed")
plt.legend()
plt.grid(True)
plt.savefig("OptimalAmountHashFunctions_DNA")
plt.clf()

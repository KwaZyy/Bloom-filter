import numpy as np
from src.BloomFilter import KMBloomFilter, false_positive_rate
from src.HashingFunctions import lose_lose, djb2, sdbm, MurmurHash3
import random
from pathlib import Path
import math
import matplotlib.pyplot as plt
import os


def error_against_amount_hash(dataset, n, m, max_k, h1=sdbm, h2=MurmurHash3, seed=0):
    """Returns a plot showing how the error rate changes as the amount of hash functions increase.
    'dataset' denotes which bloom filter of size m we create and for which n random strings of the dataset are inserted.
    The extra hash functions are generated using the Kirsch-Mitzenmatcher optimization for two given hash functions."""

    # Accessing datasets
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / dataset
    data_name = Path(data_path).stem

    with open(data_path, 'r') as file:
        data_list = file.read().splitlines()

    # Creating random subset of data
    random.seed(seed)
    randomized_data = data_list.copy()
    random.shuffle(randomized_data)
    subset_data = randomized_data[:n]
    empirical_error_rate = max_k * [0]

    # Constructing theoretical error rate
    x = np.linspace(1, max_k, 1000)
    theoretical_error_rate = (1 - np.exp(-x * n / m)) ** x

    # Constructing empirical error rates for each k-value
    for k in range(1, max_k + 1):
        empirical_error_rate[k-1] = false_positive_rate(KMBloomFilter(m, h1, h2, k), data_list, subset_data)
    optimal_k = m / n * math.log(2)

    # Plotting and saving the graph
    plt.plot(list(range(1, max_k + 1)), empirical_error_rate, label="Empirical  error rate")
    plt.plot(x, theoretical_error_rate, label="Theoretical error rate")
    plt.xlabel("Amount of hash functions")
    plt.ylabel("False positive rate")
    plt.axvline(x=optimal_k, color="r", label="Theoretical minimum", linestyle="dashed")
    plt.legend()
    plt.grid(True)
    if not os.path.exists("false_positive _rate_plots"):
        os.mkdir("false_positive_rate_plots")
    plt.savefig(f"false_positive_rate_plots/OptimalAmountHashFunctions_{data_name}")
    plt.clf()


error_against_amount_hash("words.txt", 30000, 300000, 20)
error_against_amount_hash("DNA.txt", 200000, 1000000, 10)

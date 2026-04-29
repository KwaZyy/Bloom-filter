import numpy as np
from src.BloomFilter import BloomFilter, KMBloomFilter, false_positive_rate
from src.HashingFunctions import lose_lose, djb2, sdbm, MurmurHash3
import random
from pathlib import Path
import matplotlib.pyplot as plt
import os


def false_positive_against_inserted_strings(dataset, empty_filter, samples=200, seed=0):
    """Plots the false positive rate against the amount of inserted strings when inserting into an empty Bloom filter.
    The graph is plotted over an equidistant amount, given by samples, of points from 0 to the length of the dataset
    (excluding that last point, because there are no more possible inserted strings). The given seed denotes how the
    data is randomized, to possibly remove any ordering when adding strings."""
    # Accessing datasets
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / dataset
    data_name = Path(data_path).stem

    with open(data_path, 'r') as file:
        data_list = file.read().splitlines()

    # Randomizing data
    random.seed(seed)
    randomized_data = data_list.copy()

    # Calculating theoretical false positive rates
    m = empty_filter.m
    k = len(empty_filter.hash_functions)
    n_values = np.linspace(1, len(data_list), samples+1).round().astype(int)
    n_values = n_values[:-1]
    theoretical_false_positive_rate = (1 - np.exp(-k * n_values / m)) ** k

    # Calculating empirical error rates
    empirical_false_positive_rate = len(n_values) * [0]
    for i, n in enumerate(n_values):
        empirical_false_positive_rate[i] = false_positive_rate(empty_filter, randomized_data, randomized_data[:n])

    # Plotting and saving the graph
    plt.plot(n_values, empirical_false_positive_rate, label="Empirical false positive rate")
    plt.plot(n_values, theoretical_false_positive_rate, label="Theoretical false positive rate")
    plt.xlabel("Amount of inserted strings")
    plt.ylabel("False positive rate")
    plt.axvline(x=m, color="r", label="Size of Bloom filter", linestyle="dashed")
    plt.legend()
    plt.grid(True)
    if not os.path.exists("false_positive_rate_plots"):
        os.mkdir("false_positive_rate_plots")
    plt.savefig(f"false_positive_rate_plots/FalsePositiveRateIncreasingStrings_{data_name}")
    plt.clf()


false_positive_against_inserted_strings("words.txt", KMBloomFilter(200000, sdbm, MurmurHash3, 3), 200)
false_positive_against_inserted_strings("DNA.txt", KMBloomFilter(800000, sdbm, MurmurHash3, 5), 200)

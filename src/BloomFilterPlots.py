import copy
import time
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import math

from src.BloomFilter import BloomFilter, KMBloomFilter, false_positive_rate
from src.HashingFunctions import sdbm, MurmurHash3


def time_search_add(dataset, empty_filter: BloomFilter):
    """For a given dataset and empty bloom filter returns a tuple containing four lists, which contain the time needed
    for each search and addition and the amount of cumulative time needed for these operations. The searching is done
    for a Bloom filter in which we include the previous elements, this highlights how the amount of time changes as the
    amount of elements in a filter increase."""

    # Copy empty filter
    filter = copy.deepcopy(empty_filter)

    # Accessing dataset
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / dataset

    with open(data_path, 'r') as file:
        data_list = file.read().splitlines()

    # Calculating time per search and add
    time_per_search = []
    time_per_add = []
    for string in data_list:
        start = time.perf_counter()
        filter.search(string)
        end = time.perf_counter()
        time_per_search.append(end - start)

        start = time.perf_counter()
        filter.add(string)
        end = time.perf_counter()
        time_per_add.append(end - start)

    # Calculating cumulative time per search and add
    cumulative_time_per_search = np.cumsum(time_per_search)
    cumulative_time_per_add = np.cumsum(time_per_add)
    return (np.array(time_per_search), np.array(time_per_add)), (cumulative_time_per_search, cumulative_time_per_add)


def plot_time_search_add(dataset, empty_filter: BloomFilter):
    """For a given empty Bloom filter and dataset returns box plots of the difference between adding and searching for
    the filter with and without outliers, box plots of searching and adding, and a line plot of the cumulative time
    for adding and searching."""
    # Time per search and add
    time_list = time_search_add(dataset, empty_filter)

    time_per_search = time_list[0][0]
    time_per_add = time_list[0][1]

    cumulative_time_per_search = time_list[1][0]
    cumulative_time_per_add = time_list[1][1]

    # Amount of total strings
    n = len(time_list[0][0])
    n_values = list(range(1, n+1))

    # String name of the dataset for saving plots
    data_name = Path(dataset).stem

    # Box plot of difference between adding and searching
    plt.boxplot(np.array(time_per_add) - np.array(time_per_search), tick_labels=["add time - search time"],
                patch_artist=True)
    plt.ylabel("Time (seconds)")
    plt.axhline(0, color='red', linestyle='--', alpha=0.6, label='Zero Difference')
    plt.grid(True, which="both", ls="-", alpha=0.2)
    if not os.path.exists("time_plots"):
        os.mkdir("time_plots")
    plt.savefig(f"time_plots/diff_add_search_{data_name}", bbox_inches="tight")
    plt.clf()

    # Box plot of difference between adding and searching with no outliers
    plt.boxplot(np.array(time_per_add) - np.array(time_per_search), tick_labels=["add time - search time"],
                patch_artist=True, showfliers=False)
    plt.ylabel("Time (seconds)")
    plt.axhline(0, color='red', linestyle='--', alpha=0.6, label='Zero Difference')
    plt.grid(True, which="both", ls="-", alpha=0.2)
    if not os.path.exists("time_plots"):
        os.mkdir("time_plots")
    plt.savefig(f"time_plots/diff_add_search_no_outliers_{data_name}", bbox_inches="tight")
    plt.clf()

    # Box plots of searching and adding
    plt.boxplot([time_per_search, time_per_add], tick_labels=["Search", "Add"], patch_artist=True)
    plt.yscale("log")
    plt.ylabel("Time (seconds) in log scale")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    if not os.path.exists("time_plots"):
        os.mkdir("time_plots")
    plt.savefig(f"time_plots/add_search_{data_name}", bbox_inches="tight")
    plt.clf()

    # Line plot of cumulative time needed for searching and adding the entire dataset
    plt.plot(n_values, cumulative_time_per_search, label="Search")
    plt.plot(n_values, cumulative_time_per_add, label="Add")
    plt.xlabel("Amount of tested/inserted strings")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    if not os.path.exists("time_plots"):
        os.mkdir("time_plots")
    plt.savefig(f"time_plots/cumulative_add_search_{data_name}", bbox_inches="tight")
    plt.clf()


def plot_cumulative_time_per_hash(dataset, m, h1, h2, max_k):
    """Returns a line plot showing how the amount of cumulative time needed for searching and adding all elements into
    a Bloom filter changes as the amount of hash functions of the filter increase."""

    # String name of the dataset for saving plots
    data_name = Path(dataset).stem

    # Initialization of cumulative time vectors per hash function
    cumulative_search_per_k = []
    cumulative_add_per_k = []

    # Calculating total time needed for searching and adding for an increasing amount of hash functions
    for k in range(1, max_k + 1):
        filter = KMBloomFilter(m, h1, h2, k)
        time_list = time_search_add(dataset, filter)
        cumulative_search_per_k.append(time_list[1][0][-1])
        cumulative_add_per_k.append(time_list[1][1][-1])

    # Line plot of cumulative time needed for searching and adding for an increasing amount of hash functions
    plt.plot(list(range(1, max_k + 1)), cumulative_search_per_k, label="Search")
    plt.plot(list(range(1, max_k + 1)), cumulative_add_per_k, label="Add")
    plt.xlabel("Amount of hash functions")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    if not os.path.exists("time_plots"):
        os.mkdir("time_plots")
    plt.savefig(f"time_plots/cumulative_add_search_per_hash_{data_name}", bbox_inches="tight")
    plt.clf()


def plot_time_length_string(filter: BloomFilter, plot_name: str, max_length=None):
    """Returns a line plot of the amount time needed to search and add strings of increasing length of the form a, aa,
     aaa, etc."""
    # If max length is not specified choose size of Bloom filter
    if max_length is None:
        max_length = filter.m

    # Calculates time per search and add for increasing strings of the form a, aa, aaa, etc...
    time_per_search = []
    time_per_add = []
    for i in range(1, max_length + 1):
        string = "a" * i
        start = time.perf_counter()
        filter.search(string)
        end = time.perf_counter()
        time_per_search.append(end - start)

        start = time.perf_counter()
        filter.add(string)
        end = time.perf_counter()
        time_per_add.append(end - start)

    # Line plot of time needed for searching and adding for a string of increasing size
    plt.plot(list(range(1, max_length + 1)), time_per_search, label="Search")
    plt.plot(list(range(1, max_length + 1)), time_per_add, label="Add")
    plt.xlabel("Length of string")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    if not os.path.exists("time_plots"):
        os.mkdir("time_plots")
    plt.savefig(f"time_plots/time_length_string_{plot_name}", bbox_inches="tight")
    plt.clf()


# False-positive plot helpers

def false_positive_against_filter_size(
    dataset,
    n,
    max_m,
    h1=sdbm,
    h2=MurmurHash3,
    k=3,
    samples=25,
    seed=0,
):
    """Plot the false positive rate as the Bloom filter size m increases.

    The number of inserted strings n and the number of hash functions k are
    kept fixed. For each Bloom filter size m, the same number of strings is
    inserted, and the empirical false positive rate is calculated.

    Parameters
    ----------
    dataset : str
        Name of the dataset file stored in the datasets folder.
    n : int
        Number of strings inserted into each Bloom filter.
    max_m : int
        Largest Bloom filter size to test.
    h1, h2 : callable
        Base hash functions used to construct the Kirsch-Mitzenmacher hash
        functions.
    k : int
        Number of hash functions used by the Bloom filter.
    samples : int
        Number of different Bloom filter sizes to test.
    seed : int
        Random seed used to shuffle the dataset reproducibly.
    """

    # Access dataset
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / dataset
    data_name = Path(data_path).stem

    with open(data_path, "r") as file:
        data_list = file.read().splitlines()

    if n >= len(data_list):
        raise ValueError("n must be smaller than the number of strings in the dataset.")

    # Shuffle data so the inserted strings are selected reproducibly
    random.seed(seed)
    randomized_data = data_list.copy()
    random.shuffle(randomized_data)
    inserted_data = randomized_data[:n]

    # Create increasing Bloom filter sizes
    min_m = max(k + 1, n // 10)
    m_values = np.linspace(min_m, max_m, samples).round().astype(int)
    m_values = [int(m) for m in np.unique(m_values)]
    m_values_array = np.array(m_values)

    # Calculate theoretical false positive rates
    x = np.linspace(min_m, max_m, 25*samples)
    theoretical_false_positive_rate = (1 - np.exp(-k * n / x)) ** k

    # Calculate empirical false positive rates
    empirical_false_positive_rate = []
    for m in m_values:
        empty_filter = KMBloomFilter(m, h1, h2, k)
        empirical_false_positive_rate.append(
            false_positive_rate(empty_filter, data_list, inserted_data)
        )

    # Plotting and saving the graph
    plt.plot(m_values_array, empirical_false_positive_rate, label="Empirical false positive rate")
    plt.plot(x, theoretical_false_positive_rate, label="Theoretical false positive rate")
    plt.xlabel("Bloom filter size m")
    plt.ylabel("False positive rate")
    plt.legend()
    plt.grid(True)
    if not os.path.exists("false_positive_rate_plots"):
        os.mkdir("false_positive_rate_plots")
    plt.savefig(f"false_positive_rate_plots/FalsePositiveRateIncreasingFilterSize_{data_name}")
    plt.clf()


def false_positive_against_inserted_strings(dataset, empty_filter, samples=200, seed=0):
    """Plots the false positive rate against the amount of inserted strings when inserting into an empty Bloom filter.

    The graph is plotted over an equidistant amount, given by samples, of points from 0 to the length of the dataset
    excluding the last point, because there are no more possible inserted strings. The given seed denotes how the
    data is randomized, to possibly remove any ordering when adding strings.
    """
    # Accessing dataset
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / dataset
    data_name = Path(data_path).stem

    with open(data_path, "r") as file:
        data_list = file.read().splitlines()

    # Randomizing data
    random.seed(seed)
    randomized_data = data_list.copy()
    random.shuffle(randomized_data)

    # Calculating theoretical false positive rates
    m = empty_filter.m
    k = len(empty_filter.hash_functions)
    n_values = np.linspace(1, len(data_list), samples + 1).round().astype(int)
    n_values = n_values[:-1]
    theoretical_false_positive_rate = (1 - np.exp(-k * n_values / m)) ** k

    # Calculating empirical error rates
    empirical_false_positive_rate = [0.0] * len(n_values)
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


def false_positive_against_amount_hash(dataset, n, m, max_k, h1=sdbm, h2=MurmurHash3, seed=0):
    """Returns a plot showing how the false positive rate changes as the amount of hash functions increase.
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
    empirical_false_positive_rate = [0.0] * max_k

    # Calculating theoretical false positive rates
    x = np.linspace(1, max_k, 1000)
    theoretical_false_positive_rate = (1 - np.exp(-x * n / m)) ** x

    # Calculating empirical false positive rates for each k-value
    for k in range(1, max_k + 1):
        empirical_false_positive_rate[k-1] = false_positive_rate(KMBloomFilter(m, h1, h2, k), data_list, subset_data)
    optimal_k = m / n * math.log(2)

    # Plotting and saving the graph
    plt.plot(list(range(1, max_k + 1)), empirical_false_positive_rate, label="Empirical false positive rate")
    plt.plot(x, theoretical_false_positive_rate, label="Theoretical false positive rate")
    plt.xlabel("Amount of hash functions")
    plt.ylabel("False positive rate")
    plt.axvline(x=optimal_k, color="r", label="Theoretical minimum", linestyle="dashed")
    plt.legend()
    plt.grid(True)
    if not os.path.exists("false_positive_rate_plots"):
        os.mkdir("false_positive_rate_plots")
    plt.savefig(f"false_positive_rate_plots/OptimalAmountHashFunctions_{data_name}")
    plt.clf()

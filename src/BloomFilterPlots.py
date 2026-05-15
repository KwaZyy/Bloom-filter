import copy
import time
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os

from src.BloomFilter import BloomFilter, KMBloomFilter

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

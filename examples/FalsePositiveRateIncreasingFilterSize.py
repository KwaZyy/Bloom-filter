import numpy as np
from src.BloomFilter import KMBloomFilter, false_positive_rate
from src.HashingFunctions import sdbm, MurmurHash3
import random
from pathlib import Path
import matplotlib.pyplot as plt
import os


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
    theoretical_false_positive_rate = (1 - np.exp(-k * n / m_values_array)) ** k

    # Calculate empirical false positive rates
    empirical_false_positive_rate = []
    for m in m_values:
        empty_filter = KMBloomFilter(m, h1, h2, k)
        empirical_false_positive_rate.append(
            false_positive_rate(empty_filter, data_list, inserted_data)
        )

    # Plotting and saving the graph
    plt.plot(m_values_array, empirical_false_positive_rate, label="Empirical false positive rate")
    plt.plot(m_values_array, theoretical_false_positive_rate, label="Theoretical false positive rate")
    plt.xlabel("Bloom filter size m")
    plt.ylabel("False positive rate")
    plt.legend()
    plt.grid(True)

    plot_dir = current_dir / "false_positive_rate_plots"
    plot_dir.mkdir(exist_ok=True)

    plt.savefig(plot_dir / f"FalsePositiveRateIncreasingFilterSize_{data_name}")
    plt.clf()


if __name__ == "__main__":
    false_positive_against_filter_size("words.txt", 30000, 1000000, k=3, samples=25)
    false_positive_against_filter_size("DNA.txt", 200000, 3000000, k=5, samples=25)
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mmh3
import os


def lose_lose(s: str) -> int:
    """Implementation of loselose hash function."""
    h = 0
    for char in s:
        h += ord(char)
    return h


def djb2(s: str) -> int:
    """Implementation of the djb2 hash function."""
    h = 5381
    for char in s:
        h = ((h << 5) + h) + ord(char)  # h = h * 33 + ord(char)
    return h


def sdbm(s: str) -> int:
    """Implementation of the sdbm hash function."""
    h = 0
    for char in s:
        h = ord(char) + (h << 6) + (h << 16) - h
    return h


def MurmurHash3(s: str, seed=815) -> int:
    """Implementation of the MurmurHash3 function."""
    return mmh3.hash(s, seed, signed=False)


def distribution(data, hash_function, m):
    """Returns a histogram of the modulo m reduced hash values of a dataset 'data'."""
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / data
    data_name = Path(data_path).stem
    with open(data_path, 'r') as file:
        data_list = file.read().splitlines()

    hash_values = np.array([hash_function(string) for string in data_list])
    print(f"Mean: {np.mean(hash_values)}")
    print(f"Median: {np.median(hash_values)}")

    original = [h for h in hash_values if h < m]
    modulo_reduced = [h % m for h in hash_values if h >= m]
    function_name = hash_function.__name__
    plt.hist([original, modulo_reduced], stacked=True,
             color=["blue", "orange"],
             label=[f"Original (<{m})", "Modulo Reduced"], edgecolor="black")
    plt.legend()
    plt.xlabel(f"{function_name} hash values")
    plt.ylabel("frequency")
    plot_name = f"{data_name}_{function_name}_mod{m}.png"

    if not os.path.exists("histograms"):
        os.mkdir("histograms")
    plt.savefig(f"histograms/{plot_name}", bbox_inches='tight')
    plt.clf()


def correlation_plot(data, hash_function1, hash_function2, m, sample=1000, seed=0):
    """Returns a plot of a sample of modulo m reduced hash values of two hash functions for a given
    dataset 'data'. An input seed is given for reproducibility."""
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / data
    data_name = Path(data_path).stem
    with open(data_path, 'r') as file:
        data_list = file.read().splitlines()

    hash1_values = np.array([hash_function1(string) for string in data_list])
    hash1_values = [h % m for h in hash1_values]

    hash2_values = np.array([hash_function2(string) for string in data_list])
    hash2_values = [h % m for h in hash2_values]

    hash_df = pd.DataFrame({"hash1": hash1_values, "hash2": hash2_values})
    hash_df_sample = hash_df.sample(n=sample, random_state=seed)

    function1_name = hash_function1.__name__
    function2_name = hash_function2.__name__
    plt.scatter(hash_df_sample["hash1"], hash_df_sample["hash2"], alpha=0.5)
    plt.grid(True)
    plt.xlabel(f"{function1_name} hash values")
    plt.ylabel(f"{function2_name} hash values")
    plot_name = f"{data_name}_sample{sample}_{function1_name}_{function2_name}_mod{m}.png"
    if not os.path.exists("correlation_plots"):
        os.mkdir("correlation_plots")
    plt.savefig(f"correlation_plots/{plot_name}", bbox_inches='tight')
    plt.clf()

from pathlib import Path
from functools import partial
import numpy as np
import matplotlib.pyplot as plt


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


def distribution(data, hash_function, m):
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
    plt.hist([original, modulo_reduced], stacked=True,
             color=["blue", "orange"],
             label=[f"Original (<{m})", "Modulo Reduced"], edgecolor="black")
    plt.legend()
    plt.xlabel("Hash Values")
    plt.ylabel("Frequency")

    if isinstance(hash_function, partial):
        function_name = "mmh3"
    else:
        function_name = hash_function.__name__
    plot_name = f"{data_name}_{function_name}_mod{m}.png"
    plt.savefig(f"histograms/{plot_name}")
    plt.clf()

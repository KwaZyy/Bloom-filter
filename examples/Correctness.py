from pathlib import Path
import random
import sys

current_dir = Path(__file__).resolve().parent
project_dir = current_dir.parent
sys.path.append(str(project_dir))

from src.BloomFilter import KMBloomFilter
from src.HashingFunctions import sdbm, MurmurHash3


def correctness_test(dataset, empty_filter, n=1000, seed=0):
    """
    Tests the correctness of a Bloom filter.

    The test inserts n strings from the dataset into the Bloom filter.
    Then it searches for the same inserted strings again.

    A correct Bloom filter should return True for every inserted string.
    This checks that there are no false negatives.
    """

    current_dir = Path(__file__).parent
    data_path = current_dir.parent / "datasets" / dataset

    with open(data_path, "r") as file:
        data_list = file.read().splitlines()

    if n > len(data_list):
        raise ValueError("n must not be larger than the number of strings in the dataset.")

    random.seed(seed)
    selected_strings = data_list.copy()
    random.shuffle(selected_strings)
    inserted_strings = selected_strings[:n]

    empty_filter.add(inserted_strings)

    missed_strings = []

    for string in inserted_strings:
        if not empty_filter.search(string):
            missed_strings.append(string)

    if len(missed_strings) == 0:
        print(f"Correctness test passed for {dataset}: all {n} inserted strings were found.")
    else:
        print(f"Correctness test failed for {dataset}: {len(missed_strings)} inserted strings were not found.")


if __name__ == "__main__":
    correctness_test("words.txt", KMBloomFilter(200000, sdbm, MurmurHash3, 3), n=1000)
    correctness_test("DNA.txt", KMBloomFilter(800000, sdbm, MurmurHash3, 5), n=1000)
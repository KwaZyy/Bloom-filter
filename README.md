# Bloom-filter

## Team Members

- **Arnoud Vandevelde (KwaZyy)**
- **Atemefac Valery** 

## Contents of Repository

```text
Bloom-filter/
├── datasets/
│   ├── DNA.py
│   ├── DNA.txt
│   └── words.txt
├── examples/
│   ├── correlation_plots/
│   ├── false_positive_rate_plots/
│   ├── histograms/
│   ├── job_scripts/
│   ├── time_plots/
│   ├── AddingAndSearching.py
│   ├── CorrelationHashFunctions.py
│   ├── FalsePositiveRateIncreasingStrings.py
│   ├── HistogramHashFunctions.py
│   ├── OptimalAmountHashFunctions.py
│   └── TimeAddingSearching.py
│   ├── Correctness.py
├── src/
│   ├── __init__.py
│   ├── BloomFilter.py
│   ├── BloomFilterPlots.py
│   └── HashingFunctions.py
├── tests/
├── .gitignore
├── environment.yml
└── README.md
```
## File Descriptions

### `datasets/`

This folder contains the input datasets used in the examples.

- `words.txt`: dataset containing words used for testing the Bloom filter.
- `DNA.txt`: dataset containing DNA strings used for testing the Bloom filter.
- `DNA.py`: helper file related to DNA data generation or handling.

### `src/`

This folder contains the main implementation of the Bloom filter.

- `BloomFilter.py`: contains the core Bloom filter classes and the false positive rate calculation.
  `BloomFilterPlots.py`: contains helper functions for timing plots, false positive rate plots, and experiment visualisations.
- `HashingFunctions.py`: contains the hash functions used by the Bloom filter, such as `sdbm`, `djb2`, `lose_lose`, and `MurmurHash3`.

### `examples/`

This folder contains example scripts that demonstrate and test different parts of the project.

- `Correctness.py`: checks that every inserted string can be found again by the Bloom filter. This tests that there are no false negatives.
- `FalsePositiveRateIncreasingStrings.py`: studies how the false positive rate changes when more strings are inserted into the Bloom filter.
- `FalsePositiveRateIncreasingFilterSize.py`: studies how the false positive rate changes when the Bloom filter size increases.
- `OptimalAmountHashFunctions.py`: studies how the number of hash functions affects the false positive rate.
- `TimeAddingSearching.py`: compares the time needed for adding and searching strings.
- `CorrelationHashFunctions.py`: studies the relationship between pairs of hash functions.
- `HistogramHashFunctions.py`: creates histograms showing the distribution of hash values.

### `examples/false_positive_rate_plots/`

This folder contains plots related to false positive rate experiments.

### `examples/correlation_plots/`

This folder contains plots showing correlations between hash functions.

### `examples/histograms/`

This folder contains histogram plots for hash function outputs.

### `examples/time_plots/`

This folder contains plots related to timing experiments.

### `examples/job_scripts/`

This folder contains job scripts used to run some experiments.

### `tests/`

This folder is intended for test files.

### `environment.yml`

This file describes the Python/conda environment needed to run the project.

### `.gitignore`

This file tells Git which temporary files should not be tracked.

### `README.md`

This file explains the project structure and how the repository is organized.
environment.yml denotes the python environment the software was created in.


## Conclusion

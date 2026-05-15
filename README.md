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

## Running the Project

The project can be checked from the root folder of the repository.

To check that the Python files compile:

```powershell
python -m compileall src examples tests
```

To run the pytest test suite:

```powershell
pytest
```

The test suite checks the main Bloom filter behaviour, the hash functions, and the expected project files.

## Running Example Scripts

The example scripts are stored in the `examples/` folder. They should be run from the root folder of the repository.

For example:

```powershell
python examples/Correctness.py
python examples/AddingAndSearching.py
python examples/FalsePositiveRateIncreasingStrings.py
python examples/FalsePositiveRateIncreasingFilterSize.py
python examples/OptimalAmountHashFunctions.py
```

Some scripts create plots. These plots are saved in folders such as:

- `examples/false_positive_rate_plots/`
- `examples/correlation_plots/`
- `examples/histograms/`
- `examples/time_plots/`

## Job Scripts

The `examples/job_scripts/` folder contains job scripts which were used via VSC (Vlaams Supercomputer Centrum) to run certain python scripts which were time intensive.

## Conclusions

To conclude we showed that the djb2, sdbm and MurmurHash3 functions produce appropiate and uniform values after being modulo reduced by the Bloom filter size m, indicating that these hash functions are suitable for use in Bloom filters. These functions were also tested for correlation, for which there was no indication. Regarding time complexity, under fixed strings, we empirically checked that it was of the form O(k). For increasing string sizes we found a non-linear effect diverging from the theoretical O(l) time complexity. Space complexity is only dependent on the Bloom filter size m and thus was of the form O(m). For Bloom filter we have a theoretical false positive rate given by:  $\varepsilon \approx (1 - e^{\frac{-kn}{m}})^k$, this result was compared to an empirical false positive rate for varying n,m and k values which largely agreed with the theoretical result. For an increasing amount of strings the 'add' and 'search' functions were tested, showing a linear O(n) effect. For 'adding' we also saw an increase of time needed as compared against 'searching', which was to be expected because the searching procedure can stop before iterating over all of the hash  functions. 

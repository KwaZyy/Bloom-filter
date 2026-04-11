# Bloom Filter Project

This repository contains a small Python Bloom filter package, automated tests, and helper scripts for benchmarking and false-positive experiments.

## Project Layout

```text
bloom-filter-project/
|
+-- bloomfilter/
|   +-- __init__.py
|   +-- bloom.py
|
+-- tests/
|   +-- test_bloom.py
|
+-- scripts/
|   +-- benchmark.py
|   +-- false_positive_experiment.py
|
+-- hpc/
|   +-- benchmark_job.sh
|
+-- data/
|   +-- words.txt
|
+-- README.md
+-- requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Example

```python
from bloomfilter import BloomFilter, djb2, sdbm

bloom = BloomFilter(100, djb2, sdbm)
bloom.add("apple")

print(bloom.search("apple"))
print(bloom.search("pear"))
```

## Running Tests

```bash
python -m pytest tests -p no:cacheprovider
```

## Scripts

```bash
python scripts/benchmark.py --size 10000 --repeats 5
python scripts/false_positive_experiment.py --size 10000 --insert-count 20
```

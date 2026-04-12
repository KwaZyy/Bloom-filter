# Bloom Filter Project

This project is a small and beginner-friendly Bloom filter package in Python.

A Bloom filter is a fast tool for checking whether something is in a set.
It gives two kinds of answers:
- `False` means the item is definitely not present.
- `True` means the item may be present.

That makes Bloom filters useful for quick checks before slower work like database lookups.

## Quick Start

Install the dependency:

```bash
pip install -r requirements.txt
```

Use the package in Python:

```python
from bloomfilter import BloomFilter, DEFAULT_HASH_FUNCTIONS

bloom = BloomFilter(1000, *DEFAULT_HASH_FUNCTIONS)
bloom.add_all(["apple", "banana", "orange"])

print(bloom.search("apple"))
print(bloom.search("pear"))
```

## What This Repo Contains

```text
bloomfilter/   Python package code
tests/         automated tests
scripts/       helper scripts for benchmarks and experiments
data/          sample input data
hpc/           HPC job script
README.md      project overview
wiki/          beginner-friendly documentation
```

## Beginner Guide

If you want the easiest explanation, start here:

[Using The Bloom Filter](wiki/Using-The-Bloom-Filter.md)

Short version:
- Create a filter with `BloomFilter(size, *DEFAULT_HASH_FUNCTIONS)`.
- Add values with `add()` or `add_all()`.
- Check values with `search()`.
- `False` means definitely not present.
- `True` means maybe present.

## Run From The Command Line

You can also run the package directly:

```bash
python -m bloomfilter --size 100 --add apple banana --check apple pear
```

Example output:

```text
Bloom filter size: 100
Added values: 2
apple: maybe present
pear: definitely absent
```

## Run Tests

```bash
python -m pytest tests -p no:cacheprovider
```

## Helper Scripts

Benchmark the filter:

```bash
python scripts/benchmark.py --size 10000 --repeats 5
```

Run the false-positive experiment:

```bash
python scripts/false_positive_experiment.py --size 10000 --insert-count 20
```

## Notes For Beginners

- A larger Bloom filter usually gives fewer false positives.
- Bloom filters are memory-efficient, but they do not give perfect `True` answers.
- This project includes a package API, a small CLI, tests, and helper scripts so you can learn by trying each part.

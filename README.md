# Bloom Filter Project

This project is a small and beginner-friendly Bloom filter package in Python.

A Bloom filter is a fast tool for checking whether something is in a set.
It gives two kinds of answers:
- `False` means the item is definitely not present.
- `True` means the item may be present.

That makes Bloom filters useful for quick checks before slower work like database lookups.

## Team

Fill in these names before submission:
- Team member 1: `<add name>`
- Team member 2: `<add name>`

## Submission Summary

This repository contains our Bloom filter project for the course assignment.

The maintained implementation is the Python package in `bloomfilter/`.
An older duplicate implementation was removed from `src/` so the repository has one clear source of truth.

This project currently includes:
- a reusable Bloom filter package
- multiple hash functions
- automated tests
- a command-line entry point
- a benchmark script
- a false-positive experiment script
- an HPC batch job script
- beginner-friendly documentation

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
src/           note explaining the old duplicate code was removed
README.md      project overview
wiki/          beginner-friendly documentation
```

## Canonical Code Location

The code that should be read, tested, and graded is in:
- `bloomfilter/bloom.py`
- `bloomfilter/__init__.py`
- `bloomfilter/__main__.py`

This keeps the project structure clear and avoids having two different Bloom filter implementations in the same repository.

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

## Conda And HPC Use

This section is here to match the assignment requirements and can be expanded as you continue the project.

Example local workflow:

```bash
conda activate <your-environment-name>
python -m pytest tests -p no:cacheprovider
python scripts/benchmark.py --size 10000 --repeats 5
python scripts/false_positive_experiment.py --size 10000 --insert-count 20
```

Example HPC workflow:

```bash
sbatch hpc/benchmark_job.sh
```

Before submission, expand this section with:
- the exact conda environment name you used
- how packages were installed
- how the benchmark job was submitted on HPC
- where the benchmark output files were written

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

## Conclusions

This section should be completed near the end of the project.

Suggested points to include:
- whether the Bloom filter worked correctly in testing
- how performance changed as the number of inserted words increased
- how the false-positive rate changed as the filter became fuller
- what you learned from the benchmark and HPC runs

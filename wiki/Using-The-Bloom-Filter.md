# Using The Bloom Filter

This guide explains the Bloom Filter in very simple English.

## What This Project Does

A Bloom filter is a fast tool that checks if something is in a set.

It gives two kinds of answers:
- `definitely absent`
- `maybe present`

That means:
- If the filter says something is not there, you can trust that answer.
- If the filter says something may be there, it could be true, or it could be a false positive.

So this tool is good for quick checking, but not for final proof.

## A Simple Example

Imagine you want to track words you have already seen.

You add words like:
- `apple`
- `banana`
- `orange`

Later, you ask the filter about `apple`.
It will probably say `maybe present`.

If you ask about `pear`, it may say `definitely absent`.

## How To Use It In Python

Start with this:

```python
from bloomfilter import BloomFilter, DEFAULT_HASH_FUNCTIONS

bloom = BloomFilter(1000, *DEFAULT_HASH_FUNCTIONS)
```

This creates a Bloom filter with size `1000`.

The bigger the size, the more items it can handle before false positives become more common.

## Add Items

You can add one item at a time:

```python
bloom.add("apple")
bloom.add("banana")
```

You can also add many items at once:

```python
bloom.add_all(["apple", "banana", "orange"])
```

## Check Items

Use `search()` to check an item:

```python
print(bloom.search("apple"))
print(bloom.search("pear"))
```

What the result means:
- `False` means the item is definitely not in the filter.
- `True` means the item may be in the filter.

## Full Beginner Example

```python
from bloomfilter import BloomFilter, DEFAULT_HASH_FUNCTIONS

bloom = BloomFilter(1000, *DEFAULT_HASH_FUNCTIONS)
bloom.add_all(["apple", "banana", "orange"])

for item in ["apple", "pear", "banana", "mango"]:
    if bloom.search(item):
        print(f"{item}: maybe present")
    else:
        print(f"{item}: definitely absent")
```

This is a good starting example for a beginner.

## Use It From The Command Line

You can also run the package without writing a Python file:

```bash
python -m bloomfilter --size 100 --add apple banana --check apple pear
```

This command:
- makes a Bloom filter of size `100`
- adds `apple` and `banana`
- checks `apple` and `pear`

You may see output like this:

```text
Bloom filter size: 100
Added values: 2
apple: maybe present
pear: definitely absent
```

## Save And Load

You can save the filter to a file and load it later.

```python
from bloomfilter import BloomFilter, djb2, sdbm

bloom = BloomFilter(100, djb2, sdbm)
bloom.add("apple")
bloom.save("filter.pkl")

loaded = BloomFilter.load("filter.pkl", djb2, sdbm)
print(loaded.search("apple"))
```

Important:
Use the same hash functions when loading, so the results stay correct.

## When People Usually Use A Bloom Filter

People often use Bloom filters when they want to:
- check if an item was seen before
- avoid slow database lookups
- reduce memory use
- do quick pre-checks before more expensive work

## Things To Remember

- A Bloom filter is fast.
- A Bloom filter saves memory.
- `False` means definitely not present.
- `True` means maybe present.
- A smaller filter gives more false positives.
- A bigger filter is usually better for many items.

## Best Beginner Pattern

If you are new, use this pattern first:

```python
from bloomfilter import BloomFilter, DEFAULT_HASH_FUNCTIONS

bloom = BloomFilter(1000, *DEFAULT_HASH_FUNCTIONS)
bloom.add_all(["cat", "dog", "otter"])

print(bloom.search("cat"))
print(bloom.search("fox"))
```

That is the easiest way to start using this project.

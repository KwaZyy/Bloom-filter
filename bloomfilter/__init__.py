"""Package interface for the Bloom filter project."""

if __package__ in (None, ""):
    from bloom import (
        DEFAULT_HASH_FUNCTIONS,
        BloomFilter,
        HashFunction,
        djb2,
        make_hash_function,
        sdbm,
    )
else:
    from .bloom import (
        DEFAULT_HASH_FUNCTIONS,
        BloomFilter,
        HashFunction,
        djb2,
        make_hash_function,
        sdbm,
    )

__all__ = [
    "BloomFilter",
    "DEFAULT_HASH_FUNCTIONS",
    "HashFunction",
    "djb2",
    "make_hash_function",
    "sdbm",
]

#to be remove 25-4-2026
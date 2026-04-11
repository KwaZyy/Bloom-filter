"""Core Bloom filter implementation and helper hash functions."""

from __future__ import annotations

from pathlib import Path
import hashlib
import pickle
from typing import Callable, Iterable

HashFunction = Callable[[str], int]


def djb2(value: str) -> int:
    """Implementation of the djb2 hash function."""
    hashed = 5381
    for char in value:
        hashed = ((hashed << 5) + hashed) + ord(char)
    return hashed


def sdbm(value: str) -> int:
    """Implementation of the sdbm hash function."""
    hashed = 0
    for char in value:
        hashed = ord(char) + (hashed << 6) + (hashed << 16) - hashed
    return hashed


def make_hash_function(seed: int) -> HashFunction:
    """Create a deterministic hash function based on BLAKE2."""
    personalization = seed.to_bytes(4, "big", signed=False).ljust(16, b"\0")

    def _hash(value: str) -> int:
        digest = hashlib.blake2b(
            value.encode("utf-8"),
            digest_size=8,
            person=personalization,
        ).digest()
        return int.from_bytes(digest, "big")

    _hash.__name__ = f"blake2b_seed_{seed}"
    return _hash


DEFAULT_HASH_FUNCTIONS: tuple[HashFunction, ...] = (
    djb2,
    sdbm,
    make_hash_function(1),
)


class BloomFilter:
    """Bloom filter backed by a simple list-based bit array."""

    def __init__(self, m: int, *hash_functions: HashFunction) -> None:
        if m <= 0:
            raise ValueError("Bloom filter size must be positive.")

        self.m = m
        self.hash_functions: tuple[HashFunction, ...] = (
            hash_functions or DEFAULT_HASH_FUNCTIONS
        )
        self.filter = [0] * m

    def _indexes_for(self, value: str) -> list[int]:
        return [hash_function(value) % self.m for hash_function in self.hash_functions]

    def add(self, value: str) -> None:
        """Add a value to the Bloom filter."""
        for index in self._indexes_for(value):
            self.filter[index] = 1

    def add_all(self, values: Iterable[str]) -> None:
        """Add multiple values to the Bloom filter."""
        for value in values:
            self.add(value)

    def search(self, value: str) -> bool:
        """Return False if value is definitely absent, True if it may be present."""
        return all(self.filter[index] == 1 for index in self._indexes_for(value))

    def __contains__(self, value: str) -> bool:
        return self.search(value)

    def save(self, filepath: str | Path) -> None:
        """Persist the filter state to disk."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        state = {
            "m": self.m,
            "filter": self.filter,
        }
        with path.open("wb") as handle:
            pickle.dump(state, handle)

    @classmethod
    def load(
        cls,
        filepath: str | Path,
        *hash_functions: HashFunction,
    ) -> "BloomFilter":
        """Load a Bloom filter state from disk."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"No saved filter found at {path}")

        with path.open("rb") as handle:
            state = pickle.load(handle)

        instance = cls(state["m"], *(hash_functions or DEFAULT_HASH_FUNCTIONS))
        instance.filter = list(state["filter"])
        return instance

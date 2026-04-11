"""Command-line entry point for the bloomfilter package."""

from __future__ import annotations

import argparse
from typing import Sequence

from . import BloomFilter, DEFAULT_HASH_FUNCTIONS


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the package CLI."""
    parser = argparse.ArgumentParser(
        description="Create a Bloom filter, add values, and check membership.",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=100,
        help="Bloom filter size.",
    )
    parser.add_argument(
        "--add",
        nargs="*",
        default=[],
        metavar="VALUE",
        help="Values to add to the filter.",
    )
    parser.add_argument(
        "--check",
        nargs="*",
        default=[],
        metavar="VALUE",
        help="Values to query in the filter.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the package CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    bloom = BloomFilter(args.size, *DEFAULT_HASH_FUNCTIONS)
    bloom.add_all(args.add)

    print(f"Bloom filter size: {args.size}")
    print(f"Added values: {len(args.add)}")

    if not args.check:
        print("No membership checks requested.")
        return 0

    for value in args.check:
        result = "maybe present" if bloom.search(value) else "definitely absent"
        print(f"{value}: {result}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

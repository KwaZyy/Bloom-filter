from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bloomfilter import BloomFilter, DEFAULT_HASH_FUNCTIONS


def load_words(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def measure_false_positive_rate(size: int, inserted: list[str], probes: list[str]) -> float:
    bloom = BloomFilter(size, *DEFAULT_HASH_FUNCTIONS)
    bloom.add_all(inserted)

    false_positives = sum(1 for word in probes if bloom.search(word))
    return false_positives / len(probes) if probes else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate Bloom filter false positive rate.")
    parser.add_argument("--size", type=int, default=10_000, help="Bloom filter size.")
    parser.add_argument(
        "--words-file",
        type=Path,
        default=ROOT / "data" / "words.txt",
        help="Path to newline-delimited words.",
    )
    parser.add_argument(
        "--insert-count",
        type=int,
        default=20,
        help="Number of initial words inserted into the filter.",
    )
    args = parser.parse_args()

    words = load_words(args.words_file)
    inserted = words[: args.insert_count]
    probes = words[args.insert_count :]
    rate = measure_false_positive_rate(args.size, inserted, probes)

    print(f"Inserted words: {len(inserted)}")
    print(f"Probe words: {len(probes)}")
    print(f"Estimated false positive rate: {rate:.4%}")


if __name__ == "__main__":
    main()

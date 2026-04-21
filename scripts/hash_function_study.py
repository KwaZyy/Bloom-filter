from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bloomfilter import DEFAULT_HASH_FUNCTIONS, HashFunction


@dataclass(frozen=True)
class HashMetrics:
    dataset_name: str
    hash_name: str
    sample_count: int
    bucket_count: int
    occupied_buckets: int
    bucket_collisions: int
    max_bucket_load: int


def load_words(path: Path, limit: int | None = None) -> list[str]:
    words = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return words if limit is None else words[:limit]


def generate_dna_sequences(count: int, length: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    alphabet = "ACGT"
    return [
        "".join(rng.choice(alphabet) for _ in range(length))
        for _ in range(count)
    ]


def hash_name(hash_function: HashFunction) -> str:
    return getattr(hash_function, "__name__", hash_function.__class__.__name__)


def analyze_hash_distribution(
    values: list[str],
    hash_function: HashFunction,
    bucket_count: int,
    dataset_name: str,
) -> HashMetrics:
    bucket_usage = Counter(hash_function(value) % bucket_count for value in values)
    occupied_buckets = len(bucket_usage)
    bucket_collisions = sum(count - 1 for count in bucket_usage.values() if count > 1)
    max_bucket_load = max(bucket_usage.values(), default=0)
    return HashMetrics(
        dataset_name=dataset_name,
        hash_name=hash_name(hash_function),
        sample_count=len(values),
        bucket_count=bucket_count,
        occupied_buckets=occupied_buckets,
        bucket_collisions=bucket_collisions,
        max_bucket_load=max_bucket_load,
    )


def print_report(metrics: list[HashMetrics]) -> None:
    print("Hash function study")
    print("===================")
    for entry in metrics:
        print(f"Dataset: {entry.dataset_name}")
        print(f"Hash function: {entry.hash_name}")
        print(f"Samples: {entry.sample_count}")
        print(f"Buckets: {entry.bucket_count}")
        print(f"Occupied buckets: {entry.occupied_buckets}")
        print(f"Bucket collisions: {entry.bucket_collisions}")
        print(f"Max bucket load: {entry.max_bucket_load}")
        print("")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Study hash-function bucket usage on words and DNA-like strings.",
    )
    parser.add_argument(
        "--words-file",
        type=Path,
        default=ROOT / "data" / "words.txt",
        help="Path to newline-delimited words.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=100,
        help="Number of values to analyze per dataset.",
    )
    parser.add_argument(
        "--bucket-count",
        type=int,
        default=257,
        help="Number of buckets used when comparing hash distributions.",
    )
    parser.add_argument(
        "--dna-length",
        type=int,
        default=12,
        help="Length of each generated DNA string.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed used for generated DNA strings.",
    )
    args = parser.parse_args()

    words = load_words(args.words_file, args.sample_size)
    dna = generate_dna_sequences(args.sample_size, args.dna_length, args.seed)

    metrics: list[HashMetrics] = []
    for hash_function in DEFAULT_HASH_FUNCTIONS:
        metrics.append(
            analyze_hash_distribution(words, hash_function, args.bucket_count, "words"),
        )
        metrics.append(
            analyze_hash_distribution(dna, hash_function, args.bucket_count, "dna"),
        )

    print_report(metrics)


if __name__ == "__main__":
    main()

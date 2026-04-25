from __future__ import annotations

import argparse
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bloomfilter import BloomFilter, DEFAULT_HASH_FUNCTIONS


def load_words(path: Path, limit: int | None = None) -> list[str]:
    words = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return words if limit is None else words[:limit]


def run_benchmark(size: int, words: list[str], repeats: int) -> tuple[float, float]:
    add_timings: list[float] = []
    search_timings: list[float] = []

    for _ in range(repeats):
        bloom = BloomFilter(size, *DEFAULT_HASH_FUNCTIONS)

        start = time.perf_counter()
        bloom.add_all(words)
        add_timings.append(time.perf_counter() - start)

        start = time.perf_counter()
        for word in words:
            bloom.search(word)
        search_timings.append(time.perf_counter() - start)

    return sum(add_timings) / repeats, sum(search_timings) / repeats


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark Bloom filter operations.")
    parser.add_argument("--size", type=int, default=10_000, help="Bloom filter size.")
    parser.add_argument("--repeats", type=int, default=5, help="Number of benchmark repetitions.")
    parser.add_argument(
        "--words-file",
        type=Path,
        default=ROOT / "data" / "words.txt",
        help="Path to newline-delimited words.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Optional number of words to use.")
    args = parser.parse_args()

    words = load_words(args.words_file, args.limit)
    add_average, search_average = run_benchmark(args.size, words, args.repeats)

    print(f"Words loaded: {len(words)}")
    print(f"Filter size: {args.size}")
    print(f"Average add time: {add_average:.6f}s")
    print(f"Average search time: {search_average:.6f}s")


if __name__ == "__main__":
    main()


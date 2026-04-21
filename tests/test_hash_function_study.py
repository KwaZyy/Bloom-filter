from pathlib import Path
from unittest.mock import patch

from scripts.hash_function_study import (
    analyze_hash_distribution,
    generate_dna_sequences,
    load_words,
)


def test_generate_dna_sequences_is_reproducible() -> None:
    first = generate_dna_sequences(4, 6, seed=7)
    second = generate_dna_sequences(4, 6, seed=7)

    assert first == second
    assert all(set(sequence) <= set("ACGT") for sequence in first)


def test_analyze_hash_distribution_counts_bucket_collisions() -> None:
    def simple_hash(value: str) -> int:
        return len(value)

    metrics = analyze_hash_distribution(
        ["a", "b", "cc"],
        simple_hash,
        bucket_count=5,
        dataset_name="toy",
    )

    assert metrics.dataset_name == "toy"
    assert metrics.sample_count == 3
    assert metrics.occupied_buckets == 2
    assert metrics.bucket_collisions == 1
    assert metrics.max_bucket_load == 2


def test_load_words_respects_limit() -> None:
    with patch(
        "pathlib.Path.read_text",
        return_value="apple\nbanana\ncarrot\n",
    ):
        assert load_words(Path("ignored.txt"), limit=2) == [
            "apple",
            "banana",
        ]

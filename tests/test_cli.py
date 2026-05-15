from pathlib import Path


def test_main_project_files_exist():
    assert Path("src/BloomFilter.py").exists()
    assert Path("src/BloomFilterPlots.py").exists()
    assert Path("src/HashingFunctions.py").exists()


def test_example_files_exist():
    assert Path("examples/Correctness.py").exists()
    assert Path("examples/AddingAndSearching.py").exists()
    assert Path("examples/CorrelationHashFunctions.py").exists()
    assert Path("examples/HistogramHashFunctions.py").exists()


def test_removed_scripts_folder_is_not_used():
    assert not Path("scripts/benchmark.py").exists()

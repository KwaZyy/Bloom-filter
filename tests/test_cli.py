from bloomfilter.__main__ import main


def test_module_cli_reports_membership(capsys) -> None:
    exit_code = main(["--size", "20", "--add", "apple", "banana", "--check", "apple", "pear"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Bloom filter size: 20" in captured.out
    assert "Added values: 2" in captured.out
    assert "apple: maybe present" in captured.out
    assert "pear: definitely absent" in captured.out

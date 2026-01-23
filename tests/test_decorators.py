import re

import pytest

from src.decorators import log


def test_log(capsys):
    @log()
    def func_for_log(x, y, z):
        print("Doing some stuff")
        return x * y * z

    result = func_for_log(1, 2, 3)
    captured = capsys.readouterr()
    assert result == 6
    expected = "Starting function func_for_log\n" "Doing some stuff\n" "Function result: 6\n" "Finishing...\n"
    assert re.search(r"Elapsed time \d+\.\d+", captured.out)
    assert expected in captured.out


def test_log_with_file(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(str(log_file))
    def func_for_log_with_file(x, y, z):
        print("Doing some stuff")
        return x * y * z

    result = func_for_log_with_file(1, 2, 3)
    assert result == 6
    assert log_file.exists()
    content = log_file.read_text()
    assert (
        "Starting function func_for_log_with_file\n" "Doing some stuff\n" "Function result: 6\n" "Finishing...\n"
    ) in content
    assert re.search(r"Elapsed time \d+\.\d+", content)


def test_log_bad(capsys):
    @log()
    def bad(x, y, z):
        print("Doing some stuff")
        raise ValueError

    with pytest.raises(ValueError):
        bad(1, 2, 3)
    captured = capsys.readouterr()
    expected = (
        "Starting function bad\n"
        "Doing some stuff\n"
        "Errors occurred, when execution: \n"
        "Args: [1, 2, 3], kwargs: []\n"
    )
    assert captured.out == expected


def test_log_bad_with_file(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(str(log_file))
    def bad(x, y, z):
        print("Doing some stuff")
        raise ValueError

    with pytest.raises(ValueError):
        bad(1, 2, 3)
    expected = (
        "Starting function bad\n"
        "Doing some stuff\n"
        "Errors occurred, when execution: \n"
        "Args: [1, 2, 3], kwargs: []\n"
    )
    assert log_file.exists()
    content = log_file.read_text()
    assert expected in content

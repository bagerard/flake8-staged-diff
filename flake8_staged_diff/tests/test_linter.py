from flake8_staged_diff.linter import run_dummy_check


def test_run_dummy_check():
    assert run_dummy_check() == (None, None)

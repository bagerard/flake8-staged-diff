import sys
import subprocess
from typing import Set, List


def find_between(text, left, right):
    left_index = text.index(left)
    return text[left_index + len(left) : text.index(right, left_index + len(left))]


def git_diff_upsert_lines(git_diff_output: str) -> Set[str]:
    """Extract the modified file and lines from the output of `git diff --staged`
    And return them in a format that is easily comparable with flake8's output

    Typically "/file/path:line:" as flake8's finding are reported as e.g
    src/module.py:281:70: ANN205 Missing return type annotation for staticmethod

    Inspired by https://stackoverflow.com/questions/8259851/using-git-diff-how-can-i-get-added-and-modified-lines-numbers
    """
    n_line = None
    path = None
    upserted_lines: Set[str] = set()
    for line in git_diff_output.split("\n"):
        if line.startswith("--- a/"):
            continue
        elif line.startswith("+++ b/"):
            path = line.replace("+++ b/", "")
        elif line.startswith("@@"):
            # e.g @@ -26 +26,2 @@ class DatabaseManager(SynchronousWorker, DatabaseManagerInterface):
            n_line_str = find_between(line, "+", "@@")
            n_line = int(float(n_line_str.replace(",", ".")))
        elif line.startswith("+"):
            upserted_lines.add(f"{path}:{n_line}:")
            n_line += 1
    return upserted_lines


def get_diff_staged():
    cmd_out = subprocess.run(
        ("git", "diff", "-U0", "--staged", "--"),
        stdout=subprocess.PIPE,
    )
    if cmd_out.returncode != 0:
        raise Exception(
            f"git diff failed: {cmd_out.stderr.decode() if cmd_out.stderr else cmd_out.stdout.decode()}"
        )
    return cmd_out.stdout.decode()


def run_flake8(args: List[str]) -> str:
    cmd_out = subprocess.run(
        ("flake8", *args),
        stdout=subprocess.PIPE,
    )
    if cmd_out.stderr:
        raise Exception(f"Flake8 run failed: {cmd_out.stderr}")
    return cmd_out.stdout.decode()


def main() -> int:
    files_and_args: List[str] = sys.argv[1:]
    git_diff = get_diff_staged()
    diff_upsert_lines = git_diff_upsert_lines(git_diff)

    if not diff_upsert_lines:
        print("No diff - Skip flake8 call")
        return 0

    flake8_output = run_flake8(files_and_args)
    flake8_upsert_matches = []
    for flake8_finding in flake8_output.split("\n"):
        if any(l in flake8_finding for l in diff_upsert_lines):
            flake8_upsert_matches.append(flake8_finding)

    for finding in flake8_upsert_matches:
        print(finding)

    return 1 if flake8_upsert_matches else 0


if __name__ == "__main__":
    exit(main())

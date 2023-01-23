# flake8-staged-diff

Run flake8 but report the findings only on staged files (identified with `git diff --staged`)
This tool is primarily meant to be integrated through [pre-commit](https://pre-commit.com/) but it also offers a CLI.

## How it works?

This tool runs first `git diff -U0 --staged --` and identify the files and lines that were modified,
it then runs flake8 on the entire files and simply filters out all the findings that are not coming
from the modified code.

If no files is staged in git, it will return immediately

## Pre-commit integration

An example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bagerard/flake8-staged-diff
    rev: ''  # Use the sha / tag you want to point at
    hooks:
      - id: flake8-staged-diff
```

> **_NOTE:_**  This will only affect local usage of pre-commit, typically through `git commit`
> When it runs for instance in a Github pipeline through `pre-commit run -a`, there will be **no staged files**
> and the tool will simply pass.

## CLI Usage

Interface is the same as flake8, e.g.

    flake8-staged-diff file1.py file2.py --select=E501

## Rationale

This tool allows to introduce some flake8 rules in large/legacy codebases only on the code that is updated or inserted. 

We use this at work for enforcing type annotations on modified code using the following config

```yaml
  - repo: https://github.com/bagerard/flake8-staged-diff
    rev: ''  # Use the sha / tag you want to point at
    hooks:
      - id: flake8-staged-diff
        args:
          - "--select=AN"
        additional_dependencies:
          - flake8-annotations
```
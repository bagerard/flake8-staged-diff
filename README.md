# flake8-staged-diff

Run flake8 but report the findings only on staged files (identified with `git diff --staged`)

## Rationale

This allows to introduce some flake8 rules in large/legacy codebases only on the code that is updated or inserted. 

## CLI Usage

    gitlabci-jsonschema-lint ../some_projects/.gitlab-ci.yml


## Pre-commit integration

An example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/bagerard/flake8-staged-diff
    rev: master
    hooks:
      - id: flake8-staged-diff
```


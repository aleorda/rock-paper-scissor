# rock-paper-scissor

## Pre Commit

Use [pre-commit](https://pre-commit.com/) to run and validate your changes before a commit.

pre-commit is configured to run:

- `safety`: dependencies security checks
- `black`: check formatting

To install pre-commit use:

On macOS:
```
brew install pre-commit
```

On Linux:
```
pip install pre-commit
```

To install the pre-commit hooks, run:
```
pre-commit install
```
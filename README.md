# rock-paper-scissor

## Description

This is a simple rock-paper-scissor game.

It has 2 different modes:
* Classic mode: you play against the computer with the classic rules:
  * Rock crushes Scissors (✊ > ✌)
  * Scissors cuts Paper (✌ > ✋)
  * Paper covers Rock (✋ > ✊)


* Extended mode: you play against the computer with the extended rules:
  * Scissors cuts Paper (✌ > ✋)
  * Paper covers Rock (✋ > ✊)
  * Rock crushes Lizard (✊ > 🦎)
  * Lizard poisons Spock (🦎 > 🖖)
  * Spock smashes Scissors (🖖 > ✌)
  * Scissors decapitates Lizard (✌ > 🦎)
  * Lizard eats Paper (🦎 > ✋)
  * Paper disproves Spock (✋ > 🖖)
  * Spock vaporizes Rock (🖖 > ✊)
  * Rock crushes Scissors (✊ > ✌)

## Installation

### Requirements

- Python 3.10
- Poetry
- Docker
- Docker Compose

### Setup - without Docker

To install the dependencies, run:
```
poetry install
```

Collect static files:
```
poetry run python app/manage.py collectstatic
```

To run the application, execute:
```
poetry run python app/manage.py runserver 8000
```

### Setup - with Docker

To run the application, execute:
```
docker compose build
docker compose up -d --remove-orphans
```

To stop the application, execute:
```
docker compose down
```

### Setup - with Makefile

To start the application, execute:
```
make start
```

To stop the application, execute:
```
make stop
```

## Tests

### Unit tests

To run the unit tests with coverage, execute:
```
poetry run coverage run -m pytest
poetry run coverage report
```
or
```
make coverage
```

For a more detailed report, run:
```
poetry run coverage html
```
and open the `htmlcov/index.html` file in your browser, or
```
make coverage
```


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
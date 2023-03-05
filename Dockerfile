ARG python_version=3.10
ARG poetry_version=1.4.0

FROM acidrain/python-poetry:${python_version}-alpine-${poetry_version}

COPY poetry.lock pyproject.toml ./

WORKDIR $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install --no-dev --no-interaction --no-ansi

USER nobody

# will become mountpoint of our code
WORKDIR /app

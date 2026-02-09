# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    WORKSPACE_ROOT=/app/

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    portaudio19-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry using pip and clear cache
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN poetry config installer.max-workers 20

# work directory
WORKDIR $WORKSPACE_ROOT

# copy project requirement files
COPY poetry.lock pyproject.toml $WORKSPACE_ROOT

# Install the dependencies and clear cache
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-cache && \
    rm -rf ~/.cache/pypoetry/cache/ && \
    rm -rf ~/.cache/pypoetry/artifacts/

# Copy the rest of the application
COPY . $WORKSPACE_ROOT

# Run the application
CMD ["python", "main.py"]

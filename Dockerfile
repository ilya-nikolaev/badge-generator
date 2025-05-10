FROM python:3.12-slim-bookworm AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    APP_PATH="/app"

ENV VIRTUAL_ENV="$APP_PATH/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR $APP_PATH


FROM python-base AS builder

RUN apt update \
    && apt install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/

COPY --from=ghcr.io/astral-sh/uv:0.6.17 /uv /uvx /bin/

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --all-extras --no-install-project

COPY ./src ./src
RUN uv sync --all-extras --no-editable


FROM python-base AS runner

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

CMD ["uvicorn", "badge_gen.main.entrypoint:app", "--host", "0.0.0.0", "--port", "80"]

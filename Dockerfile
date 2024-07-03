FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app
COPY . .

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash
RUN rye sync --no-dev --no-lock
RUN . .venv/bin/activate

CMD ["rye", "run", "server"]

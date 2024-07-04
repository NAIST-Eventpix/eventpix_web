FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl

WORKDIR /app
COPY . .

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash
RUN rye sync --no-lock

ARG GOOGLE_APPLICATION_CREDENTIALS=google_app.json
RUN echo $GOOGLE_APPLICATION_CREDENTIALS_DATA > $GOOGLE_APPLICATION_CREDENTIALS
RUN echo "GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS" > .env
RUN echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env

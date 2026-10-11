FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

ENV UV_TOOL_BIN_DIR=/usr/local/bin

RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN uv tool install rust-just==1.54.0 \
    && just --version

WORKDIR /workspace

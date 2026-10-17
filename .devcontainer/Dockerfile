FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

ENV UV_TOOL_BIN_DIR=/usr/local/bin

RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd \
    --uid ${USER_UID} \
    --gid ${USER_GID} \
    --create-home \
    --shell /bin/bash \
    ${USERNAME}

# Shared just installation
ENV UV_TOOL_DIR=/opt/uv-tools
ENV UV_TOOL_BIN_DIR=/usr/local/bin

RUN mkdir -p /opt/uv-tools \
    && uv tool install rust-just==1.54.0 \
    && /usr/local/bin/just --version \
    && chmod -R a+rX /opt/uv-tools

ENV UV_CACHE_DIR=/home/${USERNAME}/.cache/uv

WORKDIR /workspace

USER ${USERNAME}

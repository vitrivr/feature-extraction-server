FROM python:3.11.4-slim-bullseye

ARG PLUGINPATH
ARG CMD_ENTRYPOINT

# Set environment variables
ENV PATH=/root/.local/bin:$PATH \
    FLIT_ROOT_INSTALL=1 

# Set the working directory in the container to /app
WORKDIR /app


COPY src/ ./src/

RUN apt-get update; \
    pip install flit; \
    chmod -R 755 ./src/;

# Use Bash to handle the complex command
SHELL ["/bin/bash", "-c"]

RUN for subdir in ./src/*; do \
        plugin=$(basename "$subdir"); \
        if echo ":$PLUGINPATH:" | grep -q ":$plugin:" && [ -d "$subdir" ] && [ -e "$subdir/pyproject.toml" ]; then \
            cd "$subdir"; \
            if [ -e "install_system_dependencies.sh" ]; then \
                chmod +x "install_system_dependencies.sh"; \
                ./install_system_dependencies.sh; \
            fi; \
            flit install; \
            cd -; \
        else \
            rm -rf "$subdir"; \
        fi; \
    done

SHELL ["/bin/sh", "-c"]


RUN rm -rf ./src; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/* 

EXPOSE 8888

ENV CMD_ENTRYPOINT=${CMD_ENTRYPOINT}

COPY .env ./

CMD ${CMD_ENTRYPOINT}
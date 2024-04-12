ARG ARCH
FROM ${ARCH}python:3.11.4-slim-bullseye

ARG PLUGINPATH

# Set environment variables
ENV PATH=/root/.local/bin:$PATH \
    FLIT_ROOT_INSTALL=1 

# Set the working directory in the container to /app
WORKDIR /app

# Update package lists
RUN apt-get update

# Install flit
RUN pip install flit


# Split the PLUGINPATH on ':' to handle multiple paths
COPY plugins/ ./plugins/
COPY core/ ./core/


RUN chmod -R 755 ./plugins/ \
    && chmod -R 755 ./core/

# install core
RUN cd core \
    && chmod +x ./install_system_dependencies.sh \
    && ./install_system_dependencies.sh \
    && flit install

# Use Bash to handle the complex command
SHELL ["/bin/bash", "-c"]

RUN for subdir in ./plugins/*; do \
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



# Cleanup in the same layer to reduce image size
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

EXPOSE 8888

CMD uvicorn feature_extraction_server.services.fast_api_app:create_app --port 8888 --host 0.0.0.0

# endless loop

# CMD ["tail", "-f", "/dev/null"]
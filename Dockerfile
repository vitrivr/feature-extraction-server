# Use an official Python runtime as a parent image
FROM python:3.11.4-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    NUMBER_OF_WORKERS=1 \
    PATH=/root/.local/bin:$PATH \
    FLIT_ROOT_INSTALL=1 

# Set the working directory in the container to /app
WORKDIR /app

# Update package lists
RUN apt-get update

# Add the current directory contents into the container at /app
COPY feature_extraction_server-core/ ./feature_extraction_server-core/
COPY plugins_to_install/ ./plugins/


# Install flit
RUN pip install flit \
    && pip install gunicorn



RUN chmod -R 755 ./plugins
COPY gunicorn.conf.py /app/

# Install the plugins during image building
RUN for plugin in ./plugins/*; do \
    if [ -d "$plugin" ] && [ -e "$plugin/pyproject.toml" ]; then \
        cd "$plugin"; \
        if [ -e "install_system_dependencies.sh" ]; then \
            chmod +x "install_system_dependencies.sh"; \
            ./install_system_dependencies.sh; \
        fi; \
        flit install; \
        cd -; \
    fi; \
done

# # Install system dependencies required for flit and others for the core
RUN cd feature_extraction_server-core \
    && chmod +x ./install_system_dependencies.sh \
    && ./install_system_dependencies.sh

RUN cd feature_extraction_server-core && flit install

# Cleanup in the same layer to reduce image size
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* 




# Make port 5000 available to the world outside this container
EXPOSE 5000


CMD gunicorn -w ${NUMBER_OF_WORKERS} -b :5000 --timeout 600 --preload 'feature_extraction_server.flask.entrypoint:entrypoint()'
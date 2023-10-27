# Use an official Python runtime as a parent image
FROM python:3.11.5-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    WORKERS=1 \
    PATH=/root/.local/bin:$PATH \
    FLIT_ROOT_INSTALL=1 

# Set the working directory in the container to /app
WORKDIR /app

# Update package lists
RUN apt-get update

# Add the current directory contents into the container at /app
COPY feature_extraction_server-core/ ./feature_extraction_server-core/

# # Install system dependencies required for flit and others for the core
# RUN cd feature_extraction_server-core \
#     && chmod +x ./install_system_dependencies.sh \
#     && ./install_system_dependencies.sh 

# Cleanup in the same layer to reduce image size
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Install flit
RUN pip install flit \
    && pip install gunicorn

# Install Python dependencies (assuming you have a pyproject.toml in the feature_extraction_server-core directory)
# RUN cd feature_extraction_server-core \
#     && flit install

# Set up the plugins directory and copy the entrypoint script
RUN mkdir -p /plugins && chmod -R 755 /plugins
COPY entrypoint.sh /app/
COPY gunicorn.conf.py /app/
RUN chmod +x /app/entrypoint.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["./entrypoint.sh"]



# Run the command to start the server when the container launches
#CMD gunicorn -w ${WORKERS} -b :5000 --timeout 600 --preload 'feature_extraction_server.flask.entrypoint:entrypoint()'

# CMD gunicorn -w ${WORKERS} -b :5000 --timeout 600 --preload -c feature_extraction_server/gunicorn_hooks.py 'feature_extraction_server.app:entrypoint()'
# CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "5000"]
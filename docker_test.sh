#!/bin/bash

# Exit script if any command fails
set -e

cleanup() {
    if [ -n "$CONTAINER_ID" ]; then
        echo "Stopping container..."
        docker stop $CONTAINER_ID
        # docker rm $CONTAINER_ID
    fi
    # Kill background memory monitoring process if running
    if [ -n "$MONITOR_PID" ]; then
        kill $MONITOR_PID
    fi
}

# Function to monitor memory usage of the container in the background
monitor_memory() {
    while true; do
        docker stats --no-stream --format "Memory usage: {{.MemUsage}}" $CONTAINER_ID | tee -a memory_usage.log
        sleep 5
    done
}

# This trap will call the cleanup function if the script exits for any reason (including errors)
trap cleanup EXIT

# Variables
IMAGE_NAME="featureextractionserver"

# Step 1: Build the Docker image
docker build -t $IMAGE_NAME .

# Step 2: Run the server in the background and capture the container ID
CONTAINER_ID=$(docker run -it -e WORKERS=5 -e LOG_LEVEL=DEBUG -p 5000:5000 -v ~/.cache:/root/.cache -v $(pwd)/test:/app/test -d $IMAGE_NAME)

# Start the memory monitor in the background
monitor_memory & 
MONITOR_PID=$!

# Give the server some time to start up
sleep 10

# Step 3: Execute the tests on the running container
# You might need to adjust the path based on where your tests are located within the Docker image
docker exec $CONTAINER_ID pytest ./test -o log_cli=true

echo "Tests completed successfully!"

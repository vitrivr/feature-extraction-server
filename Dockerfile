# Use an official Python runtime as a parent image
FROM python:3.11.4-bookworm

# Set the working directory in the container to /app
WORKDIR /feature_extraction_server

# Add the current directory contents into the container at /app
ADD feature_extraction_server/ /feature_extraction_server
ADD requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

# Install libsndfile library
RUN apt-get update && apt-get install -y libsndfile1

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set default value for WORKERS environment variable
ENV WORKERS=1

# Run the command to start the server when the container launches
CMD gunicorn -w ${WORKERS} -b :5000 --timeout 600 app:application

# CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "5000"]
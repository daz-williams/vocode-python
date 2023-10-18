# Use an official Python runtime as a base image
FROM python:3.10-slim-buster

# Install make
RUN apt-get update && apt-get install -y make ffmpeg

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Run make commands
RUN make lint
RUN make typecheck

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run application. Adjust this based on your Makefile
CMD ["make", "chat"]
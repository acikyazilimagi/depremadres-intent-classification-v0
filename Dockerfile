# Use an official Python runtime as the base image
FROM python:3.9-buster

# Set the working directory to /app
WORKDIR /app

# Install required packages
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install --upgrade-strategy=only-if-needed -r requirements.txt

# Set the environment variable for FastAPI
ENV PYTHONUNBUFFERED 1

# Expose port 8000 for incoming traffic
EXPOSE 8000

# Copy the current directory contents into the container at /app
# This should be at the end of Dockerfile to utilize layer caching
COPY . /app

# Run the command to start the FastAPI server
CMD [ "python3", "src/app_main.py" ]


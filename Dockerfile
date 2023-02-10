# Use an official Python runtime as the base image
FROM python:3.9-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN pip3 install --upgrade pip
RUN pip3 install --extra-index-url https://alpine-wheels.github.io/index numpy
RUN pip3 install -r requirements.txt

# Set the environment variable for FastAPI
ENV PYTHONUNBUFFERED 1

# Run the command to start the FastAPI server
CMD [ "python", "intent-classification-v0/app_main.py" ] 

# Expose port 8000 for incoming traffic
EXPOSE 8000

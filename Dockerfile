FROM python:3.9-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Add project root to PYTHONPATH
ENV PYTHONPATH=/app/grabber_backend/:$PYTHONPATH

# Install OS dependencies
RUN apt-get update && apt-get install make vim -y

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

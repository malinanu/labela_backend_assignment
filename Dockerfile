# Use an official Python runtime as a parent image
FROM python:3.11

# Metadata indicating an image maintainer
LABEL author='Label A'

# Set the working directory in the container
WORKDIR /app

# Install dependencies required for psycopg2-binary
# Combine apt-get update with apt-get install and clean up in one layer to reduce image size
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt psycopg2-binary flake8==3.8.4 uWSGI

# Copy the current directory contents into the container at /app
COPY . /app

# Set environment variables
ENV WORKERS=2 \
    PORT=80 \
    PYTHONUNBUFFERED=1 \
    POSTGRES_USER=myuser \
    POSTGRES_PASSWORD=mypassword \
    POSTGRES_DB=mydb

# Expose the port the app runs on
EXPOSE ${PORT}

# Define volume for PostgreSQL data
VOLUME /var/lib/postgresql/data

# Use the official PostgreSQL image for the database service
# Note: This should be defined in a docker-compose.yml file, not here

# Start command to run the app
# Note: Starting PostgreSQL should be handled by its own container
CMD ["sh", "-c", "uwsgi --http :${PORT} --processes ${WORKERS} --static-map /static=/static --module autocompany.wsgi:application"]

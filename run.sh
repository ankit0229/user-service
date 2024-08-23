#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

echo "Building the Docker images..."
docker-compose build --no-cache

echo "Starting the containers..."
docker-compose up -d

echo "Waiting for the database to be ready..."
# Wait loop to ensure the database is ready before applying migrations
until docker-compose exec db pg_isready --timeout=0 --dbname=user_db
do
  echo "Waiting for the database to become available..."
  sleep 2
done

echo "Database is ready."
echo "Applying database migrations..."
docker-compose exec web alembic upgrade head

echo "The application is running at http://localhost:8000"
echo "Tailing the logs. Press CTRL+C to stop."
docker-compose logs -f

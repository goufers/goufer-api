# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for mysqlclient, psycopg2, and other packages
RUN apt-get update && \
    apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libpq-dev \
    pkg-config \
    curl \
    && apt-get clean

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=goufer.settings.dev
ENV PORT 8080

# Create a non-root user and group, and switch to it
RUN addgroup --system app && adduser --system --ingroup app app

# Change ownership of the app directory to the app user and group
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8080

# Health check for MySQL
HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD mysqladmin ping -h db_host || exit 1


# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "goufer.wsgi:application"]

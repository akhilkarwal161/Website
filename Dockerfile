# Use a specific Python 3.13 slim image for consistency and smaller size
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install SQLite3 and clean apt cache
RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set Django settings module and Python unbuffered output
ENV DJANGO_SETTINGS_MODULE=mainweb.settings
ENV PYTHONUNBUFFERED=1

# Run Django database migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port for the application
EXPOSE 8080

# Run Gunicorn to serve the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "mainweb.wsgi:application"]

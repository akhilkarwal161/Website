# Use a specific Python 3.13 slim image for consistency and smaller size
FROM python:3.13

# Update packages to patch potential vulnerabilities and then clean up
RUN apt-get update && apt-get upgrade -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code, including db.sqlite3, into the container
COPY . .

# Set Django settings module and Python unbuffered output
ENV DJANGO_SETTINGS_MODULE=mainweb.settings
ENV PYTHONUNBUFFERED=1

# Ensure the database file exists and migrations are applied
# The migrate command will use the db.sqlite3 file that was copied in
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port for the application
EXPOSE 8080

# Run Gunicorn to serve the Django application
# Gunicorn will now use the pre-migrated db.sqlite3 file that has your data
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "mainweb.wsgi:application"]

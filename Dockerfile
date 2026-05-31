# Use a specific Python alpine image for a small footprint
FROM python:alpine

# Update packages to patch potential vulnerabilities and then clean up
RUN apk update && apk upgrade && \
    rm -rf /var/cache/apk/*

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
# Set DJANGO_DEBUG to 'False' for production. This enables security features
# and optimizations like PREPEND_WWW.
ENV DJANGO_DEBUG=False

# Collect static files
RUN python manage.py collectstatic --noinput && python manage.py compress

# Expose the port for the application
EXPOSE 8080

# Run Gunicorn to serve the Django application, running migrations and cache table setup on startup
CMD ["sh", "-c", "python manage.py migrate && python manage.py createcachetable && gunicorn --bind 0.0.0.0:8080 --workers 3 --threads 2 --timeout 60 mainweb.wsgi:application"]

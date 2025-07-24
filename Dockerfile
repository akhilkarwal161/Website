# Use an official Python runtime as a parent image
# Using python 3.13 slim version for consistency with local environment and smaller image size
FROM python:3.13
# Changed to Python 3.13version

# Set the working directory inside the container
# All subsequent commands will run relative to this directory
WORKDIR /app

# Install system dependencies if your project needs any.
# For a basic Django app with SQLite, usually none are strictly required.
# If you later switch to PostgreSQL, you might need:
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

# Install a newer version of SQLite3, as Django 5.x requires 3.31 or later.
# This step is still necessary as the default SQLite in slim images might be older.
#RUN apt-get update && apt-get install -y --no-install-recommends \
    #sqlite3 \
    #&& rm -rf /var/lib/apt/lists/* 
    # Clean up apt cache to keep image size small

# Copy the requirements file first to leverage Docker's build cache.
# If requirements.txt doesn't change, this step won't re-run.
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# --no-cache-dir: Prevents pip from storing downloaded packages, reducing image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container's working directory.
# The .dockerignore file (created next) will prevent unnecessary files from being copied.
COPY . .

# Set environment variables for Django
# DJANGO_SETTINGS_MODULE: Tells Django where to find your settings file.
# PYTHONUNBUFFERED: Ensures Python output is sent directly to the console, useful for logging.
ENV DJANGO_SETTINGS_MODULE=mainweb.settings
ENV PYTHONUNBUFFERED=1

# Run Django database migrations
# This command applies any pending database migrations.
# In a more complex production setup, migrations might be run as a separate step
# in your CI/CD pipeline before starting the application.
RUN python manage.py migrate

# Collect static files into the STATIC_ROOT directory
# --noinput: Prevents collectstatic from asking for user confirmation.
# This is crucial for serving static assets (CSS, JS, images) in production.
RUN python manage.py collectstatic --noinput

# Expose the port that Gunicorn will listen on
# This informs Docker that the container will listen on this port at runtime.
EXPOSE 8000

# Define the command to run your Django application using Gunicorn
# Gunicorn is a production-ready WSGI HTTP Server.
# --bind 0.0.0.0:${PORT}: Binds Gunicorn to all network interfaces on the port
#                         provided by the environment variable (e.g., 8080).
# mainweb.wsgi:application: Specifies the WSGI application to run.
# This path refers to the 'application' object inside your 'mainweb/wsgi.py' file.
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "mainweb.wsgi:application"]


# Use a lightweight Python 3.10 image
FROM python:3.10-slim

# Environment variables to control Python behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system packages and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    netcat-openbsd \
    gettext \
    httpie && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install initial Python packages
RUN python -m pip install --upgrade pip && \
    pip install flask psycopg2-binary

# Set the application directory
WORKDIR /code

# Copy the application code and install requirements
COPY . /code
RUN pip install -r requirements.txt

# Expose the port for Django
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

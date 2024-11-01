FROM python:3.10

# Environment settings
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install necessary packages and dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    gettext \
    httpie \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install required Python packages
RUN python -m pip install --upgrade pip --root-user-action=ignore \
    && pip install flask psycopg2-binary

# Set up the application directory
RUN mkdir /code
WORKDIR /code

# Copy application code and install Python dependencies
COPY . /code
RUN pip install -r /code/requirements.txt

# Expose the port Django will use
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

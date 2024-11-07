FROM python:3.10

# Set the working directory
WORKDIR /code

# Copy requirements file into the container
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 8000

# Start your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

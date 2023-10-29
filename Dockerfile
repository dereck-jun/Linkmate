# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory in the container
RUN mkdir /app
WORKDIR /app

# Install build dependencies and MySQL client library
RUN apk add --no-cache mariadb-dev build-base libffi-dev

# Copy only the requirements file, and install dependencies
COPY requirements.txt /app/
RUN python -m venv /venv
ENV DATABASE_URL=mysql://dereck:Dydwns1!@linkmate.net/linkmate
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "linkmate.wsgi:application"]

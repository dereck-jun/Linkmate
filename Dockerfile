FROM arm64v8/alpine:latest


# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE linkmate.settings
ENV SECRET_KEY $SECRET_KEY

# Install system dependencies using apk package manager
RUN apk update && \
    apk add --no-cache build-base python3-dev py3-pip jpeg-dev zlib-dev mysql-client wget mariadb-dev libffi-dev

# Create a directory for the application
RUN mkdir -p /usr/src
RUN mkdir /usr/src/app

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app/
COPY . /usr/src/app/

# Run the application using wait-for-it.sh script
CMD ["wait-for-it.sh", "db:3306", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]

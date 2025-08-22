FROM python:3.9-slim

# Set the working directory inside the container.  All subsequent
# commands are relative to this directory.
WORKDIR /app

# Copy the requirements file and install dependencies.  The
# python-multipart library is required by FastAPI for handling
# file uploads.  Using --no-cache-dir keeps the image lean.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application source code into the image.
COPY ./app /app/app
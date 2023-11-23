# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y

# Install python dependencies
COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Add and install Python modules
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from the project’s root to the working directory
COPY . /code/

# Run the command to start uWSGI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy local code to the container
COPY . .

# Run the app
CMD ["gunicorn", "-b", ":8080", "app:create_app()"]

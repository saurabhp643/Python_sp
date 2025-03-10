# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn requests

# Expose the port
EXPOSE 8002

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
# The Dockerfile for the order_service is similar to the user_service Dockerfile. The main difference is the port number. The order_service runs on port 8002, while the user_service runs on port 8001.
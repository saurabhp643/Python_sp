# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Expose the port
EXPOSE 8001

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
# The Dockerfile for the user_service is similar to the order_service Dockerfile. The main difference is the port number. The user_service runs on port 8001, while the order_service runs on port 8002.

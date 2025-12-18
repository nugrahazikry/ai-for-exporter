# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run the API using Granian
CMD ["granian", "--interface", "asgi", "--workers", "1", "--host", "0.0.0.0", "--port", "8000", "--no-reload", "app:app"]
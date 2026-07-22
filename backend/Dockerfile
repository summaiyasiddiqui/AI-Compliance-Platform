# Use official Python image
FROM python:3.11-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show logs immediately
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make the startup script executable
RUN chmod +x entrypoint.sh

# Expose FastAPI port
EXPOSE 8000

# Run the startup script
CMD ["./entrypoint.sh"]
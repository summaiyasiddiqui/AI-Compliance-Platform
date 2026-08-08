# Use official Python image
FROM python:3.11-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show logs immediately
ENV PYTHONUNBUFFERED=1

# Create non-root application user
RUN useradd --create-home --shell /bin/bash complianceai

# Create working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make startup script executable
RUN chmod +x entrypoint.sh

# Give application user ownership of application files
RUN chown -R complianceai:complianceai /app

# Switch to non-root user
USER complianceai

# Expose FastAPI port
EXPOSE 8000

# Run startup script
CMD ["./entrypoint.sh"]

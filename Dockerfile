# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /text_analyze

# Install dependencies
COPY requirements.txt /text_analyze/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /text_analyze/

# Expose the port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

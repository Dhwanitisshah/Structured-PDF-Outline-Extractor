# Use official Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code from local app/ folder to container's /app/
COPY app/ ./

# Create output directory (relative to /app)
RUN mkdir -p output

# Run the extractor script by default
CMD ["python", "extract_outline.py"]
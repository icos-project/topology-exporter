FROM python:3.10-slim

# Install software requirements
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        curl=7.88.1-10+deb12u12 && \
    rm -rf /var/lib/apt/lists/*

# Install dependency libraries
RUN pip3 install --no-cache-dir \
        fastapi==0.115.8 \
        uvicorn==0.34.0

# Set working directory
WORKDIR /app

# Copy application files
COPY aggregator.py /app/aggregator.py

# Expose ports
EXPOSE 8000

# Run the application
ENTRYPOINT ["python", "-u", "aggregator.py"]

# Check application health
HEALTHCHECK --start-period=5s --start-interval=1s \
        CMD curl -f http://localhost:8000 || exit 1
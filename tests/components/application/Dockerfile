FROM python:3.10-slim

# Install dependency libraries
RUN pip3 install --no-cache-dir \
        eclipse_zenoh==1.2.1

# Set working directory
WORKDIR /app

# Copy application files
COPY application.py /app/application.py

# Run the application
ENTRYPOINT ["python", "-u", "application.py"]
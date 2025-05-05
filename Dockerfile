FROM python:3.10-slim

LABEL maintainer="Álvaro Ricón R. <alvaro.ricon@bsc.es>" \
      vendor="Barcelona Supercomputing Center (BSC)" \
      url="https://github.com/icos-project/topology-exporter"

# Install software requirements
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        curl=7.88.1-10+deb12u12 && \
    rm -rf /var/lib/apt/lists/*

# Install dependency libraries
RUN pip3 install --no-cache-dir \
        eclipse_zenoh==1.2.1 \
        fastapi==0.115.8 \
        python-keycloak==5.3.1 \
        pyyaml==6.0.2 \
        requests==2.32.3 \
        uvicorn==0.34.0

# Set working directory
WORKDIR /app

# Copy application files
COPY src /app
COPY icos-certificate.crt /etc/ssl/certs/icos-extra-certs.crt

# Expose ports
EXPOSE 80

# Run the application
ENTRYPOINT ["python", "-u", "fastapi_server.py"]

# Check application health
HEALTHCHECK --start-period=5s --start-interval=1s \
        CMD curl -f http://localhost || exit 1
# Build stage with python 3.9 debian
FROM python:3.9-slim as builder
# cd into /app
WORKDIR /app
# Install system level requirements for building
RUN apt-get update && apt-get install -y --no-install-recommends build-essential
# Copy requirements.txt from system to the directory in docker image
COPY requirements.txt .

# Install and build requiremnts as binary packages to /app/wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Runtime stage with python 3.9 debian
FROM python:3.9-slim
# Cd into /app
WORKDIR /app
# Copy the built wheels from the builder to the /app/wheels in runtime stage
COPY --from=builder /app/wheels /wheels
# Install wheels to python installation on runtime stage
RUN pip install --no-cache /wheels/*
# Remove the built wheels to save space
RUN rm -rf /wheels
# Copy src from system directory to app in docker image
COPY src/ /app/
# Run the python script and allow arguments
ENTRYPOINT ["python3", "app.py"]

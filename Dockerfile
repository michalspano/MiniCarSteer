###############################################################################
# LLM: 1.txt, 2.txt, 25.txt, 24.txt
# Dockerfile (G9-DIT63)
# Authors: Kaisa Arumeel, Omid Khodaparast, Michal Spano, Alexander Säfström

# Using ECR base image for the builder stage
FROM public.ecr.aws/docker/library/python:3.9-slim as builder
WORKDIR /app

# Update the system and install necessary build tools and libraries
RUN apt-get update && apt-get install -y \
    --no-install-recommends \ 
    build-essential \
    gcc \
    libc6-dev \
    libgmp-dev \
    cmake \
    tk-dev

# Copy the requirements file and install the dependencies
COPY requirements.txt .

# Install the dependencies from the requirements file using piwheels
RUN pip install --extra-index-url https://www.piwheels.org/simple -r requirements.txt

#######################################################################

# Runtime stage using AWS ECR base image 
FROM public.ecr.aws/docker/library/python:3.9-slim
WORKDIR /app

# Install runtime dependencies for tkinter
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk \
    libtk8.6 \
    libopenblas-dev

# Now transfer only what we need for the runtime, from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
# Copy the app source code to the container
COPY src/ /app/
# Set the entrypoint which will run the app
ENTRYPOINT ["python3", "app.py"]
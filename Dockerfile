################################################################################
# Dockerfile (G9-DIT63)
# Authors: Arumeel Kaisa, Khodaparast Omid, Michal Spano, Säfström Alexander
#
# Stage 1: Install all required dependencies, produce `.pyc` files
FROM python:3.11 as builder
WORKDIR /app
COPY requirements.txt .

# Add missing `libgl1` dependency for cv2
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends libgl1

# Instantiate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install the required Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --no-deps -r requirements.txt

# Copy the contents of the `src` directory
COPY src src

# Compile to `*.pyc`
RUN python -m compileall ./src

################################################################################

# Stage 2: bundle the image
FROM python:3.11
WORKDIR /app

# Reuse from artefacts the builder
COPY --from=builder /venv /venv
COPY --from=builder /app/src /app/src

# Called from the subdirectory `src` (does not work from the root because of
# the dependencies, modules)
WORKDIR src/
CMD ["/venv/bin/python3", "app.py"]
################################################################################

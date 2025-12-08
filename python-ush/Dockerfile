FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app/

# Set Python path
ENV PYTHONPATH=/app/src

# Default command (interactive shell)
CMD ["python3", "-m", "ush.ush"]

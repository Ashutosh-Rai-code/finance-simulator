FROM python:3.11-slim

WORKDIR /app

# Set CARGO_HOME to a writable directory before installing Rust
ENV CARGO_HOME=/tmp/cargo
RUN mkdir -p /tmp/cargo

# Install system dependencies and Rust
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    curl \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Rust to PATH
ENV PATH="/tmp/cargo/bin:${PATH}"

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8000

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

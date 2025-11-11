# Use a lightweight base image with Python 3 and Linux tools
FROM ubuntu:22.04

# Disable interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Update & install essentials
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    nodejs npm \
    g++ \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (requests, rq, etc.)
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

# Copy your code into the container
COPY . /app

# Set environment variables if needed
ENV PYTHONUNBUFFERED=1


# Expose FastAPI’s default port
EXPOSE 8000

# Command to start FastAPI automatically
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
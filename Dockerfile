# Use the latest version of Ubuntu
FROM ubuntu:latest

# Install Python and system dependencies required by WeasyPrint and Pydub
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \  
    libgdk-pixbuf2.0-0 \  
    libpango-1.0-0 \  
    libcairo2 \  
    libgobject-2.0-0 \  
    libglib2.0-0 \  
    libfontconfig1 \  
    libffi-dev \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Create a Python virtual environment and install dependencies
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --no-cache-dir --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Add the virtual environment to the PATH
ENV PATH="/app/venv/bin:$PATH"

# Avoid Python output buffering (e.g., for logs)
ENV PYTHONUNBUFFERED=1

# Command to run the main Python script
CMD ["python", "scripts/main.py"]
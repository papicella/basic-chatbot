# --- Stage 1: Build Environment ---
# Use a Python base image matching your specified version (3.11)
FROM python:3.11-slim-bookworm AS builder

# Set environment variables for non-interactive mode and Python unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy only the requirements file first to take advantage of Docker layer caching
COPY requirements.txt .

# Install dependencies into the virtual environment
# The --no-cache-dir flag reduces image size
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Copy the application code and the templates folder
# The cache.json (containing the token) MUST be present at this stage
# If you don't commit cache.json, you must use Kubernetes Secrets for the token data.
COPY main.py .

# Set the Flask environment variable
ENV FLASK_APP=main.py

# Expose the port that Flask will run on (default Flask port)
EXPOSE 5001

# Command to run the application using Python (Kubernetes will manage the process)
# We use python -m flask run --host=0.0.0.0 to ensure it listens on all interfaces
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

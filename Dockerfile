FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for building packages like chroma-hnswlib
RUN apt-get update && \
    apt-get install -y build-essential gcc g++ && \
    apt-get clean

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command
CMD ["python", "main.py"]
FROM python:3.10-slim
WORKDIR /app

# Copy project
COPY . /app

# Install system dependencies for pillow/opencv if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements and CPU TensorFlow
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir tensorflow-cpu

CMD ["python", "main.py"]

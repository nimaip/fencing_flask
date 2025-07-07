FROM python:3.11-slim

# Install system dependencies needed by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copy the rest of your app
COPY . .

EXPOSE 3000

CMD ["gunicorn", "--bind=0.0.0.0:3000", "app:app"]

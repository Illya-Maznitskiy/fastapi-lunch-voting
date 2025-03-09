FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variables to prevent buffering of output
ENV PYTHONUNBUFFERED 1

# Install system dependencies and tools
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Command to run your FastAPI app using Uvicorn (ASGI server)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

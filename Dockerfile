
FROM ubuntu:latest

# Set the working directory inside the container
WORKDIR /api

# Install dependencies
RUN apt update && apt install -y python3 python3-pip

# Copy the application files
COPY . .

# Install required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

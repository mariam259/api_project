# Use official Python image from DockerHub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the app files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=app.py

# Define the command to run the Flask app
CMD ["flask", "run" , "--host=0.0.0.0", "--port=8080"]
# Use an official lightweight Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
# (We will copy everything needed for running the flask app)
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and serialized model
COPY app.py .
COPY superkart_model.joblib .

# Expose the API port
EXPOSE 7860

# Run the Flask API server
CMD ["python", "app.py"]

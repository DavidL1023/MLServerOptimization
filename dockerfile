# Use an official Python runtime as a parent image with the specific version 3.12.2
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# If you have additional requirements, ensure you have a requirements.txt file in your directory
# and uncomment the next line to install those requirements.
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run"]

# Example docker command to create image
# docker run -p 127.0.0.1:5000:5000 your-image-name
# For more information, please refer to https://aka.ms/vscode-docker-python
# How to get started, refer to https://docs.docker.com/get-started/02_our_app/ 
# How to Containerize an Appplication, refer to https://docs.docker.com/get-started/02_our_app 
# How to Tag and Push, refer to https://cmakkaya.medium.com/docker-desktop-4-docker-hub-authorization-for-docker-desktop-and-pushing-a-image-from-docker-c2babb61a559 
# For this Python application a volume must be created
# docker volume create agrigateonevolume
# Mount a volume to get to the HTML files that has been retrieved and scraped with the following command when running the agrigateone container
# docker run -v agrigateonevolume:/app agrigateone
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. 
# For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "-m", "main.py"]
# Run the Python script when the container launches
CMD [ "python", "./main.py" ]


FROM python:3.10.8-slim-bullseye

# Update system and install Git
RUN apt update && apt upgrade -y
RUN apt install git -y

# Copy dependencies
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip3 install -U pip && pip3 install -U -r /requirements.txt

# Create working directory
RUN mkdir /FileToLink
WORKDIR /FileToLink

# Copy all project files
COPY . /FileToLink

# Start the bot
CMD ["python", "bot.py"]

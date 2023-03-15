# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install the dependencies specified in the requirements.txt file
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get -y update
RUN apt-get install -y wget gnupg curl wkhtmltopdf\
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN cp /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get -y update
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# Copy the rest of the application code to the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port on which the Flask app will run
EXPOSE 80

# Run the command to start the Flask app
CMD ["python", "./app.py"]
# Use the lightweight Python image based on Alpine Linux
FROM python:3.10-alpine

# Install dependencies
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver \
    bash \
    libc6-compat

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables to use Chromium
ENV PATH="/usr/lib/chromium/:/usr/bin/chromedriver:${PATH}"
ENV CHROME_BIN="/usr/bin/chromium-browser"

#Verify installation
#RUN chromium-browser --version && chromedriver --version

# Run the script when the container launches
CMD ["python3", "main_v2.py"]


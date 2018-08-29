# Pull base image
FROM resin/raspberrypi3-python

RUN apt-get update \
    && apt-get -y install \
    python3-pyqt5

# Install adafruit-ads1x15
RUN pip install adafruit-ads1x15

# Define working directory
ADD . /app

# Define default command
CMD [ "python", "./app/UI.py" ]
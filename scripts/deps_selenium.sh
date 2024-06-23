#!/bin/bash

# Install web browser Firefox
apt update && apt install -y firefox-esr

wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb
# Install wget
apt install wget

# Install Gecko driver
export GECKO_DRIVER_VERSION='v0.34.0'
wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz
tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz
rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz
chmod +x geckodriver
mv geckodriver /usr/local/bin/

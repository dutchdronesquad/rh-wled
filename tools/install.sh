#!/bin/bash

wget https://codeload.github.com/dutchdronesquad/rh-wled/zip/main -O ~/temp.zip
unzip ~/temp.zip

# Move the plugin folder into RotorHazard and remove the rest
mv ~/rh-wled-main/wled ~/RotorHazard/src/server/plugins/wled
rm -R ~/rh-wled-main
rm ~/temp.zip
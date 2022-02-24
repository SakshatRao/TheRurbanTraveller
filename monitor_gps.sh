#!/bin/bash

while :
do
    if [[ -f "/home/sakshat/Downloads/output.csv" ]]
    then
        echo "Found GPS coordinates"
        mv /home/sakshat/Downloads/output.csv /home/sakshat/Documents/TheRurbanTraveller/Memories/GPS_Coords_Data/gps_coords.csv
    fi
done
#!/bin/bash

while :
do
    if [[ -f "/home/sakshat/Downloads/select_memories.txt" ]]
    then
        echo "Found Memories Request"
        rm /home/sakshat/Downloads/select_memories.txt
        /home/sakshat/anaconda3/envs/TheRurbanTraveller_Python/bin/python /home/sakshat/Documents/TheRurbanTraveller/Memories/Animation/memories_animation.py
    fi
done
#!/bin/bash

until /home/sakshat/anaconda3/envs/TheRurbanTraveller_Python/bin/python /home/sakshat/Documents/TheRurbanTraveller/OBD2_Simulator/obd2_simulator.py
do
    echo "Retrying"
done
# /home/sakshat/anaconda3/envs/TheRurbanTraveller_Python/bin/python /home/sakshat/Documents/TheRurbanTraveller/OBD2_Simulator/sim_plot.py
/home/sakshat/anaconda3/envs/TheRurbanTraveller_Python/bin/python /home/sakshat/Documents/TheRurbanTraveller/Routine_Recognizer/model.py

# /home/sakshat/anaconda3/envs/TheRurbanTraveller_Python/bin/python /home/sakshat/Documents/TheRurbanTraveller/Memories/Animation/memories_animation.py
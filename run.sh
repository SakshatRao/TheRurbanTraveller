#!/bin/bash

./monitor_gps.sh &
./monitor_memories.sh &
./recommendations.sh
./routine_recognizer.sh
./memories.sh
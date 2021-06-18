#!/bin/bash

DATA_PATH=$1
COUNTS_POINTS_RADIUS=$2

echo "Finding counts links..."
python python_scripts/find_links.py $DATA_PATH $COUNTS_POINTS_RADIUS
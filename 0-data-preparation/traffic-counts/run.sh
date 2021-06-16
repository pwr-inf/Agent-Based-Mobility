#!/bin/bash

DATA_PATH=$1
DATA_PATH=$DATA_PATH/traffic_counts

mkdir $DATA_PATH
mkdir $DATA_PATH/raw
mkdir $DATA_PATH/interim
mkdir $DATA_PATH/processed

echo "Downloading KBR traffic counts..."
./bash_scripts/download_data.sh $DATA_PATH/raw/kbr_traffic_counts.zip

./bash_scripts/process_data.sh $DATA_PATH
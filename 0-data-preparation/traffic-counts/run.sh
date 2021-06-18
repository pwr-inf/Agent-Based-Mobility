#!/bin/bash

DATA_PATH=$1
COUNTS_POINTS_RADIUS=$2

mkdir $DATA_PATH/traffic_counts
mkdir $DATA_PATH/traffic_counts/raw
mkdir $DATA_PATH/traffic_counts/interim
mkdir $DATA_PATH/traffic_counts/processed

./bash_scripts/download_data.sh $DATA_PATH/traffic_counts/raw/kbr_traffic_counts.zip

./bash_scripts/process_data.sh $DATA_PATH/traffic_counts

./bash_scripts/find_links.sh $DATA_PATH $COUNTS_POINTS_RADIUS
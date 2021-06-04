#!/bin/bash

DATA_PATH=$1
DATA_PATH=$DATA_PATH/network

mkdir $DATA_PATH
mkdir $DATA_PATH/interim
mkdir $DATA_PATH/processed
mkdir $DATA_PATH/processing_logs
mkdir $DATA_PATH/raw

./bash_scripts/download_data.sh $DATA_PATH
./bash_scripts/process_data.sh $DATA_PATH
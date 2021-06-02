#!/bin/bash

DATA_PATH=$1

./bash_scripts/download_data.sh $DATA_PATH
./bash_scripts/process_data.sh $DATA_PATH
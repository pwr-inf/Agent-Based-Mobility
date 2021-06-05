#!/bin/bash

DATA_PATH=$1
SCENARIO_NAME=$2
HEX_SIZE=$3

echo "Processing genet standard output..."
python genet_standard_output.py  $DATA_PATH $SCENARIO_NAME \

echo "Processing custom output..."
python custom_vis.py $DATA_PATH $SCENARIO_NAME \

echo "Processing vehicles to csv..."
python genet_veh_to_csv.py $DATA_PATH $SCENARIO_NAME \

echo "Processing count hex events..."
python count_hex_events.py $DATA_PATH $SCENARIO_NAME $HEX_SIZE

python rename_scenario.py $DATA_PATH $SCENARIO_NAME _$(date +"%H-%M-%S")
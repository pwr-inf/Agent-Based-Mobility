#!/bin/bash

SCENARIOS_PATH=$1
SCENARIO_NAME=$2
HEX_SIZE=$3
INPUT_DATA_PATH=$4

echo "Processing genet standard output..."
python genet_standard_output.py  $SCENARIOS_PATH $SCENARIO_NAME

echo "Processing network counts..."
python counts_network.py $SCENARIOS_PATH $SCENARIO_NAME

# echo "Processing points counts..."
# python counts_points.py $INPUT_DATA_PATH $SCENARIOS_PATH $SCENARIO_NAME \

echo "Processing vehicles to csv..."
python genet_veh_to_csv.py $SCENARIOS_PATH $SCENARIO_NAME

# echo "Processing count hex events..."
# python count_hex_events.py $SCENARIOS_PATH $SCENARIO_NAME $HEX_SIZE

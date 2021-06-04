#!/bin/bash

DATA_PATH=$1
POPULATIONS_PATH=$2
SCENARIO_NAME=$3

ACTIVITIES_PATH=$POPULATIONS_PATH/$SCENARIO_NAME/scenarios_1_1_pub_trans_comfort_dist-up_0_0_pub_trans_punctuality_dist-up_0_0_household_cars_dist-down_0_0

echo "Processing data..."
python process_data.py config.json \
$ACTIVITIES_PATH/agents_results_1.csv $ACTIVITIES_PATH/travels_results_1.csv \
$DATA_PATH/facilities/processed/facilities.csv \
$POPULATIONS_PATH/$SCENARIO_NAME/agents.csv \
$POPULATIONS_PATH/$SCENARIO_NAME/travels.csv 7

echo "Writing xml..."
python write_xml.py \
$POPULATIONS_PATH/$SCENARIO_NAME/agents.csv $POPULATIONS_PATH/$SCENARIO_NAME/travels.csv \
$DATA_PATH/facilities/processed/facilities.csv $POPULATIONS_PATH/$SCENARIO_NAME/population.xml
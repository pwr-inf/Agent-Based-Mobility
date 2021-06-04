#!/bin/bash

DATA_PATH=$1
OUTPUT_PATH=$2
POPULATION=$3
NUM_SIMULATIONS=$4
NUM_PROCESSES=$5

cp -r $DATA_PATH ./data-private

rm -r $OUTPUT_PATH
mkdir $OUTPUT_PATH

python prepare_scenarios.py \
[decision_tree/pub_trans_comfort_dist-up,decision_tree/pub_trans_punctuality_dist-up,decision_tree/household_cars_dist-down] \
[0.] 1 scenarios

python run_simulations.py scenarios scenarios_1 data-private $OUTPUT_PATH $POPULATION $NUM_SIMULATIONS $NUM_PROCESSES
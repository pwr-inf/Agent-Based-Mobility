#!/bin/bash

SCENARIOS_PATH=$1
SCENARIO_NAME=$2

python rename_scenario.py $SCENARIOS_PATH $SCENARIO_NAME _$(date +"%H-%M-%S")
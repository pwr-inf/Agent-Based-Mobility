#!/bin/bash

DATA_PATH=$1
POPULATIONS_PATH=$2
SCENARIOS_PATH=$3
SCENARIO_NAME=$4
SCENARIO_PATH="$SCENARIOS_PATH/$(date +"%d-%m-%Y_%H-%M-%S")_$SCENARIO_NAME"
mkdir $SCENARIO_PATH

cp $DATA_PATH/network/processed/* $SCENARIO_PATH
cp config_simulation.xml $SCENARIO_PATH
cp $POPULATIONS_PATH/$SCENARIO_NAME/* $SCENARIO_PATH
cp -r $DATA_PATH/facilities/processed/* $SCENARIO_PATH

java -Xmx12g -cp /home/workdir/matsim-13.0/matsim-13.0.jar \
org.matsim.run.Controler $SCENARIO_PATH/config_simulation.xml

mkdir $SCENARIO_PATH/output
cp -r output/* $SCENARIO_PATH/output
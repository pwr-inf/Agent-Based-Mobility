#!/bin/bash

DATA_PATH=$1
DATA_PATH=$DATA_PATH/activity_model

mkdir $DATA_PATH

git clone https://github.com/weronika997/urban-mobility-project.git
mv urban-mobility-project/experiments/input_data  $DATA_PATH/base_input_data
yes | rm -r urban-mobility-project
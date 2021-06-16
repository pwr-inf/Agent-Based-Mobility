#!/bin/bash

DATA_PATH=$1

echo "Unziping KBR traffic counts..."
unzip -o $DATA_PATH/raw/kbr_traffic_counts.zip -d $DATA_PATH/interim/kbr_traffic_counts_temp > /dev/null 2>&1
convmv -f cp1250 -t utf8 --notest -r $DATA_PATH/interim/kbr_traffic_counts_temp > /dev/null 2>&1
cp -r \
$DATA_PATH"/interim/kbr_traffic_counts_temp/2-Pomiary nat©ĺenia ruchu drogowego/" \
$DATA_PATH/interim/
mv $DATA_PATH/interim/2-Pomiary\ nat©ĺenia\ ruchu\ drogowego/ $DATA_PATH/interim/kbr_traffic_counts
rm -r $DATA_PATH/interim/kbr_traffic_counts_temp

echo "Processing traffic counts..."
python python_scripts/process_counts.py \
$DATA_PATH/interim/kbr_traffic_counts/ \
$DATA_PATH/processed/
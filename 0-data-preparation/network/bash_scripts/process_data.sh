#!/bin/bash

DATA_PATH=$1

LOGS_PATH=$DATA_PATH"/processing_logs/$(date +"%d-%m-%Y_%H-%M-%S")"
mkdir $LOGS_PATH

# osm to network
echo "OSM to network..."
OSM_TO_NETWORK_LOGS=$LOGS_PATH/osm_to_network.log
java -cp pt2matsim-20-12.jar \
org.matsim.pt2matsim.run.Osm2MultimodalNetwork config/config_osm_to_network.xml \
&> $OSM_TO_NETWORK_LOGS
echo "Logs saved in $OSM_TO_NETWORK_LOGS"

# gtfs to unmapped schedule
echo "GTFS to unmapped schedule..."
GTFS_TO_SCH_LOGS=$LOGS_PATH/gtfs_to_unmapped_schedule.log
unzip $DATA_PATH/raw/gtfs.zip -d $DATA_PATH/interim/gtfs > /dev/null 2>&1
echo "..."
java -cp pt2matsim-20-12.jar org.matsim.pt2matsim.run.Gtfs2TransitSchedule \
$DATA_PATH/interim/gtfs dayWithMostServices EPSG:2177 \
$DATA_PATH/interim/pt_schedule.xml $DATA_PATH/processed/vehicles.xml\
&> $GTFS_TO_SCH_LOGS
echo "Logs saved in $GTFS_TO_SCH_LOGS"

# map schedule
echo "Mapping schedule..."
MAPPING_SCH_LOGS=$LOGS_PATH/mapping_schedule.log
java -cp pt2matsim-20-12.jar \
org.matsim.pt2matsim.run.PublicTransitMapper config/config_pt_mapper.xml \
&> $MAPPING_SCH_LOGS
echo "Logs saved in $MAPPING_SCH_LOGS"
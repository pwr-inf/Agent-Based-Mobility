#!/bin/bash

DATA_PATH=$1
DATA_PATH=$DATA_PATH/facilities

mkdir $DATA_PATH
mkdir $DATA_PATH/raw
mkdir $DATA_PATH/interim
mkdir $DATA_PATH/processed
mkdir $DATA_PATH/processed/shp
mkdir $DATA_PATH/vis/qgis_buildings_tags
mkdir $DATA_PATH/vis/qgis_buildings_filtered_by_area_tags
mkdir $DATA_PATH/vis/qgis_processed_buildings_tags
mkdir $DATA_PATH/vis/qgis_buildings_area
mkdir $DATA_PATH/vis/qgis_shops_tags
mkdir $DATA_PATH/vis/qgis_processed_shops_tags
mkdir $DATA_PATH/vis/qgis_amenities_tags
mkdir $DATA_PATH/vis/qgis_processed_amenities_tags

echo "Downloading KBR regions..."
./bash_scripts/download_regions.sh $DATA_PATH/raw/kbr_regions.zip

echo "Downloading OSM buildings..."
python python_scripts/download_osm_buildings.py $DATA_PATH/raw/osm_buildings.shp

echo "Downloading OSM shops..."
python python_scripts/download_osm_shops.py $DATA_PATH/raw/osm_shops.shp

echo "Downloading OSM amenities..."
python python_scripts/download_osm_amenities.py $DATA_PATH/raw/osm_amenities.shp
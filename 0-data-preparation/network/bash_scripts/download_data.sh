DATA_PATH=$1

# echo "Downloading OSM data..."
# ./bash_scripts/download_osm.sh $DATA_PATH/raw/map.osm

echo "Downloading GTFS data..."
./bash_scripts/download_gtfs.sh $DATA_PATH/raw/gtfs.zip
#!/bin/bash

DATA_PATH=$1
DATA_PATH=$DATA_PATH/facilities

echo "Unziping KBR regions..."
unzip -o $DATA_PATH/raw/kbr_regions.zip -d $DATA_PATH/interim/kbr_regions_temp > /dev/null 2>&1
convmv -f cp1250 -t utf8 --notest -r $DATA_PATH/interim/kbr_regions_temp > /dev/null 2>&1
cp -r \
$DATA_PATH"/interim/kbr_regions_temp//Etap I i II - Wyznaczenie obszaru badaő, liczby mieszkaőców i miejsc pracy na podstawie kart SIM/Pliki GIS - Wyznaczenie obszaru badaő/2-Podziaę na rejony/" \
$DATA_PATH/interim/
mv $DATA_PATH/interim/2-Podziaę\ na\ rejony/ $DATA_PATH/interim/kbr_regions
rm -r $DATA_PATH/interim/kbr_regions_temp

echo "Processing regions..."
python python_scripts/process_regions.py \
$DATA_PATH/interim/kbr_regions/EtapII-REJONY_wroclaw.shp \
$DATA_PATH/interim/regions.shp

echo "Processing facilities..."
python python_scripts/process_facilities.py $DATA_PATH \
config/config.json

echo "Visualising data..."
python python_scripts/make_visualizations.py $DATA_PATH

echo "Writing xml..."
python python_scripts/write_xml.py $DATA_PATH/processed/facilities.csv \
$DATA_PATH/processed/facilities.xml
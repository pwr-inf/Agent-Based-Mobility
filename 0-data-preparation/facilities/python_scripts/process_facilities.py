import json
import sys

import geopandas as gpd
import pandas as pd
from tqdm import tqdm

REGIONS_SHP_IN_FILE = 'interim/regions.shp'
BUILDINGS_SHP_IN_FILE = 'raw/osm_buildings.shp'
SHOPS_SHP_IN_FILE = 'raw/osm_shops.shp'
AMENITIES_SHP_IN_FILE = 'raw/osm_amenities.shp'

BUILD_F_A_SHP_OUT_FILE = 'interim/buildings_filtered_by_area.shp'
BUILDINGS_SHP_OUT_FILE = 'processed/shp/buildings.shp'
SHOPS_SHP_OUT_FILE = 'processed/shp/shops.shp'
AMENITIES_SHP_OUT_FILE = 'processed/shp/amenities.shp'

BUILDINGS_CSV_OUT_FILE = 'interim/buildings.csv'
SHOPS_CSV_OUT_FILE = 'interim/shops.csv'
AMENITIES_CSV_OUT_FILE = 'interim/amenities.csv'
FACILITIES_CSV_OUT_FILE = 'processed/facilities.csv'


def get_region_id(regions, point):
    mapped_region_id = -1
    for row in regions.itertuples():
        region_id = row[1]
        region_polygon = row[3]
        if point.within(region_polygon):
            mapped_region_id = region_id
            return mapped_region_id
    return mapped_region_id


def process_sub_df(df, category):
    df['id'] = df.apply(lambda row: category+'_'+str(row['osmid']), axis=1)
    df['category'] = category
    df = df.rename(columns={category: 'tag'})
    df = df[['id', 'category', 'tag', 'name', 'region_id', 'x', 'y']]

    return df


if __name__ == "__main__":

    data_path = sys.argv[1]
    if not data_path.endswith('/'):
        data_path += '/'
    config_file_path = sys.argv[2]

    tqdm.pandas()

    # load configs
    with open(config_file_path) as f:
        config = json.load(f)
    buildings_min_area = config['buildings_min_area']
    buildings_tags_to_leave = config['buildings_tags_to_leave']
    shops_tags_to_leave = config['shops_tags_to_leave']
    shops_tags_mapping = config['shops_tags_mapping']
    amenities_tags_to_leave = config['amenities_tags_to_leave']
    amenities_tags_mapping = config['amenities_tags_mapping']

    # load regions
    regions = gpd.read_file(data_path+REGIONS_SHP_IN_FILE)

    # buildings
    buildings = gpd.read_file(data_path+BUILDINGS_SHP_IN_FILE)
    # filter by area
    buildings = buildings[buildings['area'] > buildings_min_area]
    buildings.to_file(data_path+BUILD_F_A_SHP_OUT_FILE)
    # filter by tags
    buildings = buildings[buildings['building'].isin(buildings_tags_to_leave)]
    # map regions
    buildings['region_id'] = buildings.progress_apply(
        lambda row: get_region_id(regions, row['geometry']),
        axis=1
    )
    # to shp
    buildings.to_file(data_path+BUILDINGS_SHP_OUT_FILE)
    # to csv
    buildings['x'] = buildings.apply(
        lambda row: str(row['geometry'].coords[0][0]),
        axis=1
    )
    buildings['y'] = buildings.apply(
        lambda row: str(row['geometry'].coords[0][1]),
        axis=1
    )
    columns = ['osmid', 'building', 'name', 'area', 'region_id', 'x', 'y']
    buildings[columns].to_csv(data_path+BUILDINGS_CSV_OUT_FILE, index=False)

    # shops
    shops = gpd.read_file(data_path+SHOPS_SHP_IN_FILE)
    # filter by tags and map values
    shops = shops[shops['shop'].isin(shops_tags_to_leave)]
    shops = shops.replace(shops_tags_mapping)
    # map regions
    shops['region_id'] = shops.progress_apply(
        lambda row: get_region_id(regions, row['geometry']),
        axis=1
    )
    # to shp
    shops.to_file(data_path+SHOPS_SHP_OUT_FILE)
    # to csv
    shops['x'] = shops.apply(
        lambda row: str(row['geometry'].coords[0][0]),
        axis=1
    )
    shops['y'] = shops.apply(
        lambda row: str(row['geometry'].coords[0][1]),
        axis=1
    )
    columns = ['osmid', 'shop', 'name', 'region_id', 'x', 'y']
    shops[columns].to_csv(data_path+SHOPS_CSV_OUT_FILE, index=False)

    # amenities
    amenities = gpd.read_file(data_path+AMENITIES_SHP_IN_FILE)
    # filter by tags and map values
    amenities = amenities[amenities['amenity'].isin(amenities_tags_to_leave)]
    amenities = amenities.replace(amenities_tags_mapping)
    # map regions
    amenities['region_id'] = amenities.progress_apply(
        lambda row: get_region_id(regions, row['geometry']),
        axis=1
    )
    # to shp
    amenities.to_file(data_path+AMENITIES_SHP_OUT_FILE)
    # to csv
    amenities['x'] = amenities.apply(
        lambda row: str(row['geometry'].coords[0][0]),
        axis=1
    )
    amenities['y'] = amenities.apply(
        lambda row: str(row['geometry'].coords[0][1]),
        axis=1
    )
    columns = ['osmid', 'amenity', 'name', 'region_id', 'x', 'y']
    amenities[columns].to_csv(data_path+AMENITIES_CSV_OUT_FILE, index=False)

    # facilities
    buildings = process_sub_df(buildings, 'building')
    shops = process_sub_df(shops, 'shop')
    amenities = process_sub_df(amenities, 'amenity')
    facilities = pd.concat([shops, amenities, buildings])
    # to csv
    facilities.to_csv(data_path+FACILITIES_CSV_OUT_FILE, index=False)

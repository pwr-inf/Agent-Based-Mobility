import sys

import geopandas as gpd
import plotly.express as px
from tqdm import tqdm

BUILDINGS_SHP_IN_FILE = 'raw/osm_buildings.shp'
BUILD_F_A_SHP_IN_FILE = 'interim/buildings_filtered_by_area.shp'
PROC_BUILD_SHP_IN_FILE = 'processed/shp/buildings.shp'

SHOPS_SHP_IN_FILE = 'raw/osm_shops.shp'
PROC_SHOPS_SHP_IN_FILE = 'processed/shp/shops.shp'

AMENITIES_SHP_IN_FILE = 'raw/osm_amenities.shp'
PROC_AMENITIES_SHP_IN_FILE = 'processed/shp/amenities.shp'


QGIS_BUILDINGS_TAGS_OUT_FOLDER = 'vis/qgis_buildings_tags'
QGIS_BUILD_F_A_TAGS_OUT_FOLDER = 'vis/qgis_buildings_filtered_by_area_tags'
QGIS_PROC_BUILD_TAGS_OUT_FOLDER = 'vis/qgis_processed_buildings_tags'

QGIS_BUILDINGS_AREA_OUT_FOLDER = 'vis/qgis_buildings_area'

QGIS_SHOPS_TAGS_OUT_FOLDER = 'vis/qgis_shops_tags'
QGIS_PROC_SHOPS_TAGS_OUT_FOLDER = 'vis/qgis_processed_shops_tags'

QGIS_AMENITIES_TAGS_OUT_FOLDER = 'vis/qgis_amenities_tags'
QGIS_PROC_AMENITIES_TAGS_OUT_FOLDER = 'vis/qgis_processed_amenities_tags'


BUILDINGS_HISTOGRAM_OUT_FILE = 'vis/buildings_histogram.html'
BUILD_F_A_HISTOGRAM_OUT_FILE = 'vis/buildings_filtered_by_area_histogram.html'
PROC_BUILD_HISTOGRAM_OUT_FILE = 'vis/processed_buildings_histogram.html'

SHOPS_HISTOGRAM_OUT_FILE = 'vis/shops_histogram.html'
PROC_SHOPS_HISTOGRAM_OUT_FILE = 'vis/processed_shops_histogram.html'

AMENITIES_HISTOGRAM_OUT_FILE = 'vis/amenities_histogram.html'
PROC_AMENITIES_HISTOGRAM_OUT_FILE = 'vis/processed_amenities_histogram.html'

AREA_TRESHOLDS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

if __name__ == "__main__":

    data_path = sys.argv[1]
    if not data_path.endswith('/'):
        data_path += '/'

    # read data
    buildings = gpd.read_file(data_path+BUILDINGS_SHP_IN_FILE)
    buildings_f_a = gpd.read_file(data_path+BUILD_F_A_SHP_IN_FILE)
    processed_buildings = gpd.read_file(data_path+PROC_BUILD_SHP_IN_FILE)
    shops = gpd.read_file(data_path+SHOPS_SHP_IN_FILE)
    processed_shops = gpd.read_file(data_path+PROC_SHOPS_SHP_IN_FILE)
    amenities = gpd.read_file(data_path+AMENITIES_SHP_IN_FILE)
    processed_amenities = gpd.read_file(data_path+PROC_AMENITIES_SHP_IN_FILE)

    # qgis buildings tags
    for b in tqdm(buildings['building'].unique()):
        buildings[buildings['building'] == b].to_file(
            data_path+QGIS_BUILDINGS_TAGS_OUT_FOLDER+'/'+b+'.shp'
        )

    # qgis buildings filtered by area tags
    for b in tqdm(buildings_f_a['building'].unique()):
        buildings_f_a[buildings_f_a['building'] == b].to_file(
            data_path+QGIS_BUILD_F_A_TAGS_OUT_FOLDER+'/'+b+'.shp'
        )

    # qgis processed buildings tags
    for b in tqdm(processed_buildings['building'].unique()):
        processed_buildings[processed_buildings['building'] == b].to_file(
            data_path+QGIS_PROC_BUILD_TAGS_OUT_FOLDER+'/'+b+'.shp'
        )

    # qgis buildings area
    for min_tre in tqdm(AREA_TRESHOLDS):
        buildings[buildings['area'] > min_tre].to_file(
            data_path+QGIS_BUILDINGS_AREA_OUT_FOLDER+'/'+str(min_tre)+'_m2.shp'
        )

    # qgis shops tags
    for s in tqdm(shops['shop'].unique()):
        shops[shops['shop'] == s].to_file(
            data_path+QGIS_SHOPS_TAGS_OUT_FOLDER+'/'+s+'.shp'
        )

    # qgis processed shops tags
    for s in tqdm(processed_shops['shop'].unique()):
        processed_shops[processed_shops['shop'] == s].to_file(
            data_path+QGIS_PROC_SHOPS_TAGS_OUT_FOLDER+'/'+s+'.shp'
        )

    # qgis amenities tags
    for a in tqdm(amenities['amenity'].unique()):
        amenities[amenities['amenity'] == a].to_file(
            data_path+QGIS_AMENITIES_TAGS_OUT_FOLDER+'/'+a+'.shp'
        )

    # qgis processed amenities tags
    for a in tqdm(processed_amenities['amenity'].unique()):
        processed_amenities[processed_amenities['amenity'] == a].to_file(
            data_path+QGIS_PROC_AMENITIES_TAGS_OUT_FOLDER+'/'+a+'.shp'
        )

    # buildings histogram
    buildings_total_number = len(buildings)
    buildings_count = buildings[['building', 'osmid']]
    buildings_count = buildings_count.groupby('building').count()
    buildings_count = buildings_count.rename(columns={'osmid': 'count'})
    buildings_count = buildings_count.sort_values('count', ascending=True)
    fig = px.bar(
        buildings_count, orientation='h',
        x='count', text='count',
        height=4000, width=1000
    )
    fig.update_layout({
        'title': 'Buildings type histogram, total='+str(buildings_total_number)
    })
    fig.write_html(data_path+BUILDINGS_HISTOGRAM_OUT_FILE)

    # buildings filtered by area histogram
    buildings_total_number = len(buildings_f_a)
    buildings_count = buildings_f_a[['building', 'osmid']]
    buildings_count = buildings_count.groupby('building').count()
    buildings_count = buildings_count.rename(columns={'osmid': 'count'})
    buildings_count = buildings_count.sort_values('count', ascending=True)
    fig = px.bar(
        buildings_count, orientation='h',
        x='count', text='count',
        height=4000, width=1000
    )
    title_prefix = 'Buildings filtered by area type histogram, total='
    fig.update_layout({
        'title': title_prefix+str(buildings_total_number)
    })
    fig.write_html(data_path+BUILD_F_A_HISTOGRAM_OUT_FILE)

    # processed buildings histogram
    buildings_total_number = len(processed_buildings)
    buildings_count = processed_buildings[['building', 'osmid']]
    buildings_count = buildings_count.groupby('building').count()
    buildings_count = buildings_count.rename(columns={'osmid': 'count'})
    buildings_count = buildings_count.sort_values('count', ascending=True)
    fig = px.bar(
        buildings_count, orientation='h',
        x='count', text='count',
        height=4000, width=1000
    )
    title_prefix = 'Processed buildings type histogram, total='
    fig.update_layout({
        'title': title_prefix+str(buildings_total_number)
    })
    fig.write_html(data_path+PROC_BUILD_HISTOGRAM_OUT_FILE)

    # shops histogram
    shops_total_number = len(shops)
    shops_count = shops[['shop', 'osmid']]
    shops_count = shops_count.groupby('shop').count()
    shops_count = shops_count.rename(columns={'osmid': 'count'})
    shops_count = shops_count.sort_values('count', ascending=True)
    fig = px.bar(
        shops_count, orientation='h',
        x='count', text='count',
        height=4000, width=1000
    )
    fig.update_layout({
        'title': 'Shops type histogram, total='+str(shops_total_number)
    })
    fig.write_html(data_path+SHOPS_HISTOGRAM_OUT_FILE)

    # processed shops histogram
    shops_total_number = len(processed_shops)
    shops_count = processed_shops[['shop', 'osmid']]
    shops_count = shops_count.groupby('shop').count()
    shops_count = shops_count.rename(columns={'osmid': 'count'})
    shops_count = shops_count.sort_values('count', ascending=True)
    fig = px.bar(
        shops_count, orientation='h',
        x='count', text='count',
        height=4000, width=1000
    )
    title_prefix = 'Processed shops type histogram, total='
    fig.update_layout({
        'title': title_prefix+str(shops_total_number)
    })
    fig.write_html(data_path+PROC_SHOPS_HISTOGRAM_OUT_FILE)

    # amenities histogram
    amenities_total_number = len(amenities)
    amenities_count = amenities[['amenity', 'osmid']]
    amenities_count = amenities_count.groupby('amenity').count()
    amenities_count = amenities_count.rename(columns={'osmid': 'count'})
    amenities_count = amenities_count.sort_values('count', ascending=True)
    fig = px.bar(
        amenities_count, orientation='h',
        x='count', text='count',
        height=4000, width=1000
    )
    fig.update_layout({
        'title': 'Amenities type histogram, total='+str(amenities_total_number)
    })
    fig.write_html(data_path+AMENITIES_HISTOGRAM_OUT_FILE)

    # processed amenities histogram
    amenities_total_number = len(processed_amenities)
    amenities_count = processed_amenities[['amenity', 'osmid']]
    amenities_count = amenities_count.groupby('amenity').count()
    amenities_count = amenities_count.rename(columns={'osmid': 'count'})
    amenities_count = amenities_count.sort_values('count', ascending=True)
    fig = px.bar(
        amenities_count, orientation='h',
        x='count', text='count',
        height=4000, width=1000
    )
    title_prefix = 'Processed amenities type histogram, total='
    fig.update_layout({
        'title': title_prefix+str(amenities_total_number)
    })
    fig.write_html(data_path+PROC_AMENITIES_HISTOGRAM_OUT_FILE)

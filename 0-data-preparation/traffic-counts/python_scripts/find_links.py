import os
import sys
import json

import geopandas as gpd
import pandas as pd
from genet import read_matsim

if __name__ == "__main__":

    data_path = sys.argv[1]
    point_radius_m = int(sys.argv[2])

    # read matsim network

    n = read_matsim(
        path_to_network=os.path.join(
            data_path, 'network/processed/network.xml'
        ),
        epsg='epsg:2177',
        path_to_schedule=os.path.join(
            data_path, 'network/processed/pt_schedule.xml'
        ),
        path_to_vehicles=os.path.join(
            data_path, 'network/processed/vehicles.xml'
        ),
    )

    # create geopandas

    geojson_folder = os.path.join(
        data_path, 'traffic_counts/interim/network'
    )
    try:
        os.mkdir(geojson_folder)
    except FileExistsError:
        pass
    n.write_to_geojson(geojson_folder)
    network_gdf = gpd.read_file(
        os.path.join(geojson_folder, 'network_links.geojson')
    )

    # read counting points

    points_gdf = gpd.read_file(
        os.path.join(
            data_path,
            'traffic_counts/interim',
            'kbr_traffic_counts/EtapV-2_Punkty_pomiarowe_ruchu_drogowego.shp'
        )
    )

    # read kbr counts

    counts_folder = os.path.join(data_path, 'traffic_counts/processed')
    counts_files = ['ring_1.csv', 'ring_2.csv', 'ring_3.csv']

    counts = pd.DataFrame()
    for f in counts_files:
        counts = pd.concat([
            counts,
            pd.read_csv(os.path.join(counts_folder, f))
        ])

    # read streets mapping

    with open('./config/streets_mapping.json', 'r') as f:
        streets_kbr_to_osm = json.load(f)

    # finding links

    kbr_street_to_id = dict(zip(counts['street'], counts['id']))

    points_links = {}

    points_circles_df = pd.DataFrame(columns=['id', 'geometry'])
    links_df = pd.DataFrame(columns=['id', 'point_id', 'geometry'])

    for kbr_street, osm_street in list(streets_kbr_to_osm.items()):

        point = points_gdf[
            points_gdf['Pkt_pomiar'] == kbr_street_to_id[kbr_street]
        ].iloc[0].geometry.buffer(point_radius_m)

        points_circles_df = points_circles_df.append(
            {
                'id': kbr_street_to_id[kbr_street],
                'geometry': point
            },
            ignore_index=True
        )

        street_links_ids = n.extract_links_on_edge_attributes(
            conditions={'attributes': {'osm:way:name': {'text': osm_street}}},
        )

        intersected_links_ids = []

        for street_link_id in street_links_ids:

            street_link = network_gdf[
                network_gdf['id'] == street_link_id
            ].iloc[0].geometry
            if point.intersects(street_link):
                intersected_links_ids.append(street_link_id)
                links_df = links_df.append(
                    {
                        'id': street_link_id,
                        'point_id': kbr_street_to_id[kbr_street],
                        'geometry': street_link
                    },
                    ignore_index=True
                )

        points_links[kbr_street_to_id[kbr_street]] = intersected_links_ids

    points_circles_gdf = gpd.GeoDataFrame(
        points_circles_df
    ).set_crs("EPSG:2177")
    links_gdf = gpd.GeoDataFrame(
        links_df
    ).set_crs("EPSG:2177")

    # save output

    with open(
        os.path.join(data_path, 'traffic_counts/processed/points_links.json'),
        'w'
    ) as f:
        json.dump(points_links, f)
    gdf_out_folder = os.path.join(
        data_path, 'traffic_counts/interim/counts_links_shp'
    )
    try:
        os.mkdir(gdf_out_folder)
    except FileExistsError:
        pass
    points_circles_gdf.to_file(os.path.join(gdf_out_folder, 'kbr_points.shp'))
    links_gdf.to_file(os.path.join(gdf_out_folder, 'kbr_links.shp'))

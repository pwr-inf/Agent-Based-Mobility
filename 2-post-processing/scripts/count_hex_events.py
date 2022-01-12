import os
import sys
from collections import defaultdict
from typing import Dict, List

import geopandas as gpd
import h3
import matsim
import pandas as pd
from shapely.geometry import LineString, Polygon, Point
from tqdm import tqdm


def get_scenario_path(
    data_path: str,
    scenario_name: str
) -> str:

    if not data_path.endswith('/'):
        data_path += '/'
    files = os.listdir(data_path)

    if files.count(scenario_name) == 1:
        scenario_path = data_path + scenario_name
    elif files.count(scenario_name) > 1:
        raise Exception('Found more than one scenario with given name!')
    else:
        files = list(filter(
            lambda file_name: file_name.endswith(scenario_name),
            files
        ))
        if len(files) == 1:
            scenario_path = data_path + files[0]
        elif len(files) > 1:
            raise Exception('Found more than one scenario with given name!')
        else:
            raise Exception(
                'Scenario '+scenario_name+' not found in '+str(data_path)+' !'
            )

    return scenario_path


def get_links_hexes(
    scenario_path: str,
    resolution: int
) -> Dict[str, List[str]]:

    net = matsim.read_network(scenario_path+'/output/output_network.xml.gz')
    nodes = net.nodes
    nodes_coord = dict(zip(nodes['node_id'], zip(nodes['x'], nodes['y'])))
    links = net.links
    links['geometry'] = links.apply(
        lambda row: LineString(
            [
                nodes_coord[row['from_node']],
                nodes_coord[row['to_node']]
            ]
        ),
        axis=1
    )
    links = gpd.GeoDataFrame(links)
    links.crs = "EPSG:2177"
    links = links.to_crs('EPSG:4327')

    def _add_hexes(row):
        try:
            start, end = row['geometry'].boundary
            row['hexes'] = h3.h3_line(
                h3.geo_to_h3(
                    start.y,
                    start.x,
                    resolution
                ),
                h3.geo_to_h3(
                    end.y,
                    end.x,
                    resolution
                ),
            )
        except ValueError:
            row['hexes'] = []

        return row

    links = links.apply(_add_hexes, axis=1)
    link_hexes = dict(zip(links['link_id'], links['hexes']))

    return link_hexes


def get_facilitie_hexes(
    scenario_path: str,
    resolution: int
) -> Dict[str, str]:

    facilities = pd.read_csv(scenario_path+'/facilities.csv')
    facilities['geometry'] = facilities.apply(
        lambda row: Point(row['x'], row['y']),
        axis=1
    )
    facilities = gpd.GeoDataFrame(facilities)
    facilities.crs = "EPSG:2177"
    facilities = facilities.to_crs('EPSG:4327')
    facilities['hex'] = facilities.apply(
        lambda row: h3.geo_to_h3(
            row['geometry'].y,
            row['geometry'].x,
            resolution
        ),
        axis=1
    )

    return dict(zip(facilities['id'], facilities['hex']))


def count_events(
    scenario_path: str,
    resolution: int
) -> pd.DataFrame:

    link_hexes = get_links_hexes(scenario_path, resolution)
    facilities_hexes = get_facilitie_hexes(scenario_path, resolution)

    events = matsim.event_reader(
        scenario_path+'/output/output_events.xml.gz',
        types='entered link,actstart'
    )

    hexes = list(link_hexes.values())
    flat_list = []
    for sublist in hexes:
        for item in sublist:
            flat_list.append(item)
    hexes = set(flat_list + list(facilities_hexes.values()))

    events_list = {}
    for h3_index in hexes:
        events_list[h3_index] = defaultdict(int)

    for event in tqdm(events):
        if event['type'] == 'entered link':
            if event['vehicle'].startswith('person'):
                hexes = link_hexes[event['link']]
                for h3_index in hexes:
                    events_list[h3_index]['car'] += 1
        elif event['type'] == 'actstart':
            if event['actType'] == 'pt interaction':
                hexes = link_hexes[event['link']]
                for h3_index in hexes:
                    events_list[h3_index][event['actType']] += 1
            else:
                h3_index = facilities_hexes[event['facility']]
                events_list[h3_index][event['actType']] += 1

    df = pd.DataFrame(
        columns=[
            'h3', 'car', 'other', 'pt interaction',
            'school', 'university', 'work'
        ]
    )
    for key, value in events_list.items():
        value['h3'] = key
        df = df.append(value, ignore_index=True)
    events = df.fillna(0)

    return events


if __name__ == '__main__':

    data_path = sys.argv[1]
    scenario_name = sys.argv[2]
    try:
        resolution = int(sys.argv[3])
    except KeyError:
        resolution = 10

    tqdm.pandas()

    scenario_path = get_scenario_path(data_path, scenario_name)

    events = count_events(
        scenario_path=scenario_path,
        resolution=resolution
    )

    vis_path = scenario_path+'/vis'
    try:
        os.mkdir(vis_path)
    except FileExistsError:
        pass
    output_path = vis_path+'/count_hex_events'
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass

    events.to_csv(output_path+'/hex_events.csv', index=False)

    def _add_hex_geometry(row, hex_col='h3'):
        points = h3.h3_to_geo_boundary(
            row[hex_col], True
        )
        return Polygon(points)

    events['geometry'] = events.apply(
        _add_hex_geometry,
        axis=1
    )
    events = gpd.GeoDataFrame(events)
    events.crs = "EPSG:4327"
    events = events.to_crs('EPSG:2177')

    events.to_file(
        output_path+"/hex_events.geojson", driver='GeoJSON'
    )

    shp_output_path = output_path + '/shp'
    try:
        os.mkdir(shp_output_path)
    except FileExistsError:
        pass
    events.to_file(
        shp_output_path+"/hex_events.shp"
    )

import os
import sys
from collections import defaultdict

import geopandas as gpd
import matsim
import pandas as pd
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


if __name__ == "__main__":

    data_path = sys.argv[1]
    scenario_name = sys.argv[2]

    scenario_path = get_scenario_path(data_path, scenario_name)
    vis_path = scenario_path+'/vis'
    output_path = vis_path+'/custom'
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass

    # read shp files
    genet_files_path = vis_path + '/genet_standard_output'
    network_path = genet_files_path + '/network_links.geojson'
    network = gpd.read_file(network_path)

    # stream through events
    events = matsim.event_reader(
        scenario_path+'/output/output_events.xml.gz',
        types='entered link'
    )
    link_counts = defaultdict(int)
    for event in tqdm(events):
        if event['type'] == 'entered link':
            link_counts[event['link']] += 1
    link_counts = pd.DataFrame.from_dict(
        link_counts,
        orient='index',
        columns=['count']
    ).rename_axis('link_id')

    # merge data
    network_counts = network.rename(
        columns={'id': 'link_id'}
    ).merge(
        link_counts, on='link_id'
    )

    # save data
    network_counts.to_file(
        output_path+'/network_counts.json',
        driver="GeoJSON"
    )

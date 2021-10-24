import json
import os
import sys
from collections import defaultdict

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

    input_data_path = sys.argv[1]
    scenarios_path = sys.argv[2]
    scenario_name = sys.argv[3]

    scenario_path = get_scenario_path(scenarios_path, scenario_name)
    output_path = os.path.join(scenario_path, 'counts')
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass

    with open(
        os.path.join(
            input_data_path, 'traffic_counts/processed/points_links.json'
        ),
        'r'
    ) as f:
        points_links = json.load(f)

    links_to_points = {}
    for point, links in points_links.items():
        for link in links:
            links_to_points[link] = point

    selected_links = list(links_to_points.keys())

    counts = {}
    for point in list(points_links.keys()):
        counts[point] = defaultdict(list)

    events = matsim.event_reader(
        scenario_path+'/output/output_events.xml.gz',
        types='entered link'
    )

    for event in tqdm(events):
        if event['type'] == 'entered link':
            if event['link'] in selected_links:
                p = links_to_points[event['link']]
                h = int(event['time'] / 3600)
                counts[p][h].append(event['vehicle'])

    for point, hours in counts.items():
        for h, c in hours.items():
            counts[point][h] = len(set(c))

    counts_df = pd.DataFrame.from_dict(counts, orient='index')
    counts_df = counts_df.reset_index()
    counts_df = counts_df.melt(
        id_vars=['index'], var_name='hour', value_name='count'
    )
    counts_df = counts_df.fillna(0)

    counts_df.to_csv(
        os.path.join(output_path, 'counts_points.csv'),
        index=False
    )

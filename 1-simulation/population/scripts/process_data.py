import json
import sys
from typing import Set

import pandas as pd
from pandarallel import pandarallel
from tqdm import tqdm


def sample_building(
    df: pd.DataFrame,  # facilities
    region: int,
    tags: Set[str]
) -> str:
    df_filtered = df[(df['region_id'] == region) & df['tag'].isin(tags)]
    if len(df_filtered) > 0:
        sample = df_filtered.sample(1).iloc[0]
    else:
        df_filtered = df[df['tag'].isin(tags)]
        sample = df_filtered.sample(1).iloc[0]

    return sample['id']


if __name__ == "__main__":

    config_path = sys.argv[1]
    in_agents_path = sys.argv[2]
    in_travels_path = sys.argv[3]
    in_facilities_path = sys.argv[4]
    out_agents_path = sys.argv[5]
    out_travels_path = sys.argv[6]
    try:
        workers_num = int(sys.argv[7])
    except IndexError:
        workers_num = 1

    tqdm.pandas()
    if workers_num > 1:
        pandarallel.initialize(
            nb_workers=workers_num,
            progress_bar=True
        )

    # config
    with open(config_path, 'r') as f:
        config = json.load(f)
    for key, value in config['activities_tags'].items():
        config['activities_tags'][key] = set(value)

    # facilities
    facilities = pd.read_csv(in_facilities_path)

    # agents
    agents = pd.read_csv(in_agents_path, index_col=0)
    agents = agents.reset_index(drop=True)
    agents = agents.drop(columns='AgentID')
    if workers_num > 1:
        agents['home_building'] = agents.parallel_apply(
            lambda row: sample_building(
                facilities,
                row['home_region'],
                config['activities_tags']['home']
            ),
            axis=1
        )
    else:
        agents['home_building'] = agents.progress_apply(
            lambda row: sample_building(
                facilities,
                row['home_region'],
                config['activities_tags']['home']
            ),
            axis=1
        )
    agents_homes_dict = dict(zip(agents['agent_id'], agents['home_building']))
    agents.to_csv(out_agents_path, index=False)

    # travels
    travels = pd.read_csv(in_travels_path, index_col=0)
    travels = travels.replace(config['travels_activities_mapping'])
    modes = config['travels_modes_mapping']
    travels['transport_mode'] = travels.progress_apply(
        lambda row: modes['is_drive_eq_0'] if row['is_driver'] == 0
        else modes[str(row['transport_mode'])],
        axis=1
        )
    travels = travels.drop(columns=['is_driver'])
    if workers_num > 1:
        travels['dest_building'] = travels.parallel_apply(
            lambda row: agents_homes_dict[row['agent_id']]
            if row['dest_place_type'] == 'home'
            else sample_building(
                facilities,
                row['dest_region'],
                config['activities_tags'][row['dest_place_type']]
            ),
            axis=1
        )
    else:
        travels['dest_building'] = travels.progress_apply(
            lambda row: agents_homes_dict[row['agent_id']]
            if row['dest_place_type'] == 'home'
            else sample_building(
                facilities,
                row['dest_region'],
                config['activities_tags'][row['dest_place_type']]
            ),
            axis=1
        )
    travels['travel_start_time_s'] = travels.progress_apply(
        lambda row: row['travel_start_time'] * 60,
        axis=1
    )
    travels['travel_start_time'] = travels.progress_apply(
        lambda row: '{:02d}:{:02d}:00'.format(
            *divmod(row['travel_start_time'], 60)
        ),
        axis=1
    )
    travels.to_csv(out_travels_path, index=False)

import json
import sys
from typing import Set

import pandas as pd
from pandarallel import pandarallel
from tqdm import tqdm
from collections import defaultdict

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

def match_driver_passenger(
    agents: pd.DataFrame,
    travels: pd.DataFrame
) -> pd.DataFrame:
    """
    Maches dirvers and passengers
    Returns updated travels dataframe - passenger destinations are included in driver day schedule.

    Parameters: 
        agents  : DataFrame
        travels : DataFrame
    
    Returns:
        travels : DataFrame

    """
    df_merged = pd.merge(travels, agents[["home_region", "home_building", "agent_id"]], on="agent_id", how="left")
    df_merged["start_building"] = df_merged.groupby('agent_id')['dest_building'].shift()
    df_merged["start_building"] = df_merged["start_building"].fillna(df_merged["home_building"])

    df_drivers = df_merged[df_merged['transport_mode'] == 'car']
    travels = df_merged[df_merged['transport_mode'] != 'car']
    df_passengers = df_merged[df_merged['transport_mode'] == 'car_passenger']
    drivers_map = defaultdict(list)
    #dict key = (home_region, travel_start_time_hour)
    for _, row in df_drivers.iterrows():
        drivers_map[row['home_region'], row['travel_start_time'][0:2]].append(row.to_dict())
    df_passengers = df_passengers.head(10)
    for _, passenger in tqdm(df_passengers.iterrows(), total=df_passengers.shape[0]) :
        key = (passenger['home_region'], passenger['travel_start_time'][0:2])
        if key in drivers_map:
            possible_drivers = drivers_map.get(key)
            #drivers = [driver for driver in possible_drivers if driver['travel_start_time_s'] < passenger['travel_start_time_s']]
            driver = None
            if len(possible_drivers) is not 0:
                driver = possible_drivers[0]
                possible_drivers.remove(driver)
                drivers_map[key] = possible_drivers

            if driver is not None:
                # driver start -> passenger start
                ds_ps = driver
                ds_ps['dest_region'] = passenger['start_region']
                ds_ps['dest_building'] = passenger['start_building']
                ds_ps['dest_place_type'] = 'stop'
                travels = travels.append(ds_ps, ignore_index=True)

                # passenger start -> passenger dest
                ps_pd = passenger
                ps_pd['agent_id'] = driver['agent_id']
                ps_pd['dest_place_type'] = 'stop'
                ps_pd['start_place_type'] = 'stop'
                travels = travels.append(ps_pd, ignore_index=True)

                # passenger dest -> driver dest
                pd_dd = driver
                pd_dd['start_region'] = passenger['dest_region']
                pd_dd['start_building'] = passenger['dest_building']
                pd_dd['start_place_type'] = 'stop'
                travels = travels.append(ds_ps, ignore_index=True)
    for value in tqdm(drivers_map.values()):
        travels = travels.append(value)
    #travels = travels.drop(["home_region", "home_building"])
    return travels



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
    # travels = pd.read_csv(in_travels_path, index_col=0)
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
    travels['dest_activity_dur_time_s'] = travels.progress_apply(
        lambda row: row['dest_activity_dur_time'] * 60,
        axis=1
    )
    travels['dest_activity_dur_time'] = travels.progress_apply(
        lambda row: '{:02d}:{:02d}:00'.format(
            *divmod(row['dest_activity_dur_time'], 60)
        ),
        axis=1
    )
    travels.to_csv(out_travels_path, index=False)

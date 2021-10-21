import sys

import matsim
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':

    in_agents_path = sys.argv[1]
    in_travels_path = sys.argv[2]
    in_facilities_path = sys.argv[3]
    out_xml_path = sys.argv[4]

    agents = pd.read_csv(in_agents_path)
    travels = pd.read_csv(in_travels_path)
    facilities = pd.read_csv(in_facilities_path)

    agents_homes_dict = dict(
        zip(agents['agent_id'], agents['home_building'])
    )
    agents_age_sex_dict = dict(
        zip(agents['agent_id'], agents['age_sex'])
    )
    facilities_coords = dict(
        zip(facilities['id'], zip(facilities['x'], facilities['y']))
    )

    with open(out_xml_path, 'wb+') as f_write:

        writer = matsim.writers.PopulationWriter(f_write)

        writer.start_population()

        prev_agent_id = -1
        activity_type = None
        activity_dur_time = None

        for row_id, row in tqdm(
            travels.sort_values(['agent_id', 'travel_start_time']).iterrows(),
            total=len(travels)
        ):
            agent_id = row['agent_id']

            if agent_id != prev_agent_id:
                try:
                    building = agents_homes_dict[prev_agent_id]
                    (x, y) = facilities_coords[building]
                    writer.add_activity(
                        type='home',
                        x=x,
                        y=y,
                        facility_id=building
                    )
                    writer.end_plan()
                    writer.end_person()
                except KeyError:
                    pass
                writer.start_person(
                    "person_"+str(agent_id)+'_'+agents_age_sex_dict[agent_id]
                )
                writer.start_plan(selected=True)
                building = agents_homes_dict[agent_id]
                (x, y) = facilities_coords[building]
                writer.add_activity(
                    type='home',
                    x=x,
                    y=y,
                    facility_id=building,
                    end_time=row['travel_start_time_s']
                )
                writer.add_leg(mode=row['transport_mode'])
            else:
                writer.add_activity(
                    type=activity_type,
                    x=x,
                    y=y,
                    facility_id=building,
                    max_dur=activity_dur_time
                )
                writer.add_leg(mode=row['transport_mode'])

            building = row['dest_building']
            (x, y) = facilities_coords[building]
            activity_type = row['dest_place_type']
            activity_dur_time = row['dest_activity_dur_time_s']
            prev_agent_id = agent_id

        building = agents_homes_dict[prev_agent_id]
        (x, y) = facilities_coords[building]
        writer.add_activity(
            type='home',
            x=x,
            y=y,
            facility_id=building
        )
        writer.end_plan()
        writer.end_person()

        writer.end_population()

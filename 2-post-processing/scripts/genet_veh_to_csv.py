import gzip
import os
import shutil
import sys

from genet import read_matsim


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

    for file_path in [
        '/output/output_network.xml.gz',
        '/output/output_transitSchedule.xml.gz',
        '/output/output_vehicles.xml.gz'
    ]:
        with gzip.open(
            scenario_path+file_path,
            'rb'
        ) as f_in:
            with open(
                scenario_path+file_path.replace('.gz', ''),
                'wb'
            ) as f_out:
                shutil.copyfileobj(f_in, f_out)

    n = read_matsim(
        path_to_network=scenario_path+'/output/output_network.xml',
        epsg='epsg:2177',
        path_to_schedule=scenario_path+'/output/output_transitSchedule.xml',
        path_to_vehicles=scenario_path+'/output/output_vehicles.xml',
    )
    n.print()

    df = n.schedule.route_trips_to_dataframe()
    df.to_csv(scenario_path+'/vehicles.csv', index=None)

    df['id'] = df['vehicle_id']
    df['category'] = df.apply(
        lambda row: 'bus' if 'bus' in row['vehicle_id'] else 'tram',
        axis=1
    )
    df['tag'] = df['service_id']
    df['name'] = df.apply(
        lambda row: 'route_id-'+row['route_id']+'-trip_id-'+row['trip_id'],
        axis=1
    )
    df['region_id'] = None
    df['x'] = None
    df['y'] = None
    df = df[['id', 'category', 'tag', 'name', 'region_id', 'x', 'y']]
    df.to_csv(scenario_path+'/veh_as_facilities.csv', index=None)

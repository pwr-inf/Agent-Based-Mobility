import gzip
import os
import shutil
import sys

# from genet import Network
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
    # data_path = 'data-processing/data/'
    # scenario_name = 'others_10k'

    scenario_path = get_scenario_path(data_path, scenario_name)
    vis_path = scenario_path+'/vis'
    output_path = vis_path+'/genet_standard_output'
    try:
        os.mkdir(vis_path)
    except FileExistsError:
        pass
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass

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

    n.generate_standard_outputs(
        output_dir=output_path,
        include_shp_files=True
    )

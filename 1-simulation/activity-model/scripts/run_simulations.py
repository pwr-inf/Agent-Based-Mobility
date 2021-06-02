import json
import os
import sys
from distutils.dir_util import copy_tree
from typing import Dict

from src.runners import run


def change_dist(
    dist: Dict[str, Dict[str, float]],
    value: float
):

    if value != 0:

        if value < 0:
            value = abs(value)
            reverse = False
        else:
            reverse = True

        for dist_key in dist.keys():
            d = dist[dist_key]
            prev_key = None
            for k in sorted(d.keys(), reverse=reverse):
                if prev_key:
                    change_value = value * d[k]
                    d[prev_key] = d[prev_key] + change_value
                    d[k] = d[k] - change_value
                prev_key = k
            dist[dist_key] = d

    return dist


def get_output_folder_postfix(scenario):
    postfix = ''

    for [dist, value] in scenario:
        postfix += '_'
        postfix += dist.split('/')[-1]
        postfix += '_'
        postfix += str(value).replace('.', '_')

    return postfix


if __name__ == '__main__':

    scenarios_folder_path = sys.argv[1]
    assert type(scenarios_folder_path) == str
    assert len(scenarios_folder_path) > 0
    if not scenarios_folder_path.endswith('/'):
        scenarios_folder_path = scenarios_folder_path + '/'
    assert os.path.exists(scenarios_folder_path)

    scenarios_name = sys.argv[2]
    assert type(scenarios_name) == str
    assert len(scenarios_name) > 0
    assert not scenarios_name.endswith('.json')

    input_data_folder_path = sys.argv[3]
    assert type(input_data_folder_path) == str
    assert len(input_data_folder_path) > 0
    if not input_data_folder_path.endswith('/'):
        input_data_folder_path = input_data_folder_path + '/'
    assert os.path.exists(input_data_folder_path)

    results_path = sys.argv[4]
    assert type(results_path) == str
    assert len(results_path) > 0
    if not results_path.endswith('/'):
        results_path = results_path + '/'

    population = int(sys.argv[5])
    assert population > 0

    num_simulations = int(sys.argv[6])
    assert num_simulations > 0

    num_processes = int(sys.argv[7])
    assert num_processes > 0

    scenarios_full_path = scenarios_folder_path + scenarios_name + '.json'
    with open(scenarios_full_path, 'r') as f:
        scenarios = json.load(f)['scenarios']

    for i, simulation_scenario in enumerate(scenarios):

        new_distributions_path = input_data_folder_path + scenarios_name \
            + '_' + str(i + 1)
        copy_tree(
            input_data_folder_path + 'base_distributions',
            new_distributions_path
        )

        for [dist_name, value] in simulation_scenario:
            if dist_name.endswith('-up'):
                dist_name = dist_name.replace('-up', '')
            elif dist_name.endswith('-down'):
                value = -1 * value
                dist_name = dist_name.replace('-down', '')
            else:
                raise Exception('No -up or -down in distribution name!')

            dist_path = new_distributions_path + '/' + dist_name + '.json'

            with open(dist_path, 'r') as f:
                dist = json.load(f)
            dist = change_dist(dist, value)
            with open(dist_path, 'w') as f:
                json.dump(dist, f)

        output_folder_name = scenarios_name + '_' + str(i+1) \
            + get_output_folder_postfix(simulation_scenario)
        output_folder_path = results_path + output_folder_name
        os.mkdir(output_folder_path)

        print('Starts '+str(i+1)+' simulation...')
        run(
            in_dir_path=new_distributions_path,
            out_dir_path=output_folder_path,
            num_agents=population,
            sim_start_time=4*60,
            sim_step_time=60,
            sim_end_time=24*60,
            num_simulations=num_simulations,
            num_processes=num_processes
        )
        print('Finished '+str(i+1)+' simulation.')

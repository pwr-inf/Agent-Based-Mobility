import collections
import json
import os
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from random import sample

import numpy as np
import pandas as pd
import pymongo
from graph_tool.all import *
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
    population = int(sys.argv[3])
    scenario_path = get_scenario_path(data_path, scenario_name)

    mongo_user = os.environ['MONGO_USER']
    mongo_password = os.environ['MONGO_PASSWORD']
    mongo_host = os.environ['MONGO_HOST']
    mongo_port = os.environ['MONGO_PORT']
    db_name = os.environ['MONGO_DB_NAME']
    collection_name = os.environ['MONGO_COLLECTION_NAME']
    buffor_size = int(os.environ['MONGO_BUFFOR_SIZE'])

    mongo_uri = ''.join([
        'mongodb://',
        mongo_user,
        ':',
        mongo_password,
        '@',
        mongo_host,
        ':',
        mongo_port
    ])

    myclient = pymongo.MongoClient(mongo_uri)
    mydb = myclient[db_name]
    mongo_collection = mydb[collection_name]

    db_stats = mydb.command('dbstats')

    # read mongo data

    interactions_in_time_window_size = 60 * 60
    interactions_in_time = defaultdict(int)
    interactions_by_type_in_time = defaultdict(lambda: defaultdict(int))
    interactions_by_age_in_time = defaultdict(lambda: defaultdict(int))

    interactions_by_age_group = defaultdict(int)
    interactions_by_age_group_by_agent = defaultdict(lambda: defaultdict(int))

    interactions_by_type = defaultdict(int)

    interactions_by_activity_type = defaultdict(int)
    interactions_by_activity_type_by_agent = defaultdict(lambda: defaultdict(int))

    interactions_by_region = defaultdict(int)
    interactions_by_region_by_agent = defaultdict(lambda: defaultdict(int))

    age_age_interactions = defaultdict(lambda: defaultdict(int))
    act_act_interactions = defaultdict(lambda: defaultdict(int))

    interactions_by_age_by_agent_by_age = {}
    interactions_by_age_by_agent_by_age['6-15'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_agent_by_age['16-19'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_agent_by_age['16-19'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_agent_by_age['20-24'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_agent_by_age['25-44'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_agent_by_age['45-60 F / 45-65 M'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_agent_by_age['61+ F / 66+ M'] = defaultdict(lambda: defaultdict(int))

    interactions_by_age_by_type = defaultdict(lambda: defaultdict(int))

    interactions_by_age_by_type_by_agent = {}
    interactions_by_age_by_type_by_agent['6-15'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_type_by_agent['16-19'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_type_by_agent['16-19'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_type_by_agent['20-24'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_type_by_agent['25-44'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_type_by_agent['45-60 F / 45-65 M'] = defaultdict(lambda: defaultdict(int))
    interactions_by_age_by_type_by_agent['61+ F / 66+ M'] = defaultdict(lambda: defaultdict(int))

    ug = Graph(directed=False)

    for document in tqdm(mongo_collection.find(), total=db_stats['objects']):

        # graph

        e = ug.add_edge(
            int(document['agent_1_id']),
            int(document['agent_2_id'])
        )

        if document['agent_1_age'] == '45-60' or document['agent_1_age'] == '45-65':
            agent_1_age = '45-60 F / 45-65 M'
        elif document['agent_1_age'] == '61-x' or document['agent_1_age'] == '66-x':
            agent_1_age = '61+ F / 66+ M'
        else:
            agent_1_age = document['agent_1_age']

        if document['agent_2_age'] == '45-60' or document['agent_2_age'] == '45-65':
            agent_2_age = '45-60 F / 45-65 M'
        elif document['agent_2_age'] == '61-x' or document['agent_2_age'] == '66-x':
            agent_2_age = '61+ F / 66+ M'
        else:
            agent_2_age = document['agent_2_age']

        interaction_start_window = int(document['interaction_start_time_s'] / interactions_in_time_window_size)
        interaction_windows_number = max(1, round(document['interaction_dur_time_s'] / interactions_in_time_window_size))
        for w in range(
            interaction_start_window,
            interaction_start_window + interaction_windows_number
        ):
            interactions_in_time[w] += 1
            interactions_by_type_in_time[document['interaction_type']][w] += 1
            interactions_by_age_in_time[agent_1_age][w] += 1
            interactions_by_age_in_time[agent_2_age][w] += 1

        interactions_by_age_group[agent_1_age] += 1
        interactions_by_age_group[agent_2_age] += 1
        interactions_by_age_group_by_agent[agent_1_age][document['agent_1_id']] += 1
        interactions_by_age_group_by_agent[agent_2_age][document['agent_2_id']] += 1

        activities = document['interaction_type'].split('--')
        interactions_by_activity_type[activities[0]] += 1
        interactions_by_activity_type[activities[1]] += 1
        interactions_by_activity_type_by_agent[activities[0]][document['agent_1_id']] += 1
        interactions_by_activity_type_by_agent[activities[1]][document['agent_2_id']] += 1

        interactions_by_region[document['facility_region']] += 1
        interactions_by_region_by_agent[document['facility_region']][document['agent_1_id']] += 1
        interactions_by_region_by_agent[document['facility_region']][document['agent_2_id']] += 1

        age_age_interactions[agent_1_age][agent_2_age] += 1
        age_age_interactions[agent_2_age][agent_1_age] += 1
        act_act_interactions[activities[0]][activities[1]] += 1
        act_act_interactions[activities[1]][activities[0]] += 1
        interactions_by_age_by_agent_by_age[agent_1_age][document['agent_1_id']][agent_2_age] += 1
        interactions_by_age_by_agent_by_age[agent_2_age][document['agent_2_id']][agent_1_age] += 1

        interactions_by_age_by_type[agent_1_age][activities[0]] += 1
        interactions_by_age_by_type[agent_2_age][activities[1]] += 1

        interactions_by_age_by_type_by_agent[agent_1_age][activities[0]][document['agent_1_id']] += 1
        interactions_by_age_by_type_by_agent[agent_2_age][activities[1]][document['agent_2_id']] += 1

    myclient.close()

    output = {}

    # graph properties

    # remove nodes with degree == 0

    degrees = ug.get_total_degrees(list(ug.vertices()))
    active_nodes = ug.new_vertex_property('bool')
    for i in range(population):
        if degrees[i] > 0:
            active_nodes[i] = True
        else:
            active_nodes[i] = False

    sub_ug = GraphView(ug, vfilt=active_nodes)

    # nodes number

    nodes_number = len(list(sub_ug.vertices()))

    output['nodes_number'] = nodes_number

    # components

    components = Counter(list(label_components(sub_ug)[0]))

    output['components_number'] = len(components)
    output['max_component_share'] = max(list(components.values())) / len(list(sub_ug.vertices()))

    # density

    output['density'] = db_stats['objects'] / (nodes_number * (nodes_number - 1))

    # degree

    output['degree_mean'] = vertex_average(sub_ug, 'total')[0]

    # degree histogram

    y, x = vertex_hist(sub_ug, 'total')

    output['degree_histogram_x'] = x[1:]
    output['degree_histogram_y'] = y

    # asortativity

    output['asortativity'] = assortativity(sub_ug, 'total')[0]

    # clustering coefficient

    output['clusterin_coefficient'] = global_clustering(sub_ug)[0]

    # modularity
    # TODO

    # shortest paths

    largest_comp = GraphView(sub_ug, vfilt=label_largest_component(sub_ug))
    vertices_list = list(largest_comp.vertices())

    lens = []
    for i in tqdm(range(1000)):
        source = sample(vertices_list, 1)[0]
        targets = sample(vertices_list, 1)
        lens += list(shortest_distance(largest_comp, source=source, target=targets))

    output['shortest_paths'] = lens

    # vis 1

    # interactions in time

    interactions_in_time = collections.OrderedDict(sorted(interactions_in_time.items()))

    output['all_interactions_in_time'] = {}
    output['all_interactions_in_time']['x'] = list(interactions_in_time.keys())
    output['all_interactions_in_time']['y'] = list(interactions_in_time.values())

    # interactions in time by type

    # work--work

    interactions = interactions_by_type_in_time['work--work']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_type'] = {}
    output['interactions_in_time_by_type']['work--work'] = {}
    output['interactions_in_time_by_type']['work--work']['x'] = list(interactions.keys())
    output['interactions_in_time_by_type']['work--work']['y'] = list(interactions.values())

    # school-school

    interactions = interactions_by_type_in_time['school--school']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_type']['school--school'] = {}
    output['interactions_in_time_by_type']['school--school']['x'] = list(interactions.keys())
    output['interactions_in_time_by_type']['school--school']['y'] = list(interactions.values())

    # univ--univ

    interactions = interactions_by_type_in_time['university--university']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_type']['univ--univ'] = {}
    output['interactions_in_time_by_type']['univ--univ']['x'] = list(interactions.keys())
    output['interactions_in_time_by_type']['univ--univ']['y'] = y=list(interactions.values())

    # pt--pt

    interactions = interactions_by_type_in_time['public_transport--public_transport']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_type']['pt--pt'] = {}
    output['interactions_in_time_by_type']['pt--pt']['x'] = list(interactions.keys())
    output['interactions_in_time_by_type']['pt--pt']['y'] = list(interactions.values())

    # interactions in time by age group

    # 6-15

    interactions = interactions_by_age_in_time['6-15']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_age'] = {}
    output['interactions_in_time_by_age']['6-15'] = {}
    output['interactions_in_time_by_age']['6-15']['x'] = list(interactions.keys())
    output['interactions_in_time_by_age']['6-15']['y'] = list(interactions.values())

    # 16-19

    interactions = interactions_by_age_in_time['16-19']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_age']['16-19'] = {}
    output['interactions_in_time_by_age']['16-19']['x'] = list(interactions.keys())
    output['interactions_in_time_by_age']['16-19']['y'] = list(interactions.values())

    # 20-24

    interactions = interactions_by_age_in_time['20-24']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_age']['20-24'] = {}
    output['interactions_in_time_by_age']['20-24']['x'] = list(interactions.keys())
    output['interactions_in_time_by_age']['20-24']['y'] = list(interactions.values())

    # 25-44

    interactions = interactions_by_age_in_time['25-44']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_age']['25-44'] = {}
    output['interactions_in_time_by_age']['25-44']['x'] = list(interactions.keys())
    output['interactions_in_time_by_age']['25-44']['y'] = list(interactions.values())

    # 45-60 F / 45-65 M

    interactions = interactions_by_age_in_time['45-60 F / 45-65 M']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_age']['45-60 F / 45-65 M'] = {}
    output['interactions_in_time_by_age']['45-60 F / 45-65 M']['x'] = list(interactions.keys())
    output['interactions_in_time_by_age']['45-60 F / 45-65 M']['y'] = list(interactions.values())

    # 61+ F / 66+ M

    interactions = interactions_by_age_in_time['61+ F / 66+ M']
    interactions = collections.OrderedDict(sorted(interactions.items()))

    output['interactions_in_time_by_age']['61+ F / 66+ M'] = {}
    output['interactions_in_time_by_age']['61+ F / 66+ M']['x'] = list(interactions.keys())
    output['interactions_in_time_by_age']['61+ F / 66+ M']['y'] = list(interactions.values())

    # in age groups mean

    d = {}
    d['6-15'] = np.array(list(interactions_by_age_group_by_agent['6-15'].values()))
    d['16-19'] = np.array(list(interactions_by_age_group_by_agent['16-19'].values()))
    d['20-24'] = np.array(list(interactions_by_age_group_by_agent['20-24'].values()))
    d['25-44'] = np.array(list(interactions_by_age_group_by_agent['25-44'].values()))
    d['45-60 F / 45-65 M'] = np.array(list(interactions_by_age_group_by_agent['45-60 F / 45-65 M'].values()))
    d['61+ F / 66+ M'] = np.array(list(interactions_by_age_group_by_agent['61+ F / 66+ M'].values()))

    output['in_age_groups'] = {}
    output['in_age_groups']['6-15'] = d['6-15']
    output['in_age_groups']['16-19'] = d['16-19']
    output['in_age_groups']['20-24'] = d['20-24']
    output['in_age_groups']['25-44'] = d['25-44']
    output['in_age_groups']['45-60 F / 45-65 M'] = d['45-60 F / 45-65 M']
    output['in_age_groups']['61+ F / 66+ M'] = d['61+ F / 66+ M']

    # by type mean

    output['by_type'] = {}

    for key, value in interactions_by_activity_type_by_agent.items():
        a = np.array(list(value.values()))
        output['by_type'][key] = a

    # by basic types mean

    output['by_basic_type'] = {}

    d = defaultdict(lambda: defaultdict(int))

    for act, value in interactions_by_activity_type_by_agent.items():
        for agent, cnts in interactions_by_activity_type_by_agent[act].items():

            if act == 'school' or act == 'univeristy':
                d['school / university'][agent] += cnts
            elif act == 'public_transport':
                d['transport'][agent] += cnts
            elif act == 'work':
                d['work'][agent] += cnts
            else:
                d['other'][agent] += cnts

    for key in ['other', 'school / university', 'transport', 'work']:
        a = np.array(list(d[key].values()))
        output['by_basic_type'][key] = a

    # type--type total matrix

    d = deepcopy(act_act_interactions)
    df = pd.DataFrame.from_dict(d).fillna(0)

    output['type_type_matrix'] = df.to_json()

    # age-age total matrix

    map_age = {
        '6-15': '6-15',
        '16-19': '16-19',
        '20-24': '20-24',
        '25-44': '25-44',
        '45-60 F / 45-65 M': '45-60 F / 45-65 M',
        '61+ F / 66+ M': '61+ F / 66+ M'
    }

    d_to_vis = defaultdict(lambda : defaultdict(int))
    for k1 in map_age.keys():
        for k2 in list(map_age.keys())[::-1]:
            d_to_vis[map_age[k1]][map_age[k2]] += age_age_interactions[k1][k2]

    df = pd.DataFrame.from_dict(d_to_vis).fillna(0)

    output['age_age_matrix'] = df.to_json()

    # age-age mean

    output['age_age'] = {}

    def plot_age_age(age_group):
        d = defaultdict(list)

        output['age_age'][age_group] = {}

        interactions = interactions_by_age_by_agent_by_age[age_group]

        for agent, values in interactions.items():
            for age in ['6-15', '16-19', '20-24', '25-44', '45-60 F / 45-65 M', '61+ F / 66+ M']:
                d[age].append(values[age])

        for key, value in d.items():
            output['age_age'][age_group] = value


    plot_age_age('6-15')
    plot_age_age('16-19')
    plot_age_age('20-24')
    plot_age_age('25-44')
    plot_age_age('45-60 F / 45-65 M')
    plot_age_age('61+ F / 66+ M')

    # basic types by age mean

    output['basic_types_by_age'] = {}

    def plot_type_by_age_mean(age_group):

        output['basic_types_by_age'][age_group] = {}
        others = []

        data = interactions_by_age_by_type_by_agent[age_group]

        for act, value in data.items():

            if act == 'school' or act == 'univeristy':
                output['basic_types_by_age'][age_group]['school / university'] = list(value.values())
            elif act == 'public_transport':
                output['basic_types_by_age'][age_group]['public_transport'] = list(value.values())
            elif act == 'work':
                output['basic_types_by_age'][age_group]['work'] = list(value.values())
            else:
                others = others + list(value.values())

        output['basic_types_by_age'][age_group]['other'] = others

    plot_type_by_age_mean('6-15')
    plot_type_by_age_mean('16-19')
    plot_type_by_age_mean('20-24')
    plot_type_by_age_mean('25-44')
    plot_type_by_age_mean('45-60 F / 45-65 M')
    plot_type_by_age_mean('61+ F / 66+ M')

    # vis 2

    output['interactions_by_region'] = interactions_by_region
    output['interactions_by_region_by_agent'] = {}

    for region, d in interactions_by_region_by_agent.items():

        degrees = []
        for agent, value in d.items():
            degrees.append(value)

        output['interactions_by_region_by_agent'][region] = degrees

    out_path = os.path.join(scenario_path, 'cs_out.json')
    with open (out_path, 'w') as f:
        json.dump(output, f)

import itertools
import json
import os
import shutil
import sys
from typing import List


def prepare_scenarios(
    distributions: List[str],
    values_of_change: List[float]
):
    lists_to_product = []
    for dist in distributions:
        lists_to_product.append(
            list(itertools.product([dist], values_of_change))
        )

    all_combinations = list(itertools.product(*lists_to_product))

    return all_combinations


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    while len(out) > num:
        la = out.pop(-1)
        for el in la:
            out[-1].append(el)

    return out


if __name__ == '__main__':

    distributions = sys.argv[1]
    assert type(distributions) == str
    assert len(distributions) > 0
    assert ' ' not in distributions
    assert distributions.startswith('[')
    assert distributions.endswith(']')
    distributions = list(
        map(str, distributions.strip('[]').split(','))
    )

    values_of_change = sys.argv[2]
    assert type(values_of_change) == str
    assert len(values_of_change) > 0
    assert ' ' not in values_of_change
    assert values_of_change.startswith('[')
    assert values_of_change.endswith(']')
    values_of_change = list(
        map(float, values_of_change.strip('[]').split(','))
    )

    services_number = int(sys.argv[3])

    output_dir = sys.argv[4]
    assert type(output_dir) == str
    assert len(output_dir) > 0
    if not output_dir.endswith('/'):
        output_dir = output_dir + '/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    elif len(os.listdir(output_dir)) > 0:
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    scenarios = prepare_scenarios(
        distributions,
        values_of_change
    )

    chunked_scenarios = chunkIt(scenarios, services_number)

    for i, scenarios_list in enumerate(chunked_scenarios):
        with open(output_dir + 'scenarios_' + str(i+1) + '.json', 'w') as f:
            json.dump({'scenarios': scenarios_list}, f)

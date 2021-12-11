import os
import sys

import matsim
from src.data.activity import ActType
from src.data.contact_structure import ContactStructure
from src.data.facilities import Facilities
from src.data.population import Population


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

    facilities_path = scenario_path + '/facilities.csv'
    veh_as_facilities_path = scenario_path + '/veh_as_facilities.csv'
    agents_path = scenario_path + '/agents.csv'
    events_path = scenario_path + '/output/output_events.xml.gz'

    facilities = Facilities()
    facilities.read_csv(facilities_path)
    facilities.read_csv(veh_as_facilities_path)

    population = Population()
    population.read_csv(agents_path, facilities)

    cs = ContactStructure()
    cs.add_layer('work')
    cs.add_layer('school')
    cs.add_layer('university')
    cs.add_layer('public_transport')
    cs.add_layer('gastronomy')
    cs.add_layer('culture_and_entertainment')
    cs.add_layer('adults_entertainment')
    cs.add_layer('sport')
    cs.add_layer('official_matters')
    cs.add_layer('other')
    cs.add_layer('grocery_shopping')
    cs.add_layer('other_shopping')
    cs.add_layer('pharmacy')
    cs.add_layer('healthcare')
    cs.add_layer('services')
    cs.add_layer('leisure_time_schools')
    cs.add_layer('religion')

    reader = matsim.event_reader(
        events_path,
        types='actstart,actend,PersonEntersVehicle,PersonLeavesVehicle'
    )
    cs.read_from_events(reader, population, facilities)

    layers = [
        ActType.WORK,
        ActType.SCHOOL,
        ActType.UNIV,
        ActType.OTHER,
        ActType.PT,
        ActType.GASTRONOMY,
        ActType.CAE,
        ActType.AE,
        ActType.SPORT,
        ActType.OM,
        ActType.OTHER,
        ActType.GS,
        ActType.OS,
        ActType.PHARMACY,
        ActType.HEALTHCARE,
        ActType.SERVICES,
        ActType.LTS,
        ActType.RELIGION
    ]

    interactions = cs.agent_agent_multi_graph(layers)

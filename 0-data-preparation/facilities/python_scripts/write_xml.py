import sys

import matsim
import pandas as pd
from tqdm import tqdm

if __name__ == "__main__":

    in_csv_path = sys.argv[1]
    out_xml_path = sys.argv[2]

    facilities = pd.read_csv(in_csv_path)

    with open(out_xml_path, 'wb+') as f_write:
        writer = matsim.writers.FacilitiesWriter(f_write)

        writer.start_facilities()

        for row_id, facility in tqdm(
            facilities.iterrows(),
            total=len(facilities)
        ):
            writer.start_facility(
                facility_id=facility['id'],
                x=facility['x'],
                y=facility['y']
            )
            writer.end_facility()

        writer.end_facilities()

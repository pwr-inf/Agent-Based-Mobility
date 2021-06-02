import sys

import geopandas as gpd

if __name__ == "__main__":

    regions_input_path = data_path = sys.argv[1]
    regions_output_path = data_path = sys.argv[2]

    regions = gpd.read_file(regions_input_path)
    regions = regions[['NUMBER', 'NAME', 'geometry']]
    regions = regions.rename(columns={'NUMBER': 'region_id', 'NAME': 'name'})
    regions = regions.to_crs('EPSG:2177')
    # regions['centroid'] = regions['geometry'].centroid

    regions.to_file(regions_output_path)

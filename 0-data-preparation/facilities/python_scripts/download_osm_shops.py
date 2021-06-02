import osmnx as ox
import sys


def download_shops(
    output_path: str
):
    ox.settings.timeout = 600
    tags = {'shop': True}
    gdf = ox.geometries_from_place('Wrocław', tags)
    columns = ['osmid', 'shop', 'name', 'geometry']
    gdf_sub = gdf[columns]
    gdf_sub = gdf_sub.to_crs("EPSG:2177")
    gdf_sub['geometry'] = gdf_sub['geometry'].centroid

    gdf_sub.to_file(output_path)


if __name__ == "__main__":

    output_path = sys.argv[1]

    download_shops(output_path)

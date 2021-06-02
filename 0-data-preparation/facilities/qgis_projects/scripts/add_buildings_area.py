DATA_DIR = './Projects/ABMobility/facilities/data/vis/qgis_buildings_area'

project = QgsProject.instance()

files = os.listdir(DATA_DIR)
files.sort()
for f in files:
    if f.endswith('shp'):

        lay = QgsVectorLayer(
            DATA_DIR+'/'+f,
            f.replace('.shp', ''),
            "ogr"
        )
        lay.renderer().symbol().setColor(QColor("blue"))
        project.addMapLayer(lay)

DATA_DIR = './Projects/ABMobility/facilities/data/vis/qgis_amenities_tags'
GROUP_NAME = 'amenity'
LABEL_FIELD_NAME = 'amenity'

project = QgsProject.instance()
root = project.layerTreeRoot()
# group = root.addGroup(GROUP_NAME)
group_with_labels = root.addGroup(GROUP_NAME + ' with labels')

files = os.listdir(DATA_DIR)
files.sort()
for f in files:
    if f.endswith('shp'):

        # lay = QgsVectorLayer(
        #     DATA_DIR+'/'+f,
        #     f.replace('.shp', ''),
        #     "ogr"
        # )
        # project.addMapLayer(lay, False)
        # group.addLayer(lay)

        lay = QgsVectorLayer(
            DATA_DIR+'/'+f,
            f.replace('.shp', ''),
            "ogr"
        )
        project.addMapLayer(lay, False)
        group_with_labels.addLayer(lay)
        label_settings = QgsPalLayerSettings()
        label_settings.drawLabels = True
        label_settings.fieldName = LABEL_FIELD_NAME
        lay.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
        lay.setLabelsEnabled(True)
        lay.triggerRepaint()

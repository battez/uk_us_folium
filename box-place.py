'''
    plot some Twitter Places on a Folium map
'''
import csv
import math
import pandas as pd
import os.path

# Map related:
import folium
# print(folium.__version__)
import branca.colormap as cm


# FeatureGroup, Marker, LayerControl


# data set-up:
locs = 'places_grouped.csv' # lats longs and names
dfin = pd.read_csv(locs)
df = dfin.set_index(['_id'])
all = df.index.tolist()
# print(df.head(2))
# print(df.columns)

# MAPS and their params
filename = os.path.basename(__file__)
output_osm = filename.split('.')[0] + '.html'
zoom_start = 7
centre = [df['place.0.bounding_box.coordinates.0.0.1'].mean(), df['place.0.bounding_box.coordinates.0.1.0'].mean()] # Pennsylvania-ish
df = df.sort_values(['place.0.place_type'], ascending=[True])


fmap = folium.Map(location=centre, zoom_start=zoom_start, tiles="Cartodb Positron")

# box styles
styles = {'opacity' : 0.1, 'color' : '#323232', 'fill_color':'red' }
threshold = 4000 # max no of count we will allow
linear = cm.LinearColormap(['green', 'yellow', 'red'],
                           vmin=1, vmax=500)

idx = 0
remove = ['country']
curr_place_type = 'a'
feature_group = dict()

# fixme - will calculate the color based on the count (tweet intensity)
for row in df.itertuples():
    idx += 1

    # popup text
    index, count, name, place_type = row[:4]

    # skip some values that just screw up the map
    if (not isinstance(place_type, str)) or (not isinstance(name, str)) or\
     (place_type in remove) or (name[-6:] == 'Canada') or (count > threshold):
        continue

    


    
    # bounding box corners for every Place
    bottom_left = list()
    top_right = list()
    
    # boxes coords:
    bottom_left.append(row[5])
    bottom_left.append(row[4])
    top_right.append(row[9])
    top_right.append(row[8])
    
    
    string = '%s: %d tweets. (type:%s)' % (name, count, place_type)
    folium.features.RectangleMarker(
        bounds=[bottom_left, top_right],
        color=styles['color'],
        fill_color=linear(count),
        fill_opacity=styles['opacity'],
        popup=string).add_to(fmap)





# output both maps
fmap.save(output_osm)
    

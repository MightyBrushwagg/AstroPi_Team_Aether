import exif
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def convertToDecimal(long_lat, reference):
    total = long_lat[0] + long_lat[1]/60 + long_lat[2]/3600
    if reference in ["W", "S"]:
        total *= -1

    return total

directory = r"C:\Users\xavie\OneDrive\Desktop\Aether\Aether\aether_pictures"

with open(r"C:\Users\xavie\OneDrive\Desktop\Aether\Aether\aether_pictures\aether_image271.jpg", "rb") as image_file:
    myimage = exif.Image(image_file)
print(convertToDecimal(myimage.gps_latitude, myimage.gps_latitude_ref))
print(convertToDecimal(myimage.gps_longitude, myimage.gps_longitude_ref))
print(myimage.gps_latitude)
print(myimage.gps_latitude_ref)
print(myimage.gps_longitude)
print(myimage.gps_longitude_ref)

with open(r'C:\Users\xavie\OneDrive\Desktop\Aether\Aether\coords.csv', 'w',newline="") as f:
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            with open(os.path.join(directory, filename), "rb") as image_file:
                myimage = exif.Image(image_file)

            
                #create the csv writer
                writer = csv.writer(f, lineterminator='\n')
                row = [filename, convertToDecimal(myimage.gps_longitude, myimage.gps_longitude_ref), convertToDecimal(myimage.gps_latitude, myimage.gps_latitude_ref)]
                #write a row to the csv file
                writer.writerow(row)

                #print(myimage.gps_latitude)
                #print(myimage.gps_latitude_ref)
                #print(myimage.gps_longitude)
                #print(myimage.gps_longitude_ref)

#                print(convertToDecimal(myimage.gps_latitude, myimage.gps_latitude_ref))
#                print(convertToDecimal(myimage.gps_longitude, myimage.gps_longitude_ref))

import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import shapely
import warnings
from shapely.errors import ShapelyDeprecationWarning

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

df = pd.read_csv(r"C:\Users\xavie\OneDrive\Desktop\Aether\Aether\coords.csv", delimiter=',', skiprows=0, low_memory=False)

geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = GeoDataFrame(df, geometry=geometry)   

#this is a simple map that goes with geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color='red', markersize=15);
plt.show()

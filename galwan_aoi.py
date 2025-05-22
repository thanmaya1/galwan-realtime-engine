# galwan_aoi.py

from sentinelhub import BBox, CRS

# Galwan Valley approx center
center_lat = 34.678
center_lon = 79.581

# Define bounding box: 0.05 degrees ~ 5.5km at this latitude
aoi = BBox(bbox=[center_lon - 0.05, center_lat - 0.05,
                 center_lon + 0.05, center_lat + 0.05],
           crs=CRS.WGS84)
print(aoi)



from sentinelhub import BBox, CRS

# Bakhmut, Ukraine approx center coordinates
center_lat = 48.5848
center_lon = 37.9980

# Define bounding box: Covers approx 10 km²
aoi = BBox(bbox=[center_lon - 0.05, center_lat - 0.05,
                 center_lon + 0.05, center_lat + 0.05],
           crs=CRS.WGS84)

print(aoi)  # Confirm the bounding box
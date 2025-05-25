import rasterio
from rasterio.transform import from_bounds
from sentinelhub import BBox, CRS

# Input PNG file path
input_png = "C:\\Users\\anon\\OneDrive\\Desktop\\eatgrass\\b81898d9afeca1c33f353f827fca42bc\\response.png"

# Output GeoTIFF file path
output_tiff = "C:\\Users\\anon\\OneDrive\\Desktop\\eatgrass\\bakhmut_image.tif"

# Define AOI for Bakhmut, Ukraine (approx. 10 km²)
center_lat = 48.5848
center_lon = 37.9980
aoi = BBox(
    bbox=[center_lon - 0.05, center_lat - 0.05, 
          center_lon + 0.05, center_lat + 0.05],
    crs=CRS.WGS84
)

print(f"🗺️ AOI BBox: {aoi}")

# Extract bounding box coordinates correctly
minx, miny = aoi.lower_left  # Corrected attribute access
maxx, maxy = aoi.upper_right  # Corrected attribute access
bbox_coords = (minx, miny, maxx, maxy)  # Correct order for rasterio

# Define transformation based on bounding box
transform = from_bounds(*bbox_coords, width=1024, height=1024)

# Open the PNG image
with rasterio.open(input_png) as src:
    profile = src.profile
    data = src.read()

# Update profile for GeoTIFF output
profile.update({
    'driver': 'GTiff',
    'height': 1024,
    'width': 1024,
    'transform': transform,
    'crs': 'EPSG:4326'
})

# Save the image as GeoTIFF
with rasterio.open(output_tiff, 'w', **profile) as dst:
    dst.write(data)

print("✅ Successfully converted to GeoTIFF:", output_tiff)
from sentinelhub import (
    SentinelHubRequest, SHConfig, DataCollection,
    MimeType, BBox, CRS
)
from bakhmut_aoi import aoi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
CLIENT_ID = os.getenv("SH_CLIENT_ID")
CLIENT_SECRET = os.getenv("SH_CLIENT_SECRET")

# Configure access
config = SHConfig()
config.sh_client_id = CLIENT_ID
config.sh_client_secret = CLIENT_SECRET
config.save()

# **True-Color Evalscript for Natural Imagery**
evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["B04", "B03", "B02"], // Red, Green, Blue (true-color)
    output: { bands: 3 }
  };
}
function evaluatePixel(sample) {
  return [sample.B04, sample.B03, sample.B02];  // Removes infrared distortion
}
"""

# **Build the Sentinel-2 Request**
request = SentinelHubRequest(
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=("2025-05-20", "2025-05-23")  # ✅ Adjust time range as needed
        )
    ],
    responses=[
        SentinelHubRequest.output_response("default", MimeType.PNG)  # PNG for highest quality
    ],
    bbox=aoi,
    size=(1024, 1024),  # High resolution for sharp imagery
    config=config,
    data_folder="C:/Users/anon/OneDrive/Desktop/eatgrass"
)

# Run request
image = request.get_data(save_data=True)[0]
print("🚀 Bakhmut true-color image downloaded successfully!")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from tqdm import tqdm
from screenshot_capturer import capture_location_screenshots

# Inputs
del_lon = 0.0020116000  # change in longitude per snapshot
del_lat = 0.0008818999  # change in latitude per snapshot
central_lat, central_lon = 28.63272109, 77.21953181  # latitude & longitude for central C.P.
grid_dim = 1000  # in meters

def divide_grid(central_lat, central_lon, grid_dim, del_lon, del_lat):
    import math

    # Calculate the number of cells in each direction
    num_cells_lon = math.ceil(grid_dim / (del_lon * 111320))  # Converting degrees to meters
    num_cells_lat = math.ceil(grid_dim / (del_lat * 110540))  # Converting degrees to meters

    # Display necessary details
    print(f"Central latitude and longitude: {central_lat, central_lon}")
    print(f"Longitude change per cell: {del_lon:.8f} degrees")
    print(f"Latitude change per cell: {del_lat:.8f} degrees")
    print(f"Number of cells along zonal direction: {num_cells_lon} (i.e iterations)")
    print(f"Number of cells along meridional direction: {num_cells_lat} (i.e iterations)")
    print()
    
    # Calculate the final latitude and longitude of the top-left cell
    starting_lat = central_lat + ((num_cells_lat // 2) - 1) * del_lat
    starting_lon = central_lon - ((num_cells_lon // 2) - 1) * del_lon

    # Format to 6 decimal places
    starting_lat = float(f"{starting_lat:.6f}")
    starting_lon = float(f"{starting_lon:.6f}")

    return starting_lat, starting_lon, num_cells_lon, num_cells_lat

starting_lat, starting_lon, num_cells_lon, num_cells_lat = divide_grid(central_lat, central_lon, grid_dim, del_lon, del_lat)
print(f"Starting latitude: {starting_lat:.6f}")
print(f"Starting longitude: {starting_lon:.6f}")
print()
print()

time.sleep(2)

# Iterate over the grid to capture screenshots
for i in tqdm(range(num_cells_lat), desc="Processing Screenshots", unit="row"):
    formatted_lat = format(starting_lat, '.6f') + "N"
    formatted_lon = format(starting_lon, '.6f') + "E"
    cell_y1 = f"{formatted_lat} {formatted_lon}"
    print(f"Screenshots for lat {formatted_lat} has begun")
    capture_location_screenshots(cell_y1, iterations=num_cells_lon)
    starting_lat -= del_lat  # Update latitude for the next row
    print("**************************")
    time.sleep(1)


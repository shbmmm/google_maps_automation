from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os

output_dir = "/app/screenshots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
        

def capture_location_screenshots(lat_lon, iterations):
    
    # Setup Chrome options
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1000,1000")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(options=options)
    action = ActionChains(driver)

    def ENTER(element):
        action.click(on_element=element)
        action.perform()

    def TYPE(text):
        action.send_keys(text)
        action.perform()
        
    # Function to capture screenshots iteratively
    def capture_grid_screenshots(iterations):     
        for i in range(iterations):
            current_url = driver.current_url
            pattern = r'@([0-9\.\-]+),([0-9\.\-]+),([0-9]+m)'

            match = re.search(pattern, current_url)
            if match:
                lat = match.group(1)
                lon = match.group(2)
            else:
                print("No match found")

            file_name = f"{lat}_{lon}.png"
            file_path = os.path.join(output_dir, file_name)
            driver.save_screenshot(file_path)
            print("---------------snapshot taken over: ", lat, lon)

            for _ in range(6):
                action.send_keys(Keys.ARROW_RIGHT).perform()
                time.sleep(1)  # Small delay between key presses

    # Open Google Maps
    driver.get("https://maps.google.com/")
    print("1. Google maps has been loaded.")
    time.sleep(2)

    # Search for the location
    search_box = driver.find_element(By.ID, "searchboxinput")
    ENTER(search_box)
    TYPE(lat_lon)
    search_button = driver.find_element(By.CLASS_NAME, "google-symbols")
    ENTER(search_button)
    print("2. lat lon entered and located.")
    time.sleep(2)

    layers_button = driver.find_element(By.CSS_SELECTOR, ".yHc72.qk5Wte")
    ENTER(layers_button)
    print("3. Satellite mode activated.")
    time.sleep(3)

    driver.implicitly_wait(20)
    action.move_to_element(layers_button).perform()
    more_layers = driver.find_element(By.CSS_SELECTOR, ".LGcAjc.aeXnX")
    ENTER(more_layers)
    print("4. [more layers] have been clicked.")
    time.sleep(3)

    driver.implicitly_wait(20)
    check_box = driver.find_element(By.CSS_SELECTOR, "#layer-switcher > div > div > div > div.yYTQHb > ul > li:nth-child(2) > button > span.xXq44b.google-symbols.NhBTye.PHazN")
    action.move_to_element(check_box).perform()
    ENTER(check_box)
    print("5. Labels have been removed")
    time.sleep(2)

    close_cross = driver.find_element(By.CSS_SELECTOR, "#layer-switcher > div > div > div > div.OwXc3d > header > button > span")
    ENTER(close_cross)
    print("6. [layers menu] has been dismissed.")
    time.sleep(3)

    left_arrow = driver.find_element(By.CLASS_NAME, "EIbCs")
    ENTER(left_arrow)
    print("7. Page has been customized for zooming.")
    time.sleep(2)

    zoom_in = driver.find_element(By.CSS_SELECTOR, "button.zHtKKd.widget-zoom-in[aria-label='Zoom in']")
    for _ in range(3):
        ENTER(zoom_in)
        
    print("--------page zoomed 3 times")
    time.sleep(1.5)

    for _ in range(8):
        zoom_in.send_keys(Keys.SHIFT, Keys.TAB)
        time.sleep(1)
        
    driver.implicitly_wait(5)
    canvas = driver.find_element(By.CSS_SELECTOR, ".iBPHvd")
    canvas.send_keys(Keys.RETURN)
    time.sleep(1)

    print("8. Function for the screenshot defined.")
    print("9. Initiating snapshot automation.")
    print("10. Files will be saved in the directory.")
    capture_grid_screenshots(iterations)
    time.sleep(3)
    driver.quit()
    print("Chrome browser has been closed")


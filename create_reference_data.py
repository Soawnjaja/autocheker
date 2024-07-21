import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def collect_website_data(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--log-level=3")  # Suppress logging
    driver = webdriver.Chrome(options=options)
    
    try:
        logging.info(f"Collecting data for {url}")
        driver.get(url)
        
        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Collect DOM structure
        dom_structure = driver.execute_script("return document.documentElement.outerHTML;")
        
        # Collect JavaScript and CSS files
        scripts = [script.get_attribute('src') for script in driver.find_elements(By.TAG_NAME, 'script') if script.get_attribute('src')]
        styles = [link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME, 'link') if link.get_attribute('rel') == 'stylesheet']
        
        # Save data
        data = {
            'url': url,
            'dom_structure': dom_structure,
            'scripts': scripts,
            'styles': styles
        }
        
        return data
    
    except Exception as e:
        logging.error(f"Error collecting data for {url}: {e}")
        return None
    
    finally:
        driver.quit()

def save_data(data, save_path):
    if data is None:
        return
    
    # Create directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    file_name = f"data_{data['url'].replace('https://', '').replace('http://', '').replace('/', '_')}.json"
    file_path = os.path.join(save_path, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# List of URLs
urls = [
    "https://print-one.ru",
    "https://interstone.su",
    "https://pandanail44.ru"
    # Add more URLs here
]

# Path to save files
save_path = "references"

# Collect data for each website
for url in urls:
    data = collect_website_data(url)
    save_data(data, save_path)

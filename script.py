import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def collect_website_data(url):
    options = webdriver.ChromeOptions()
    options.headless = True
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

def load_saved_data(url, save_path):
    file_name = f"data_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.json"
    file_path = os.path.join(save_path, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

def hash_data(data):
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode('utf-8')).hexdigest()

def compare_data(current_data, saved_data):
    current_hash = hash_data(current_data)
    saved_hash = hash_data(saved_data)
    return current_hash != saved_hash

def log_differences(current_data, saved_data, log_path):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    log_file = os.path.join(log_path, 'differences.log')
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write(f"Difference detected for {current_data['url']}:\n")
        file.write(f"Current data:\n{json.dumps(current_data, indent=4)}\n")
        file.write(f"Saved data:\n{json.dumps(saved_data, indent=4)}\n")
        file.write("\n")

# List of URLs
urls = [
    "https://print-one.ru",
    "https://interstone.su",
    "https://pandanail44.ru"
    # Add more URLs here
]

# Path to save files
save_path = "references"
log_path = "logs"

# Collect data for each website and compare with saved data
for url in urls:
    current_data = collect_website_data(url)
    saved_data = load_saved_data(url, save_path)
    
    if saved_data:
        if compare_data(current_data, saved_data):
            logging.info(f"Changes detected for {url}")
            log_differences(current_data, saved_data, log_path)
            save_data(current_data, save_path)  # Update saved data
        else:
            logging.info(f"No changes detected for {url}")
    else:
        logging.info(f"No saved data found for {url}. Saving current data.")
        save_data(current_data, save_path)

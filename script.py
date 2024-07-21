import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

def collect_website_data(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Сбор DOM-структуры
        dom_structure = driver.execute_script("return document.documentElement.outerHTML;")
        
        # Сбор ссылок на JavaScript и CSS файлы
        scripts = [script.get_attribute('src') for script in driver.find_elements(By.TAG_NAME, 'script') if script.get_attribute('src')]
        styles = [link.get_attribute('href') for link in driver.find_elements(By.TAG_NAME, 'link') if link.get_attribute('rel') == 'stylesheet']
        
        # Сохранение данных
        data = {
            'url': url,
            'dom_structure': dom_structure,
            'scripts': scripts,
            'styles': styles
        }
        
        return data
    
    finally:
        driver.quit()

def load_saved_data(url, save_path):
    file_name = f"data_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.json"
    file_path = os.path.join(save_path, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

def compare_data(current_data, saved_data):
    differences = {}
    for key in current_data:
        if current_data[key] != saved_data[key]:
            differences[key] = {
                'current': current_data[key],
                'saved': saved_data[key]
            }
    return differences

def log_differences(differences, log_path):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    log_file = os.path.join(log_path, 'differences.log')
    with open(log_file, 'a', encoding='utf-8') as file:
        for key, value in differences.items():
            file.write(f"Difference in {key}:\n")
            file.write(f"Current: {value['current']}\n")
            file.write(f"Saved: {value['saved']}\n")
            file.write("\n")

# Массив с URL-адресами сайтов
urls = [
    "https://print-one.ru",
    "https://interstone.su",
    "https://pandanail44.ru"
    # Добавьте сюда другие URL
]

# Путь для сохранения файлов
save_path = "references"
log_path = "logs"

# Сбор данных для каждого сайта и сравнение с сохраненными данными
for url in urls:
    current_data = collect_website_data(url)
    saved_data = load_saved_data(url, save_path)
    
    if saved_data:
        differences = compare_data(current_data, saved_data)
        if differences:
            print(f"Changes detected for {url}")
            log_differences(differences, log_path)
        else:
            print(f"No changes detected for {url}")
    else:
        print(f"No saved data found for {url}. Please run the initial data collection script.")

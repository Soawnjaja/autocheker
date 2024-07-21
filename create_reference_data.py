import json
import os
from selenium import webdriver

def collect_website_data(url, save_path):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Сбор DOM-структуры
        dom_structure = driver.execute_script("return document.documentElement.outerHTML;")
        
        # Сбор ссылок на JavaScript и CSS файлы
        scripts = [script.get_attribute('src') for script in driver.find_elements_by_tag_name('script') if script.get_attribute('src')]
        styles = [link.get_attribute('href') for link in driver.find_elements_by_tag_name('link') if link.get_attribute('rel') == 'stylesheet']
        
        # Сохранение данных
        data = {
            'url': url,
            'dom_structure': dom_structure,
            'scripts': scripts,
            'styles': styles
        }
        
        # Создание папки, если она не существует
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        file_name = f"data_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.json"
        file_path = os.path.join(save_path, file_name)
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    
    finally:
        driver.quit()

# Массив с URL-адресами сайтов
urls = [
    "https://example.com",
    "https://anotherexample.com",
    # Добавьте сюда другие URL
]

# Путь для сохранения файлов
save_path = "references"

# Сбор данных для каждого сайта
for url in urls:
    collect_website_data(url, save_path)

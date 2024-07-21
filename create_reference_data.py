import json
from selenium import webdriver

def collect_website_data(url):
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
        with open(f"data_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.json", 'w') as file:
            json.dump(data, file, indent=4)
    
    finally:
        driver.quit()

# Пример использования
collect_website_data("https://example.com")
import json
from selenium import webdriver

def check_website_data(url, reference_data_file):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    results = {'url': url, 'status': True}
    try:
        driver.get(url)
        
        # Получение текущей DOM-структуры и ресурсов
        current_dom = driver.execute_script("return document.documentElement.outerHTML;")
        current_scripts = [script.get_attribute('src') for script in driver.find_elements_by_tag_name('script') if script.get_attribute('src')]
        current_styles = [link.get_attribute('href') for link in driver.find_elements_by_tag, 'link') if link.get_attribute('rel') == 'stylesheet']
        
        # Загрузка эталонных данных
        with open(reference_data_file, 'r') as file:
            reference_data = json.load(file)
        
        # Сравнение DOM-структуры, скриптов и стилей
        if current_dom != reference_data['dom_structure'] or \
           set(current_scripts) != set(reference_data['scripts']) or \
           set(current_styles) != set(reference_data['styles']):
            results['status'] = False
    
    finally:
        driver.quit()
    return results

def main():
    websites = [
        {"url": "https://interstone.su", "data_file": "data_interstone_su.json"},
        {"url": "https://print-one.ru", "data_file": "data_print_one_ru.json"},
        {"url": "https://officecrew.ru", "data_file": "data_officecrew_ru.json"}
    ]
    
    results = []
    for site in websites:
        result = check_website_data(site['url'], site['data_file'])
        results.append(result)
    
    # Формирование отчета
    print("Отчет о проверке сайтов:")
    for result in results:
        status = "все хорошо" if result['status'] else "есть изменения"
        print(f"{result['url']}: {status}")

if __name__ == "__main__":
    main()
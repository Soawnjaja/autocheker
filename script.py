import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import hashlib
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TreeNode:
    def __init__(self, data, children=[]):
        self.data = data
        self.children = children
    
    def is_leaf(self):
        return not self.children

def hash_node(data):
    return hashlib.sha256(data.encode()).hexdigest()

def hash_tree(node):
    if node.is_leaf():
        return hash_node(node.data)
    else:
        child_hashes = ''.join(hash_tree(child) for child in node.children)
        return hash_node(child_hashes)

def build_tree_from_element(element):
    children = element.find_elements(By.XPATH, "./*")
    child_nodes = [build_tree_from_element(child) for child in children]
    return TreeNode(element.tag_name + element.get_attribute('outerHTML'), child_nodes)

def collect_website_data(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    try:
        logging.info(f"Сбор данных для {url}")
        driver.get(url)
        
        # Получение корневого элемента DOM
        root_element = driver.find_element(By.XPATH, '/*')
        root_node = build_tree_from_element(root_element)
        
        # Хеширование дерева
        dom_hash = hash_tree(root_node)
        
        # Сохранение хеша
        data = {
            'url': url,
            'dom_hash': dom_hash
        }
        
        logging.debug(f"Собранные данные для {url}: {json.dumps(data, indent=4)}")
        return data
    
    except Exception as e:
        logging.error(f"Ошибка при сборе данных для {url}: {e}")
        return None
    
    finally:
        driver.quit()

def save_data(data, save_path):
    if data is None:
        return
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    file_name = f"data_{data['url'].replace('https://', '').replace('http://', '').replace('/', '_')}.json"
    file_path = os.path.join(save_path, file_name)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    
    logging.info(f"Данные сохранены для {data['url']} по пути {file_path}")

def load_saved_data(url, save_path):
    file_name = f"data_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.json"
    file_path = os.path.join(save_path, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            saved_data = json.load(file)
            logging.debug(f"Загруженные сохраненные данные для {url}: {json.dumps(saved_data, indent=4)}")
            return saved_data
    return None

def compare_data(current_data, saved_data):
    current_hash = current_data['dom_hash']
    saved_hash = saved_data['dom_hash']
    logging.debug(f"Текущий хэш: {current_hash}, Сохраненный хэш: {saved_hash}")
    return current_hash != saved_hash

def log_differences(current_data, saved_data, log_path):
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    
    log_file = os.path.join(log_path, 'differences.log')
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write(f"Обнаружены различия для {current_data['url']}:\n")
        file.write(f"Текущие данные:\n{json.dumps(current_data, indent=4)}\n")
        file.write(f"Сохраненные данные:\n{json.dumps(saved_data, indent=4)}\n")
        file.write("\n")
    
    logging.info(f"Различия записаны для {current_data['url']}")

# Список URL-адресов и путь для сохранения файлов
urls = ["https://print-one.ru", "https://interstone.su", "https://pandanail44.ru"]
save_path = "references"
log_path = "logs"

# Сбор данных для каждого сайта и сравнение с сохраненными данными
for url in urls:
    current_data = collect_website_data(url)
    saved_data = load_saved_data(url, save_path)
    
    if saved_data:
        if compare_data(current_data, saved_data):
            logging.info(f"Обнаружены изменения для {url}")
            log_differences(current_data, saved_data, log_path)
            save_data(current_data, save_path)  # Обновление сохраненных данных
        else:
            logging.info(f"Изменений не обнаружено для {url}")
    else:
        logging.info(f"Сохраненные данные не найдены для {url}. Сохранение текущих данных.")
        save_data(current_data, save_path)

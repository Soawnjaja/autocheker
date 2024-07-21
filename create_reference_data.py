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

# Список URL-адресов и путь для сохранения файлов
urls = ["https://print-one.ru", "https://interstone.su", "https://pandanail44.ru"]
save_path = "references"

# Сбор данных для каждого сайта и сохранение в качестве эталона
for url in urls:
    current_data = collect_website_data(url)
    save_data(current_data, save_path)

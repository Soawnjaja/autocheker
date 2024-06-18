import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка опций Chrome
options = webdriver.ChromeOptions()
options.headless = True 

# Создание экземпляра драйвера
driver = webdriver.Chrome(options=options)

# Путь к главной папке приложения
base_path = os.path.dirname(os.path.abspath(__file__))
screenshots_path = os.path.join(base_path, 'screenshots')
os.makedirs(screenshots_path, exist_ok=True)

# Список URL сайтов для проверки
urls = [
    "https://print-one.ru",
    "https://interstone.su"
]

# Размеры устройств
devices = {
    "desktop": (1920, 1080),
    "tablet": (768, 1024),
    "mobile": (375, 667),
}

# Функция для создания скриншота
def create_screenshot(url, device_name, device_size):
    driver.set_window_size(*device_size)
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    domain_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace(".", "_")
    screenshot_path = os.path.join(screenshots_path, f'{device_name}_{domain_name}_home.png')
    driver.save_screenshot(screenshot_path)
    print(f"Скриншот для {url} на устройстве {device_name} сохранен.")

# Создание скриншотов
for url in urls:
    for device_name, device_size in devices.items():
        create_screenshot(url, device_name, device_size)

driver.quit()
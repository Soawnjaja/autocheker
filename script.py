import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from skimage.metrics import structural_similarity as ssim
import cv2

# Настройка опций Chrome
options = webdriver.ChromeOptions()
options.headless = True 

# Создание экземпляра драйвера
driver = webdriver.Chrome(options=options)

# Путь к главной папке приложения
base_path = os.path.dirname(os.path.abspath(__file__))
reference_path = os.path.join(base_path, 'reference')
screenshots_path = os.path.join(base_path, 'screenshots')
os.makedirs(reference_path, exist_ok=True)
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

# Функция для создания и сравнения скриншотов
def create_and_compare_screenshot(url, device_name, device_size):
    driver.set_window_size(*device_size)
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    domain_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace(".", "_")
    screenshot_filename = f'{device_name}_{domain_name}_home.png'
    screenshot_path = os.path.join(screenshots_path, screenshot_filename)
    reference_screenshot_path = os.path.join(reference_path, screenshot_filename)

    driver.save_screenshot(screenshot_path)
    print(f"Скриншот для {url} на устройстве {device_name} сохранен.")

    # Сравнение скриншотов
    if os.path.exists(reference_screenshot_path):
        original = cv2.imread(reference_screenshot_path, cv2.IMREAD_GRAYSCALE)
        new_shot = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)
        score, _ = ssim(original, new_shot, full=True)
        print(f"SSIM score for {url} on {device_name}: {score}")
    else:
        print(f"No reference screenshot found for {url} on {device_name}. Please check the reference directory.")

# Создание и сравнение скриншотов
for url in urls:
    for device_name, device_size in devices.items():
        create_and_compare_screenshot(url, device_name, device_size)

driver.quit()
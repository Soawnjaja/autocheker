import os
from selenium import webdriver
from PIL import Image, ImageChops

# Путь к главной папке приложения
base_path = os.path.dirname(os.path.abspath(__file__))
reference_path = os.path.join(base_path, 'reference')
screenshots_path = os.path.join(base_path, 'screenshots')
os.makedirs(reference_path, exist_ok=True)
os.makedirs(screenshots_path, exist_ok=True)

# Настройка WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Список URL сайтов для проверки
urls = ["https://artgroup76.ru", "https://print-one.ru", "https://interstone.su", "https://print-one.ru/"]

# Размеры устройств
devices = {"desktop": (1920, 1080), "tablet": (768, 1024), "mobile": (375, 667)}

def create_screenshot(url, device_name, device_size):
    driver.set_window_size(*device_size)
    driver.get(url)
    domain_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace(".", "_")
    screenshot_path = os.path.join(screenshots_path, f'{device_name}_{domain_name}.png')
    driver.save_screenshot(screenshot_path)
    return screenshot_path

def compare_screenshots(reference_path, test_path):
    try:
        image_one = Image.open(reference_path)
        image_two = Image.open(test_path)
        diff = ImageChops.difference(image_one, image_two)
        return not diff.getbbox()
    except FileNotFoundError:
        print(f"Файл не найден: {reference_path}")
        return False
 
# Проверка сайтов
for url in urls:
    for device_name, device_size in devices.items():
        temp_screenshot = create_screenshot(url, device_name, device_size)
        ref_screenshot_path = os.path.join(reference_path, f'{device_name}_{url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace(".", "_")}.png')
        if compare_screenshots(ref_screenshot_path, temp_screenshot):
            print(f"Сайт {url} на устройстве {device_name} соответствует эталону.")
        else:
            print(f"Обнаружены изменения на сайте {url} на устройстве {device_name}.")

driver.quit()
import os
from selenium import webdriver
from PIL import Image, ImageChops
from bitrix_integration import send_message_to_bitrix

# Путь к главной папке приложения
base_path = os.path.dirname(os.path.abspath(__file__))

# Пути к папкам скриншотов
screenshots_path = os.path.join(base_path, 'screenshots')
os.makedirs(screenshots_path, exist_ok=True)

# Настройка WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Список URL сайтов для проверки
urls = ["https://artgroup76.ru",
    "https://print-one.ru",
    "https://interstone.su",
    "https://print-one.ru/"]

# Размеры устройств
devices = {"desktop": (1920, 1080), "tablet": (768, 1024), "mobile": (375, 667)}

# Функции для создания и сравнения скриншотов
def create_screenshot(url, device_name, device_size):
    driver.set_window_size(*device_size)
    driver.get(url)
    domain_name = url.replace("http://", "").replace(".", "_")
    screenshot_path = os.path.join(screenshots_path, f'{device_name}_{domain_name}.png')
    driver.save_screenshot(screenshot_path)
    return screenshot_path

def compare_screenshots(reference_path, test_path):
    image_one = Image.open(reference_path)
    image_two = Image.open(test_path)
    diff = ImageChops.difference(image_one, image_two)
    return not diff.getbbox()

# Проверка сайтов
for url in urls:
    for device_name, device_size in devices.items():
        temp_screenshot = create_screenshot(url, device_name, device_size)
        reference_screenshot = os.path.join(base_path, 'reference', f'{device_name}_{url.replace("http://", "").replace(".", "_")}.png')
        if compare_screenshots(reference_screenshot, temp_screenshot):
            message = f"Сайт {url} на устройстве {device_name} соответствует эталону."
        else:
            message = f"Обнаружены изменения на сайте {url} на устройстве {device_name}."
        send_message_to_bitrix(message)

driver.quit()
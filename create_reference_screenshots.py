import os
from selenium import webdriver

# Настройка опций Chrome
options = webdriver.ChromeOptions()
options.headless = True 

# Создание экземпляра драйвера
driver = webdriver.Chrome(options=options)

# Путь к главной папке приложения
base_path = os.path.dirname(os.path.abspath(__file__))
reference_path = os.path.join(base_path, 'reference')
os.makedirs(reference_path, exist_ok=True)

# Список URL сайтов для проверки
urls = [
    "https://artgroup76.ru",
    "https://print-one.ru",
    "https://interstone.su",
    "https://peachdesign.ru"
    # Добавьте все необходимые сайты
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
    domain_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace(".", "_")
    screenshot_path = os.path.join(reference_path, f'{device_name}_{domain_name}.png')
    print(f"Путь для сохранения скриншота: {screenshot_path}")
    try:
        driver.save_screenshot(screenshot_path)
        print(f"Скриншот для {url} на устройстве {device_name} сохранен.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

# Создание эталонных скриншотов
for url in urls:
    for device_name, device_size in devices.items():
        create_screenshot(url, device_name, device_size)

driver.quit()

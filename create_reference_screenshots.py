import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка опций Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Создание экземпляра драйвера
driver = webdriver.Chrome(options=options)

# Путь к главной папке приложения
base_path = os.path.dirname(os.path.abspath(__file__))
screenshots_path = os.path.join(base_path, 'reference')
os.makedirs(screenshots_path, exist_ok=True)

# Список URL сайтов для проверки
urls = [
    "https://print-one.ru",
    "https://interstone.su"
]

# Устройства для эмуляции
devices = {
    "desktop": {"width": 1920, "height": 1080, "deviceScaleFactor": 1, "mobile": False},
    "iPad Mini": {"width": 768, "height": 1024, "deviceScaleFactor": 2, "mobile": True, "userAgent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"},
    "iPhone 14": {"width": 390, "height": 844, "deviceScaleFactor": 3, "mobile": True, "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"}
}

# Функция для создания скриншота
def create_screenshot(url, device_name, device_params):
    # Настройка эмуляции устройства
    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', device_params)
    if 'userAgent' in device_params:
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": device_params['userAgent']})

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    # Прокрутка страницы для загрузки всего контента
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.readyState") == "complete")

    domain_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_").replace(".", "_")
    screenshot_path = os.path.join(screenshots_path, f'{device_name}_{domain_name}_home.png')
    driver.save_screenshot(screenshot_path)
    print(f"Скриншот для {url} на устройстве {device_name} сохранен.")

# Создание скриншотов
for url in urls:
    for device_name, device_params in devices.items():
        create_screenshot(url, device_name, device_params)

driver.quit()

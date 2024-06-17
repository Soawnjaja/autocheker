# MyWebChecker

## Установка
1. Убедитесь, что Python и Google Chrome установлены на вашем компьютере.
2. Склонируйте репозиторий или скачайте файлы в папку на вашем рабочем столе.
3. Установите необходимые зависимости:
    pip install selenium Pillow bitrix24-rest
4. Настройте путь к ChromeDriver в `script.py`, если это необходимо.

## Настройка
1. В файле `bitrix_integration.py` укажите URL вашего webhook из Bitrix24.
2. Поместите эталонные скриншоты в папку `reference/`.
3.  Примеры именования файлов:
Для сайта my-site.com, нужно создать три разных скриншота для каждого типа устройства (десктоп, планшет, мобильный), используя следующую схему именования:
desktop_my_site_com.png
tablet_my_site_com.png
mobile_my_site_com.png
## Запуск
Запустите скрипт командой: python script.py



author : Wishinskiy A.M
=======
# autocheker
py script for check availability sites

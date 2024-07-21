# AutoChecker

## Установка

1. Убедитесь, что Python и Google Chrome установлены на вашем компьютере.
2. Склонируйте репозиторий или скачайте файлы в папку на вашем рабочем столе.
3. Установите необходимые зависимости:
sh pip install selenium
4. Настройте путь к ChromeDriver в `script.py`, если это необходимо.

## Настройка

1. В файле `script.py` укажите массив URL-адресов сайтов, которые вы хотите проверить.
2. Поместите эталонные данные в папку `references/`.

### Примеры именования файлов:

Для сайта `example.com`, данные должны быть сохранены в файле с именем:
data_example_com.json

## Запуск

Запустите скрипт командой:
sh python script.py
## Описание функционала

1. **Сбор данных**: Скрипт собирает DOM-структуру, ссылки на JavaScript и CSS файлы с указанных сайтов.
2. **Сравнение данных**: Скрипт сравнивает текущие данные с сохраненными эталонными данными.
3. **Логирование различий**: В случае обнаружения различий, они логируются в файл `logs/differences.log`.
4. **Обновление данных**: Если обнаружены изменения, текущие данные сохраняются в папку `references`.

## Пример использования
python

Массив с URL-адресами сайтов
urls = [ "https://example.com", "https://anotherexample.com", # Добавьте сюда другие URL ]

Путь для сохранения файлов
save_path = "references" log_path = "logs"

Сбор данных для каждого сайта и сравнение с сохраненными данными
for url in urls: current_data = collect_website_data(url) saved_data = load_saved_data(url, save_path)

if saved_data:
    differences = compare_data(current_data, saved_data)
    if differences:
        print(f"Changes detected for {url}")
        log_differences(differences, log_path)
        save_data(current_data, save_path)  # Обновление сохраненных данных
    else:
        print(f"No changes detected for {url}")
else:
    print(f"No saved data found for {url}. Saving current data.")
    save_data(current_data, save_path)

## Автор

Wishinskiy A.M

# Проект парсинга PEP
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![BeautifulSoup4](https://img.shields.io/badge/-BeautifulSoup4-464646?style=flat&logo=BeautifulSoup4&logoColor=ffffff&color=043A6B)](https://www.crummy.com/software/BeautifulSoup/)
[![Prettytable](https://img.shields.io/badge/-Prettytable-464646?style=flat&logo=Prettytable&logoColor=ffffff&color=043A6B)](https://github.com/jazzband/prettytable)
[![Logging](https://img.shields.io/badge/-Logging-464646?style=flat&logo=Logging&logoColor=ffffff&color=043A6B)](https://docs.python.org/3/library/logging.html)

## Парсинг документов PEP

> Парсер собирает данные обо всех PEP документах, сравнивает статусы и записывает их в файл,
также реализованы сбор информации о статусе версий, скачивание архива с документацией и сбор ссылок о новостях в Python,
> логирует свою работу и ошибки в командную строку и файл логов.

## Примеры команд
### _Доступные аргументы командной строки_
Для просмотра режимов работы парсера в терминале введите команду 
с именованным аргументом ```-h``` или  ```--help```:  
```
python src/main.py -h
```
Выведет справку по использованию:
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
Создаст csv файл с таблицей из двух колонок: «Статус» и «Количество»:
```
python main.py pep -o file
```

Выводит таблицу prettytable с тремя колонками: "Ссылка на документацию", "Версия", "Статус":
```
python main.py latest-versions -o pretty 
```

Выводит ссылки в консоль на нововведения в python:
```
python main.py whats-new
```
Автор: [Елизавета Шалаева](https://github.com/kaspeya)

# Проект парсинга pep

Аргументы командной строки:
usage: main.py [-h] [-c] [-o {pretty,file}]
               {whats-new,latest-versions,download}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных 
import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from outputs import control_output
from constants import (ARGS_LOG_INFO, BASE_DIR, DOWNLOAD_LOG_INFO,
                       EXPECTED_STATUS, FINISH_LOG_INFO, MAIN_DOC_URL,
                       PEP_URL, START_LOG_INFO,)
from utils import find_tag, get_response, get_soup


def whats_new(session):
    """Парсер статей по нововведениям в питон."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = main_div.find('div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    # Добавляем в пустой список заголовки таблицы.
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            # Если страница не загрузится, программа перейдёт к след. ссылке.
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        # Добавление в список ссылок и текстов из тегов h1 и dl в виде кортежа.
        results.append(
            (version_link, h1.text, dl_text)
        )
    
    return results


def latest_versions(session):
    """Парсер текущих версий питона с описанием."""
    soup = get_soup(session, MAIN_DOC_URL)
    sidebar = soup.find('div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    # Перебор в цикле всех найденных списков.
    for ul in ul_tags:
        # Проверка, есть ли искомый текст в содержимом тега.
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')
    
    # Добавляем в пустой список заголовки таблицы.
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    # Шаблон для поиска версии и статуса:
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    # Цикл для перебора тегов <a>, полученных ранее.
    for a_tag in a_tags:
        # Извлечение ссылки.
        link = a_tag['href']
        # Поиск паттерна в ссылке.
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            # Если строка соответствует паттерну,
            # переменным присываивается содержимое групп, начиная с первой.
            version, status = text_match.groups()
        else:
            # Если строка не соответствует паттерну, первой переменной
            # присваивается весь текст, второй — пустая строка.
            version, status = a_tag.text, ''
            # Добавление полученных переменных в список в виде кортежа.
        results.append(
            (link, version, status)
        )
        return results


def download(session):
    """Парсер, скачивающий документацию."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)
    main_tag = soup.find('div', {'role': 'main'})
    table_tag = main_tag.find('table', {'class': 'docutils'})
    # Команда получения нужного тега.
    pdf_a4_tag = table_tag.find('a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    # Сохраняем в переменную содержимое атрибута href.
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    
    filename = archive_url.split('/')[-1]
    # Сформируйте путь до директории downloads.
    downloads_dir = BASE_DIR / 'downloads'
    # Создайте директорию.
    downloads_dir.mkdir(exist_ok=True)
    # Получите путь до архива, объединив имя файла с директорией.
    archive_path = downloads_dir / filename
    # Загрузка архива по ссылке.
    response = session.get(archive_url)
    
    # В бинарном режиме открывается файл на запись по указанному пути.
    with open(archive_path, 'wb') as file:
        # Полученный ответ записывается в файл.
        file.write(response.content)
    
    logging.info(DOWNLOAD_LOG_INFO.format(archive_path=archive_path))


def pep(session):
    """Парсер статусов PEP."""
    soup = get_soup(session, PEP_URL)
    section = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tbody_tag = find_tag(section, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    pep_count = 0
    status_dict = defaultdict(int)
    # Добавляем в пустой список заголовки таблицы.
    results = [('Статус', 'Количество')]
    for n in tqdm(tr_tags):
        pep_count += 1
        data = list(find_tag(n, 'abbr').text)
        preview_status = data[1:][0] if len(data) > 1 else ''
        url = urljoin(PEP_URL, find_tag(n, 'a', attrs={
            'class': 'pep reference internal'})['href'])
        soup = get_soup(session, url)
        table_info = find_tag(soup, 'dl',
                              attrs={'class': 'rfc2822 field-list simple'})
        status_pep_page = table_info.find(
            string='Status').parent.find_next_sibling('dd').string
        status_dict[status_pep_page] = status_dict.get(status_pep_page, 0) + 1
        if status_pep_page not in EXPECTED_STATUS[preview_status]:
            error_message = ('Несовпадающие статусы:\n'
                             f'{url}\n'
                             f'Статус в карточке: {status_pep_page}\n'
                             'Ожидаемые статусы: '
                             f'{EXPECTED_STATUS[preview_status]}')
            logging.warning(error_message)
    results.extend([(status, status_dict[status]) for status in status_dict])
    results.append(('Total', pep_count))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    # Запускаем функцию с конфигурацией логов.
    configure_logging()
    # Отмечаем в логах момент запуска программы.
    logging.info(START_LOG_INFO)
    # Конфигурация парсера аргументов командной строки —
    # передача в функцию допустимых вариантов выбора.
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    # Считывание аргументов из командной строки.
    args = arg_parser.parse_args()
    # Логируем переданные аргументы командной строки.
    logging.info(ARGS_LOG_INFO.format(args=args))
    
    # Создание кеширующей сессии.
    session = requests_cache.CachedSession()
    # Если был передан ключ '--clear-cache', то args.clear_cache == True.
    if args.clear_cache:
        # Очистка кеша.
        session.cache.clear()
    
    # Получение из аргументов командной строки нужного режима работы.
    parser_mode = args.mode
    # Поиск и вызов нужной функции по ключу словаря.
    # С вызовом функции передаётся и сессия.
    results = MODE_TO_FUNCTION[parser_mode](session)
    
    # Если из функции вернулись какие-то результаты,
    if results is not None:
        # передаём их в функцию вывода вместе с аргументами командной строки.
        control_output(results, args)
    # Логируем завершение работы парсера.
    logging.info(FINISH_LOG_INFO)


if __name__ == '__main__':
    main()

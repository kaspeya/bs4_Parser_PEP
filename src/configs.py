import argparse
import logging
from logging.handlers import RotatingFileHandler

from src.constants import BASE_DIR, DT_FORMAT, LOG_FORMAT


def configure_argument_parser(available_modes):
    """Конфигурация аргументов командной строки."""
    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=('pretty', 'file'),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    """Конфигурация логирования."""
    # Создание директории для логов.
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    # Получение абсолютного пути до файла с логами.
    log_file = log_dir / 'parser.log'

    # Инициализация хендлера с ротацией логов.
    # Максимальный объём одного файла — десять в шестой степени байт (10**6),
    # максимальное количество файлов с логами — 5.
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    # Базовая настройка логирования basicConfig.
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        # Уровень записи логов.
        level=logging.INFO,
        # Вывод логов в терминал.
        handlers=(rotating_handler, logging.StreamHandler())
    )
